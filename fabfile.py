from invoke import task
from invoke import run as local
import os


image_name = "zero:latest"
dist_name = "zero.image.tar.gz"

@task
def deploy(c):
    upload(c)
    setup(c)
    start(c)


@task
def upload(c):
    local(f"docker save {image_name} | gzip > {dist_name}")
    c.put(dist_name, f"/data/")
    c.run(f"docker load --input /data/{dist_name}")


@task
def setup(c):
    pass


@task
def start(c):
    c.run("docker run -d -p 8787:8787 -p 8000:8000 zero:latest")


@task
def restart(c):
    c.run("docker restart zero")