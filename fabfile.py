from invoke import task
from invoke import run as local
import os


image_name = "cupen/zero:latest"
install_dir = "/data/zero/"


@task
def install(c):
    print("uploading docker-compose.yml")
    c.run(f"mkdir -p {install_dir}")
    c.put("docker-compose.yml", f"{install_dir}/docker-compose.yml")


@task
def start(c):
    # c.run(f"docker run -d -p 8787:8787 -p 8000:8000 --name zero -e webenv=prod {image_name}")
    print("starting container")
    with c.cd(install_dir):
        c.run("docker-compose up -d --remove-orphans")
        pass
    pass


@task
def restart(c):
    # c.run(f"docker run -d -p 8787:8787 -p 8000:8000 --name zero -e webenv=prod {image_name}")
    print("restarting container")
    with c.cd(install_dir):
        c.run("docker-compose pull zero")

        # FIXME: 未知问题，运行久了会崩掉，再启动 container 则会提示端口已占用。
        c.run("docker-compose rm -fs zero")
        c.run("docker-compose up -d --remove-orphans")
        # c.run("docker-compose restart zero")
        pass
    pass


@task
def check(c):
    c.run("curl https://zero.givemecolor.cc", pty=True, echo=True)
    print("")

    headers = "-H 'Connection: upgrade' -H 'Upgrade: websocket'"
    c.run(f"curl {headers} https://zero.givemecolor.cc" , pty=True, echo=True)
