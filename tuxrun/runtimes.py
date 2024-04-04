# vim: set ts=4
#
# Copyright 2021-present Linaro Limited
#
# SPDX-License-Identifier: MIT

import logging
import os
import subprocess
import sys
import time
from pathlib import Path

from tuxrun.templates import wrappers

# Tuxmake Runtime
from tuxmake.runtime import Runtime as TuxmakeRuntime

BASE = (Path(__file__) / "..").resolve()
LOG = logging.getLogger("tuxrun")


def run_hacking_sesson(definition, case, test):
    if definition == "hacking-session" and case == "tmate" and "reference" in test:
        if sys.stdout.isatty():
            subprocess.Popen(
                [
                    "xterm",
                    "-e",
                    "bash",
                    "-c",
                    f"ssh {test['reference']}",
                ]
            )


class Runtime:
    binary = ""
    container = False
    network = None

    def __init__(self):
        self._runtime = TuxmakeRuntime.get(self.binary)
        self.__bindings__ = []
        self.__pre_proc__ = None
        self.writer = None
        self.results = None
        self.network = None
        self.hacking_session = False

    @classmethod
    def select(cls, name):
        if name == "docker":
            return DockerRuntime
        if name == "podman":
            return PodmanRuntime
        return NullRuntime

    def bind(self, src, dst=None, ro=False, device=False):
        if dst is None:
            dst = src
        self.__bindings__.append((str(src), dst, ro, device))

    def image(self, image):
        self._runtime.set_image(image)

    def pre_run(self, tmpdir):
        pass

    def post_run(self):
        pass

    def add_bindings(self):
        raise NotImplementedError()  # pragma: no cover

    def logger(self, line):
        if line:
            self.writer.write(line)
            res = self.results.parse(line)
            # Start an xterm if an hacking session url is available
            if self.hacking_session and res:
                run_hacking_sesson(*res)

    def run(self, args, logger=None):
        LOG.debug("Calling %s", " ".join(args))
        return self._runtime.run_cmd(args, offline=False, logger=logger, echo=False)

    def prepare(self, writer, results, hacking_session=False):
        self.writer = writer
        self.results = results
        self.hacking_session = hacking_session

        self._runtime.network = self.network
        self._runtime.allow_user_opts = False
        self._runtime.prepare()

    def cleanup(self):
        if self._runtime:
            self._runtime.cleanup()
            self._runtime = None


class ContainerRuntime(Runtime):
    bind_guestfs = True
    container = True

    def __init__(self):
        super().__init__()
        self.bind("/boot", ro=True)
        self.bind("/lib/modules", ro=True)
        # Bind /dev/kvm is available
        if Path("/dev/kvm").exists():
            self.bind("/dev/kvm", device=True)
        # Create /var/tmp/.guestfs-$id
        if self.bind_guestfs:
            guestfs = Path(f"/var/tmp/.guestfs-{os.getuid()}")
            guestfs.mkdir(exist_ok=True)
            self.bind(guestfs, "/var/tmp/.guestfs-0")

    def add_bindings(self):
        srcs = set()
        dsts = set()
        for binding in self.__bindings__:
            (src, dst, ro, device) = binding
            if src in srcs:
                LOG.error("Duplicated mount source %r", src)
                raise Exception("Duplicated mount source %r" % src)
            if dst in dsts:
                LOG.error("Duplicated mount destination %r", dst)
                raise Exception("Duplicated mount destination %r" % dst)
            srcs.add(src)
            dsts.add(dst)
            self._runtime.add_volume(src, dst, ro=ro, device=device)


class DockerRuntime(ContainerRuntime):
    # Do not bind or libguestfs will fail at runtime
    # "security: cached appliance /var/tmp/.guestfs-0 is not owned by UID 0"
    bind_guestfs = False
    binary = "docker"

    def pre_run(self, tmpdir):
        # Render and bind the docker wrapper
        wrap = (
            wrappers()
            .get_template("docker.jinja2")
            .render(runtime="docker", volume=str(tmpdir / "dispatcher" / "tmp"))
        )
        LOG.debug("docker wrapper")
        LOG.debug(wrap)
        (tmpdir / "docker").write_text(wrap, encoding="utf-8")
        (tmpdir / "docker").chmod(0o755)
        self.bind(str(tmpdir / "docker"), "/usr/local/bin/docker", True)

        # Bind the docker socket
        self.bind("/var/run/docker.sock")


class PodmanRuntime(ContainerRuntime):
    binary = "podman"
    network = None

    def pre_run(self, tmpdir):
        # Render and bind the docker wrapper
        self.network = os.path.basename(tmpdir)
        subprocess.run(["podman", "network", "create", self.network])
        wrap = (
            wrappers()
            .get_template("docker.jinja2")
            .render(
                runtime="podman",
                volume=str(tmpdir / "dispatcher" / "tmp"),
                network=self.network,
            )
        )
        LOG.debug("docker wrapper")
        LOG.debug(wrap)
        (tmpdir / "docker").write_text(wrap, encoding="utf-8")
        (tmpdir / "docker").chmod(0o755)
        self.bind(str(tmpdir / "docker"), "/usr/local/bin/docker", True)

        # Start podman system service and bind the socket
        socket = tmpdir / "podman.sock"
        self.bind(socket, "/run/podman/podman.sock")

        args = [
            self.binary,
            "system",
            "service",
            "--time",
            "0",
            f"unix://{socket}",
        ]
        self.__pre_proc__ = subprocess.Popen(
            args,
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            preexec_fn=os.setpgrp,
        )
        # wait for the socket
        for _ in range(60):
            if socket.exists():
                return
            time.sleep(1)
        raise Exception(f"Unable to create podman socket at {socket}")

    def post_run(self):
        if self.network:
            subprocess.call([self.binary, "network", "rm", self.network])
        if self.__pre_proc__ is None:
            return
        self.__pre_proc__.kill()
        self.__pre_proc__.wait()


class NullRuntime(Runtime):
    def add_bindings(self):
        pass
