from invoke import task
from invoke import run as local
import os


image_name = "zero:latest"
remote_image_name = f"cupen/{image_name}"


@task
def deploy(c):
    start(c)


@task
def start(c):
    c.run(f"docker run -d -p 8787:8787 -p 8000:8000 --name zero -e webenv=prod {remote_image_name}")


@task
def full_restart(c):
    c.run(f"docker stop zero")
    c.run(f"docker rm zero")
    c.run(f"docker pull {remote_image_name}")
    start(c)
