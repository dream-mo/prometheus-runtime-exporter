import gc
import sys
import psutil
import time


class RuntimeMetric:

    def __init__(self, pid=None):
        if pid:
            self.process = psutil.Process(pid)
        else:
            self.process = psutil.Process()

    def getThreadCount(self) -> int:
        """
        获取当前线程数量
        :return:
        """
        return self.process.num_threads()

    def getGCThreshold(self) -> tuple:
        """
        获取分代内存要进行GC的频率阈值,默认700, 10,10
        第0代: 若>=700个对象, 则触发1次0代GC
        第1代: 若0代每触发10次,则1代触发1次GC
        第2代: 若1代每触发10次,则2代触发1次GC
        :return:
        """
        return gc.get_threshold()

    def getGCCount(self) -> tuple:
        """
        获取GC内存区域0、1、2代当前存在的对象数量
        :return:
        """
        return gc.get_count()

    def getGCStats(self) -> list:
        """
        获取GC内存区域0、1、2代的回收情况,例如:
        [{'collections': 14, 'collected': 31, 'uncollectable': 0}, {'collections': 1, 'collected': 71, 'uncollectable': 0}, {'collections': 0, 'collected': 0, 'uncollectable': 0}]
          【collections】: is the number of times this generation was collected
          【collected】: is the total number of objects collected inside this generation
          【uncollectable】: is the total number of objects which were found to be uncollectable
        :return:
        """
        return gc.get_stats()

    def getInterpreterVersion(self) -> str:
        """
        获取Python解释器版本号: 例如 3.9.6
        :return:
        """
        v = sys.version_info
        return f"{v.major}.{v.minor}.{v.micro}"

    def getInterpreterApiVersion(self) -> int:
        """
        获取Python解释器的API版本号: 例如 1013
        :return:
        """
        return int(sys.api_version)

    def getOsFileHandlerNum(self) -> int:
        """
        获取进程文件句柄数量
        :return:
        """
        if psutil.WINDOWS:
            num = self.process.num_handles()
        else:
            num = self.process.num_fds()
        return num

    def getCPUPercent(self, interval=1.0) -> float:
        """
        获取进程CPU使用率
        :param interval:
        :return:
        """
        return self.process.cpu_percent(interval=interval)

    def getCPUTimes(self) -> tuple:
        """
        获取进程CPU使用耗时(秒)
        :return:
        """
        t = self.process.cpu_times()
        return t.user, t.system,

    def getMemoryRSS(self) -> int:
        """
        获取进程占用的物理内存(字节数)
        :return:
        """
        print(self.process.memory_full_info())
        return self.process.memory_full_info().rss

    def getUpTime(self):
        """
        获取进程运行的时长(秒)
        :return:
        """
        start_time = self.process.create_time()
        current_time = time.time()
        runtime = current_time - start_time
        return runtime
