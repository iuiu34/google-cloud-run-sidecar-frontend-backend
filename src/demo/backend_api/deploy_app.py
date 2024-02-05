import re
import subprocess

import fire
import yaml


def get_release_candidate(filename):
    with open(filename) as f:
        data = f.read()

    # Find the current version in the file
    match = re.search(r'v[0-9]+\.[0-9]+\.[0-9]+(rc[0-9]+)?', data)

    if match is None:
        print("No version found in the file.")
        return

    current_version = match.group()

    # Check if the version contains a release candidate number
    if 'rc' in current_version:
        # Split the version into base version and release candidate number
        base_version, rc_number = re.match(r'(v[0-9]+\.[0-9]+\.[0-9]+rc)([0-9]+)', current_version).groups()

        # Increment the release candidate number
        new_rc_number = int(rc_number) + 1

        # Combine the base version and new release candidate number to form the new version
        new_version = base_version + str(new_rc_number)
    else:
        # If the version doesn't contain a release candidate number, append 'rc1' to it
        new_version = current_version + 'rc1'

    # Replace the current version with the new version
    data_ = data.replace(current_version, new_version)

    # Write the updated data back to the file
    with open(filename, 'w') as f:
        f.write(data_)


def deploy_app(docker: bool = True,
               cloud_run: bool = False,
               app_engine: bool = False,
               frontend: bool = False,
               dev: bool = False,
               tox: bool = True):
    repo = 'ds-demo'
    if cloud_run and app_engine:
        raise ValueError('Cannot deploy to both Cloud Run and App Engine. Choose one.')

    if app_engine:
        filename = 'app.yaml'
    else:
        filename = 'service.yaml'

    if dev:
        filename = filename.split('.')
        filename = f"{filename[0]}_dev.{filename[1]}"
        branch = 'dev'
        subbranch = 'test'
    else:
        branch = 'master'
        subbranch = 'dev'

    if cloud_run and docker:
        get_release_candidate(filename)

    with open(filename) as f:
        app_config = yaml.full_load(f)

    if app_engine:
        image_url = app_config['env_variables']['IMAGE_URL']
    else:
        image_url = app_config['spec']['template']['spec']['containers'][-1]['image']

    if tox:
        cmd = 'tox'
        subprocess.run(cmd, check=True)

    if docker:
        cmd = 'container/vm_docker_build.sh'
        cmd = f'sh {cmd} {image_url} {branch} {subbranch} {repo}'
        subprocess.run(cmd, check=True)

    if docker and frontend:
        repo = f'{repo}/frontend'
        image_url = app_config['spec']['template']['spec']['containers'][0]['image']
        cmd = 'container/vm_docker_build.sh'
        cmd = f'sh {cmd} {image_url} {branch} {subbranch} {repo}'
        subprocess.run(cmd, check=True)

    if cloud_run:
        service_name = app_config['metadata']['name']
        # cmd = f'sh gcloud run services delete {service_name} -q'
        # subprocess.run(cmd, check=True)
        cmd = f"sh gcloud run services replace {filename}"
        subprocess.run(cmd, check=True)
        cmd = f'sh gcloud run services add-iam-policy-binding {service_name} ' \
              f'--member="allUsers" --role="roles/run.invoker"'
        subprocess.run(cmd, check=True)
    elif app_engine:
        cmd = f"sh gcloud app deploy {filename} -q --image-url={image_url}"
        subprocess.run(cmd, check=True)


def main():
    """Execute main program."""
    fire.Fire(deploy_app)
    print('\x1b[6;30;42m', 'Success!', '\x1b[0m')


if __name__ == "__main__":
    main()
