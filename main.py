import os
import requests


FVULS_BASE_URL = os.environ['FVULS_BASE_URL']
FVULS_TOKEN = os.environ['FVULS_TOKEN']
FVULS_SERVER_UUID = os.environ['FVULS_SERVER_UUID']
FVULS_LOCKFILE_PATH = os.environ['FVULS_LOCKFILE_PATH']
FILE_CONTENT = ""

print(os.environ)


def create_request(method, endpoint, params={}, data={}):
    try:
        headers = {
            'Authorization': FVULS_TOKEN,
            'Accept': 'application/json'
        }

        if method == 'POST' or method == 'PUT':
            # merge two headers
            headers = headers.update({'Content-Type': 'application/json'})
            res = requests.request(
                method,
                url=f'{FVULS_BASE_URL}/{endpoint}',
                headers=headers,
                json=data
            ).json()
        else:
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
            # read lockfile content
            with open(FVULS_LOCKFILE_PATH, 'r') as file:
                FILE_CONTENT = file.read()

            payload = {
                'fileContent': FILE_CONTENT,
                'path': FVULS_LOCKFILE_PATH,
            }

            post_res = create_request(
                'PUT',
                f'v1/lockfile/{lockfile_id}',
                data=payload
            )

            if post_res['id']:
                print(f'Updated lockfile: {lockfile_id}')
                return exit(0)
        else:
            # read lockfile content
            with open(FVULS_LOCKFILE_PATH, 'r') as file:
                FILE_CONTENT = file.read()

            payload = {
                'fileContent': FILE_CONTENT,
                'path': FVULS_LOCKFILE_PATH,
                'serverID': server_id,
            }

            post_res = create_request('POST', 'v1/lockfile', data=payload)
            lockfile_id = post_res['id']

            if lockfile_id:
                print(f'Created lockfile: {lockfile_id}')
                return exit(0)


if __name__ == "__main__":
    main()
