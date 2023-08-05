'''
Predefined queries for Cirrus API

Designed to work with the following schema (2020-01-17):
https://github.com/cirruslabs/cirrus-ci-web/blob/1806cccc/schema.graphql
'''


from time import monotonic as time, sleep
import logging

from . import CirrusAPI


log = logging.getLogger(__name__)


class CirrusQueryError(ValueError):
    '''Raised when query executes successfully but returns invalid data'''


class CirrusBuildError(RuntimeError):
    '''Raised on build failures'''


class CirrusTimeoutError(RuntimeError):
    '''Raised when build takes too long'''


def get_repo(api: CirrusAPI, owner: str, repo: str) -> str:
    '''Get internal ID for GitHub repo'''
    query = '''
        query GetRepos($owner: String!) {
            githubRepositories(owner: $owner) {
                id
                name
            }
        }
    '''
    params = dict(owner=owner)
    all_repos = api(query, params)
    for item in all_repos['githubRepositories']:
        if item['name'] == repo:
            return item['id']
    raise CirrusQueryError('repo not found: {}/{}'.format(owner, repo))


def create_build(api: CirrusAPI,
                 repo_id: str,
                 repo_branch: str = 'master',
                 config: str = '') -> str:
    '''
    Trigger new build on Cirrus CI

    Return build ID
    '''
    query = '''
        mutation ScheduleCustomBuild($config: String!,
                                     $repo: ID!,
                                     $branch: String!,
                                     $mutation_id: String!) {
            createBuild(
                input: {
                    repositoryId: $repo,
                    branch: $branch,
                    clientMutationId: $mutation_id,
                    configOverride: $config
                }
            ) {
                build {
                    id
                    status
                }
            }
        }
    '''
    mutation_id = 'cirrus-run job {}'.format(int(time()))
    answer = api(
        query=query,
        params=dict(
            repo=repo_id,
            branch=repo_branch,
            mutation_id=mutation_id,
            config=config),
    )
    return answer['createBuild']['build']['id']


def wait_build(api, build_id: str, delay=3, abort=60*60):
    '''Wait until build finishes'''
    query = '''
        query GetBuild($build: ID!) {
            build(id: $build) {
                status
            }
        }
    '''
    params = dict(build=build_id)

    time_start = time()
    while time() < time_start + abort:
        response = api(query, params)
        status = response['build']['status']
        log.info('build {}: {}'.format(build_id, status))
        if status in {'COMPLETED'}:
            return True
        if status in {'CREATED', 'TRIGGERED', 'EXECUTING'}:
            sleep(delay)
            continue
        if status in {'NEEDS_APPROVAL', 'FAILED', 'ABORTED', 'ERRORED'}:
            raise CirrusBuildError('build {} was terminated: {}'.format(build_id, status))
        raise CirrusBuildError('build {} returned unknown status: {}'.format(build_id, status))
    raise CirrusTimeoutError('build {} timed out'.format(build_id))
