from pathlib import Path

import pytest

from tuxrun.runtimes import DockerRuntime, NullRuntime, PodmanRuntime, Runtime
from tuxmake.exceptions import RuntimeNotFoundError


def test_select():
    assert Runtime.select("docker") == DockerRuntime
    assert Runtime.select("null") == NullRuntime
    assert Runtime.select("podman") == PodmanRuntime


def test_image():
    runtime = Runtime.select("docker")()
    runtime.image("test")
    assert runtime._runtime.get_image() == "test"


def test_prepare(mocker):
    runtime = Runtime.select("docker")()
    runtime.image("test_image")
    runtime.network = "test_network"
    mocker.patch.object(runtime._runtime, "prepare")
    runtime.prepare("writer_obj", "results_obj")
    assert runtime.writer == "writer_obj"
    assert runtime.results == "results_obj"
    assert runtime._runtime.get_image() == "test_image"
    assert runtime._runtime.network == "test_network"


def test_cleanup(mocker):
    runtime = Runtime.select("podman")()
    runtime.container_id = "test_id"
    cleanup_mock = mocker.patch.object(runtime._runtime, "cleanup")
    assert runtime._runtime.name == "podman"
    runtime.cleanup()
    assert runtime._runtime is None
    assert cleanup_mock.call_count == 1


def test_add_bindings(mocker):
    runtime = Runtime.select("docker")()
    vol_mock = mocker.patch.object(runtime._runtime, "add_volume")
    bindings = runtime.__bindings__
    for item in [
        ("/boot", "/boot", True, False),
        ("/lib/modules", "/lib/modules", True, False),
    ]:
        assert item in bindings
    if Path("/dev/kvm").exists():
        assert ("/dev/kvm", "/dev/kvm", False, True) in bindings
    # case: with ro=True
    bind = "/test/bind"
    runtime.bind(bind, ro=True)
    runtime.add_bindings()
    assert (bind, bind, True, False) in bindings
    assert vol_mock.call_count == len(bindings)

    # case: Exception with duplicated binding
    runtime.bind(bind, device=True)
    with pytest.raises(Exception):
        runtime.add_bindings()


def test_podman_not_installed(mocker):
    mocker.patch("subprocess.Popen", side_effect=FileNotFoundError)
    runtime = Runtime.select("podman")()
    with pytest.raises(RuntimeNotFoundError) as e:
        runtime.prepare(None, None)
    assert "Runtime not installed: podman" in str(e.value)


def test_docker_not_installed(mocker):
    mocker.patch("subprocess.Popen", side_effect=FileNotFoundError)
    runtime = Runtime.select("docker")()
    with pytest.raises(RuntimeNotFoundError) as e:
        runtime.prepare(None, None)
    assert "Runtime not installed: docker" in str(e.value)


def test_pre_run_docker(tmp_path):
    runtime = Runtime.select("docker")()
    runtime.pre_run(tmp_path)
    assert runtime.__bindings__[-1] == (
        "/var/run/docker.sock",
        "/var/run/docker.sock",
        False,
        False,
    )


def test_pre_run_null():
    runtime = Runtime.select("null")()
    runtime.pre_run(None)


def test_pre_run_podman(mocker, tmp_path):
    (tmp_path / "podman.sock").touch()
    popen = mocker.patch("subprocess.Popen")
    run = mocker.patch("subprocess.run")

    runtime = Runtime.select("podman")()
    runtime.pre_run(tmp_path)
    assert runtime.__pre_proc__ is not None
    popen.assert_called_once()
    run.assert_called_once()


def test_pre_run_podman_errors(mocker, tmp_path):
    popen = mocker.patch("subprocess.Popen")
    run = mocker.patch("subprocess.run")
    sleep = mocker.patch("time.sleep")

    runtime = Runtime.select("podman")()
    with pytest.raises(Exception) as exc:
        runtime.pre_run(tmp_path)
    assert exc.match("Unable to create podman socket at ")
    assert exc.match("podman.sock")
    popen.assert_called_once()
    run.assert_called_once()
    sleep.assert_called()


def test_post_run_null():
    runtime = Runtime.select("null")()
    runtime.post_run()


def test_post_run_podman(mocker):
    runtime = Runtime.select("podman")()
    runtime.post_run()

    runtime.__pre_proc__ = mocker.MagicMock()
    runtime.post_run()
    runtime.__pre_proc__.kill.assert_called_once_with()
    runtime.__pre_proc__.wait.assert_called_once_with()


def test_run(mocker):
    popen = mocker.patch("subprocess.Popen")

    runtime = Runtime.select("podman")()
    runtime.image("image")
    runtime.run(["hello", "world"])
    popen.assert_called_once()


def test_run_errors(mocker):
    popen = mocker.patch("subprocess.Popen", side_effect=FileNotFoundError)

    runtime = Runtime.select("podman")()
    runtime.image("image")
    with pytest.raises(FileNotFoundError):
        with runtime.run(["hello", "world"]):
            pass
    popen.assert_called_once()

    popen = mocker.patch("subprocess.Popen", side_effect=Exception)
    runtime = Runtime.select("podman")()
    runtime.image("image")
    with pytest.raises(Exception):
        with runtime.run(["hello", "world"]):
            pass
    popen.assert_called_once()

    # Test duplicated source bindings
    popen = mocker.patch("subprocess.Popen", side_effect=FileNotFoundError)

    runtime = Runtime.select("podman")()
    runtime.image("image")
    runtime.bind("/hello", "/world")
    runtime.bind("/hello", "/world2")
    with pytest.raises(Exception) as exc:
        runtime.add_bindings()
    assert exc.match("Duplicated mount source '/hello'")
    popen.assert_not_called()

    # Test duplicated destination bindings
    runtime = Runtime.select("podman")()
    runtime.image("image")
    runtime.bind("/hello", "/world")
    runtime.bind("/hello2", "/world")
    with pytest.raises(Exception) as exc:
        runtime.add_bindings()
    assert exc.match("Duplicated mount destination '/world'")
    popen.assert_not_called()
