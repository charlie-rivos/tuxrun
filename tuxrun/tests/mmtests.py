# vim: set ts=4
#
# Copyright 2023-present Linaro Limited
#
# SPDX-License-Identifier: MIT

from tuxrun.tests import Test


class MMTests(Test):
    devices = ["qemu-arm64", "qemu-x86_64"]
    configfile: str = ""
    full_archive: bool = False
    iterations: int = 10
    timeout = 90
    need_test_definition = True

    @property
    def name(self):
        return self.configfile.replace("configs/config-", "mmtests-")

    def render(self, **kwargs):
        kwargs.update(
            {
                "name": self.name,
                "configfile": self.configfile,
                "full_archive": self.full_archive,
                "iterations": self.iterations,
                "timeout": self.timeout,
            }
        )
        return self._render("mmtests.yaml.jinja2", **kwargs)


class MMTestsDbSqliteInsertSmall(MMTests):
    configfile = "configs/config-db-sqlite-insert-small"


class MMTestsHpcScimarkcSmall(MMTests):
    configfile = "configs/config-hpc-scimarkc-small"
    iterations = 20


class MMTestsBlogbench(MMTests):
    configfile = "configs/config-io-blogbench"
    iterations = 30


class MMTestsFioRandreadAsyncRandwrite(MMTests):
    configfile = "configs/config-io-fio-randread-async-randwrite"


class MMTestsFioRandreadAsyncSeqwrite(MMTests):
    configfile = "configs/config-io-fio-randread-async-seqwrite"


class MMTestsFioRandreadSyncHeavywrite(MMTests):
    configfile = "configs/config-io-fio-randread-sync-heavywrite"


class MMTestsFioRandreadSyncRandwrite(MMTests):
    configfile = "configs/config-io-fio-randread-sync-randwrite"


class MMTestsFsmarkSmallFileStream(MMTests):
    configfile = "configs/config-io-fsmark-small-file-stream"


class MMTestsRedisBenchmarkSmall(MMTests):
    configfile = "configs/config-memdb-redis-benchmark-small"
    iterations = 20


class MMTestsRedisMemtierSmall(MMTests):
    configfile = "configs/config-memdb-redis-memtier-small"
    iterations = 20


class MMTestsSchbench(MMTests):
    configfile = "configs/config-scheduler-schbench"


class MMTestsSysbenchCpu(MMTests):
    configfile = "configs/config-scheduler-sysbench-cpu"


class MMTestsSysbenchThread(MMTests):
    configfile = "configs/config-scheduler-sysbench-thread"


class MMTestsAim9Disk(MMTests):
    configfile = "configs/config-workload-aim9-disk"


class MMTestsCoremark(MMTests):
    configfile = "configs/config-workload-coremark"
    iterations = 20


class MMTestsCyclictestFineHackbench(MMTests):
    configfile = "configs/config-workload-cyclictest-fine-hackbench"
    iterations = 15


class MMTestsCyclictestHackbench(MMTests):
    configfile = "configs/config-workload-cyclictest-hackbench"
    iterations = 20


class MMTestsEbizzy(MMTests):
    configfile = "configs/config-workload-ebizzy"
    timeout = 180


class MMTestsPmqtestHackbench(MMTests):
    configfile = "configs/config-workload-pmqtest-hackbench"


class MMTestsStressngAfAlg(MMTests):
    configfile = "configs/config-workload-stressng-af-alg"


class MMTestsStressngBadAltstack(MMTests):
    configfile = "configs/config-workload-stressng-bad-altstack"


class MMTestsStressngClassIoParallel(MMTests):
    configfile = "configs/config-workload-stressng-class-io-parallel"


class MMTestsStressngContext(MMTests):
    configfile = "configs/config-workload-stressng-context"


class MMTestsStressngFork(MMTests):
    configfile = "configs/config-workload-stressng-fork"


class MMTestsStressngGet(MMTests):
    configfile = "configs/config-workload-stressng-get"


class MMTestsStressngGetdent(MMTests):
    configfile = "configs/config-workload-stressng-getdent"


class MMTestsStressngMadvise(MMTests):
    configfile = "configs/config-workload-stressng-madvise"


class MMTestsStressngMmap(MMTests):
    configfile = "configs/config-workload-stressng-mmap"


class MMTestsStressngVmSplice(MMTests):
    configfile = "configs/config-workload-stressng-vm-splice"


class MMTestsStressngZombie(MMTests):
    configfile = "configs/config-workload-stressng-zombie"


class MMTestsUsemem(MMTests):
    configfile = "configs/config-workload-usemem"


class MMTestsScaleIoProcesses(MMTests):
    configfile = "configs/config-workload-will-it-scale-io-processes"


class MMTestsScaleIoThreads(MMTests):
    configfile = "configs/config-workload-will-it-scale-io-threads"


class MMTestsScalePfProcesses(MMTests):
    configfile = "configs/config-workload-will-it-scale-pf-processes"


class MMTestsScalePfThreads(MMTests):
    configfile = "configs/config-workload-will-it-scale-pf-threads"


class MMTestsScaleSysProcesses(MMTests):
    configfile = "configs/config-workload-will-it-scale-sys-processes"


class MMTestsScaleSysThreads(MMTests):
    configfile = "configs/config-workload-will-it-scale-sys-threads"
