# vim: set ts=4
#
# Copyright 2024-present Linaro Limited
#
# SPDX-License-Identifier: MIT

from tuxrun.tests import Test


class RTTests(Test):
    devices = ["fvp-aemva", "qemu-arm64", "qemu-x86_64"]
    name = "rt-tests"
    timeout = 15
    need_test_definition = True

    def render(self, **kwargs):
        kwargs["subname"] = self.subname
        kwargs["name"] = self.name
        kwargs["timeout"] = self.timeout

        return self._render("rt-tests.yaml.jinja2", **kwargs)


class RTTestsHackbench(RTTests):
    subname = "hackbench"
    name = f"rt-tests-{subname}"
    timeout = 20


class RTTestsPmqtest(RTTests):
    subname = "pmqtest"
    name = f"rt-tests-{subname}"
    timeout = 10


class RTTestsPiStress(RTTests):
    subname = "pi-stress"
    name = f"rt-tests-{subname}"
    timeout = 10
