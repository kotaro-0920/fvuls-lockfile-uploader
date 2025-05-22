#!/usr/bin/env python

import os
import requests
import validators

FVULS_BASE_URL = os.getenv('FVULS_BASE_URL', 'https://rest.vuls.biz')
VULS_SAAS_TOKEN = os.environ['FVULS_TOKEN']
VULS_SAAS_UUID = os.environ['FVULS_SERVER_UUID']
FVULS_LOCKFILE_PATH = os.getenv('INPUT_PATH', None)
# Read inputs
REPO_NAME = os.getenv('INPUT_REPONAME', None)


print(REPO_NAME)
print(FVULS_BASE_URL)
print(FVULS_TOKEN)
print(FVULS_SERVER_UUID)
print(FVULS_LOCKFILE_PATH)

def create_request(method, endpoint, params={}, data={}):
    try:
        headers = {
            'Authorization': FVULS_TOKEN,
            'Accept': 'application/json'
        }

        if FVULS_LOCKFILE_PATH is None:
            print("You have to specify path")
            return exit(1)

        if method == 'POST' or method == 'PUT':
            # override path if reponame exists
            data['path'] = FVULS_LOCKFILE_PATH
            if REPO_NAME is not None:
                is_url = validators.url(REPO_NAME)
                if is_url:
                    normalize_path = os.path.normpath(FVULS_LOCKFILE_PATH)
                    data['path'] = REPO_NAME + normalize_path
                else:
                    join = os.path.join(REPO_NAME, FVULS_LOCKFILE_PATH)
                    data['path'] = os.path.normpath(join)

            # read lockfile content
            with open(FVULS_LOCKFILE_PATH, 'r') as file:
                data['fileContent'] = file.read()

            headers.update({'Content-Type': 'application/json'})
            res = requests.request(
                method,
                url=f'{FVULS_BASE_URL}/{endpoint}',
                headers=headers,
                json=data
            ).json()
        else:
            if REPO_NAME and 'filterPath' in params:
                join = os.path.join(REPO_NAME, FVULS_LOCKFILE_PATH)
                params['filterPath'] = os.path.normpath(join)

            res = requests.request(
                method,
                url=f'{FVULS_BASE_URL}/{endpoint}',
                params=params,
                headers=headers
            ).json()

        if 'message' in res:
            print(res)
            return exit(1)

        return res
    except ValueError as e:
        # handle parse error
        print(e)
        return exit(1)


def main():
    servers_res = create_request(
        'GET',
        f'v1/server/uuid/{FVULS_SERVER_UUID}',
    )

    # check that .json() did NOT return an empty dict
    if servers_res:
        server_id = servers_res['id']

        # Get lock files
        lockfiles_res = create_request(
            'GET',
            'v1/lockfiles',
            params={
                'page': 1,
                'limit': 20,
                'offset': 0,
                'filterServerID': server_id,
                'filterPath': FVULS_LOCKFILE_PATH
            }
        )

        # check if list is not empty
        if 'lockfiles' in lockfiles_res:
            # updates lockfile
            lockfile_id = lockfiles_res['lockfiles'][0]['id']

            post_res = create_request(
                'PUT',
                f'v1/lockfile/{lockfile_id}',
            )

            if post_res['id']:
                print(f'Updated lockfile: {lockfile_id}')
                return exit(0)
        else:
            payload = {'serverID': server_id}
            post_res = create_request('POST', 'v1/lockfile', data=payload)

            if post_res['id']:
                print(f'Created lockfile: {post_res["id"]}')
                return exit(0)


if __name__ == "__main__":
    main()
