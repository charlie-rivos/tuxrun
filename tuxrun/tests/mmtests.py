# vim: set ts=4
#
# Copyright 2023-present Linaro Limited
#
# SPDX-License-Identifier: MIT

from tuxrun.tests import Test


class MMTests(Test):
    devices = ["qemu-arm64", "qemu-x86_64"]
    config_file: str = ""
    # By default, we only archive the results JSON file
    full_archive: bool = False
    # Number of iterations to run the test, by default 10
    iterations: int = 10
    # Timeout in minutes
    timeout = 90
    need_test_definition = True

    @property
    def name(self):
        return self.config_file.replace("configs/config-", "mmtests-")

    def render(self, **kwargs):
        kwargs.update(
            {
                "name": self.name,
                "config_file": self.config_file,
                "full_archive": self.full_archive,
                "iterations": self.iterations,
                "timeout": self.timeout,
            }
        )
        return self._render("mmtests.yaml.jinja2", **kwargs)


class MMTestsDbSqliteInsertSmall(MMTests):
    config_file = "configs/config-db-sqlite-insert-small"


class MMTestsHpcScimarkcSmall(MMTests):
    config_file = "configs/config-hpc-scimarkc-small"
    iterations = 20


class MMTestsBlogbench(MMTests):
    config_file = "configs/config-io-blogbench"
    iterations = 30


class MMTestsFioRandreadAsyncRandwrite(MMTests):
    config_file = "configs/config-io-fio-randread-async-randwrite"


class MMTestsFioRandreadAsyncSeqwrite(MMTests):
    config_file = "configs/config-io-fio-randread-async-seqwrite"


class MMTestsFioRandreadSyncHeavywrite(MMTests):
    config_file = "configs/config-io-fio-randread-sync-heavywrite"


class MMTestsFioRandreadSyncRandwrite(MMTests):
    config_file = "configs/config-io-fio-randread-sync-randwrite"


class MMTestsFsmarkSmallFileStream(MMTests):
    config_file = "configs/config-io-fsmark-small-file-stream"


class MMTestsRedisBenchmarkSmall(MMTests):
    config_file = "configs/config-memdb-redis-benchmark-small"
    iterations = 20


class MMTestsRedisMemtierSmall(MMTests):
    config_file = "configs/config-memdb-redis-memtier-small"
    iterations = 20


class MMTestsSchbench(MMTests):
    config_file = "configs/config-scheduler-schbench"


class MMTestsSysbenchCpu(MMTests):
    config_file = "configs/config-scheduler-sysbench-cpu"


class MMTestsSysbenchThread(MMTests):
    config_file = "configs/config-scheduler-sysbench-thread"


class MMTestsAim9Disk(MMTests):
    config_file = "configs/config-workload-aim9-disk"


class MMTestsCoremark(MMTests):
    config_file = "configs/config-workload-coremark"
    iterations = 20


class MMTestsCyclictestFineHackbench(MMTests):
    config_file = "configs/config-workload-cyclictest-fine-hackbench"
    iterations = 15


class MMTestsCyclictestHackbench(MMTests):
    config_file = "configs/config-workload-cyclictest-hackbench"
    iterations = 20


class MMTestsEbizzy(MMTests):
    config_file = "configs/config-workload-ebizzy"
    timeout = 180


class MMTestsPmqtestHackbench(MMTests):
    config_file = "configs/config-workload-pmqtest-hackbench"


class MMTestsStressngAfAlg(MMTests):
    config_file = "configs/config-workload-stressng-af-alg"


class MMTestsStressngBadAltstack(MMTests):
    config_file = "configs/config-workload-stressng-bad-altstack"


class MMTestsStressngClassIoParallel(MMTests):
    config_file = "configs/config-workload-stressng-class-io-parallel"


class MMTestsStressngContext(MMTests):
    config_file = "configs/config-workload-stressng-context"


class MMTestsStressngFork(MMTests):
    config_file = "configs/config-workload-stressng-fork"


class MMTestsStressngGet(MMTests):
    config_file = "configs/config-workload-stressng-get"


class MMTestsStressngGetdent(MMTests):
    config_file = "configs/config-workload-stressng-getdent"


class MMTestsStressngMadvise(MMTests):
    config_file = "configs/config-workload-stressng-madvise"


class MMTestsStressngMmap(MMTests):
    config_file = "configs/config-workload-stressng-mmap"


class MMTestsStressngVmSplice(MMTests):
    config_file = "configs/config-workload-stressng-vm-splice"


class MMTestsStressngZombie(MMTests):
    config_file = "configs/config-workload-stressng-zombie"


class MMTestsUsemem(MMTests):
    config_file = "configs/config-workload-usemem"


class MMTestsScaleIoProcesses(MMTests):
    config_file = "configs/config-workload-will-it-scale-io-processes"


class MMTestsScaleIoThreads(MMTests):
    config_file = "configs/config-workload-will-it-scale-io-threads"


class MMTestsScalePfProcesses(MMTests):
    config_file = "configs/config-workload-will-it-scale-pf-processes"


class MMTestsScalePfThreads(MMTests):
    config_file = "configs/config-workload-will-it-scale-pf-threads"


class MMTestsScaleSysProcesses(MMTests):
    config_file = "configs/config-workload-will-it-scale-sys-processes"


class MMTestsScaleSysThreads(MMTests):
    config_file = "configs/config-workload-will-it-scale-sys-threads"
