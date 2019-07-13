#!/usr/bin/python3

from fabric.api import env, run, cd, task

debug = False

"""
Fabric deploy script

This is a Fabric (python 3) deployment script to be used by CircleCI to
deploy this project automatically to either production or staging.
"""

env.path = 'hackathon/transport_server'
env.user = 'admin123'


@task
def deploy():
    with cd(env.path):
        run('git pull')
        run('source venv/bin/activate')
        run('pip3 install -r requirements.txt')
        run('python3 manage.py migrate --noinput')
        run('python3 manage.py collectstatic --noinput')
        run("echo 'admin123' | sudo -S systemctl restart gunicorn")
