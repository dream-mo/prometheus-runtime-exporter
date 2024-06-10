from prometheus_client import Gauge, CollectorRegistry, generate_latest
from prometheus_runtime_exporter.runtime import RuntimeMetric


class RuntimeExporter:

    GENERATION = 3

    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(RuntimeExporter, cls).__new__(cls)
        return cls.__instance

    def __init__(self, namespace='app'):
        labels = ('pid', 'worker_role')
        self.registry = CollectorRegistry(auto_describe=False)

        self.thread_count = Gauge(name="thread_count", documentation="process thread count", labelnames=labels, namespace=namespace,
                                  registry=self.registry)
        self.gc_generation_object_count = Gauge(name="gc_generation_object_count", labelnames=labels + ("generation",),
                                                documentation="generation object count", namespace=namespace, registry=self.registry)
        self.gc_generation_threshold = Gauge(name="gc_generation_threshold", labelnames=("generation",),
                                             documentation="generation gc threshold", namespace=namespace, registry=self.registry)

        self.gc_collections_stats_count = Gauge(name="gc_collections_stats_count", labelnames=labels + ("generation",),
                                                documentation="collections stats count", namespace=namespace,
                                                registry=self.registry)
        self.gc_collected_stats_count = Gauge(name="gc_collected_stats_count",
                                              labelnames=labels + ("generation",),
                                              documentation="collected stats count", namespace=namespace,
                                              registry=self.registry)
        self.gc_uncollectable_stats_count = Gauge(name="gc_uncollectable_stats_count",
                                                  labelnames=labels + ("generation",),
                                                  documentation="uncollectable stats count", namespace=namespace,
                                                  registry=self.registry)

        self.python_version = Gauge(name="python_version", labelnames=("version",), documentation="python version",
                                    namespace=namespace, registry=self.registry)
        self.python_api_version = Gauge(name="python_api_version", labelnames=("version",),
                                        documentation="python api version", namespace=namespace,
                                        registry=self.registry)

        self.os_file_handles_num = Gauge(name="os_file_handles_num", labelnames=labels, documentation="process file "
                                                                                                      "handle count",
                                         namespace=namespace, registry=self.registry)
        self.os_cpu_used_percent = Gauge(name="os_cpu_used_percent", labelnames=labels, documentation="cpu usage "
                                                                                                      "percent",
                                         namespace=namespace, registry=self.registry)
        self.os_cpu_times = Gauge(name="os_cpu_times", labelnames=labels + ("role",),
                                  documentation="cpu time",
                                  namespace=namespace, registry=self.registry)
        self.os_mem_rss = Gauge(name="os_mem_rss", labelnames=labels, documentation="memory rss bytes", namespace=namespace,
                                registry=self.registry)
        self.os_uptime = Gauge(name="os_uptime", documentation="process updatime", labelnames=labels, namespace=namespace,
                               registry=self.registry)

    def update(self, pid, worker_role):
        metric = RuntimeMetric(pid)
        self.thread_count.labels(pid=pid, worker_role=worker_role).set(metric.getThreadCount())
        generation_object_counts = metric.getGCCount()
        for g in range(self.GENERATION):
            self.gc_generation_object_count.labels(pid=pid, generation=g, worker_role=worker_role).set(
                generation_object_counts[g])
        gc_generation_thresholds = metric.getGCThreshold()
        for g in range(self.GENERATION):
            self.gc_generation_threshold.labels(generation=g).set(gc_generation_thresholds[g])
        gc_collections_stats = metric.getGCStats()
        for g in range(self.GENERATION):
            self.gc_collections_stats_count.labels(pid=pid, generation=g, worker_role=worker_role).set(
                gc_collections_stats[g]['collections'])
            self.gc_collected_stats_count.labels(pid=pid, generation=g, worker_role=worker_role).set(
                gc_collections_stats[g]['collected'])
            self.gc_uncollectable_stats_count.labels(pid=pid, generation=g, worker_role=worker_role).set(
                gc_collections_stats[g]['uncollectable'])
        self.python_version.labels(version=metric.getInterpreterVersion())
        self.python_api_version.labels(version=metric.getInterpreterApiVersion()).set(1)
        self.os_file_handles_num.labels(pid=pid, worker_role=worker_role).set(metric.getOsFileHandlerNum())
        self.os_cpu_used_percent.labels(pid=pid, worker_role=worker_role).set(metric.getCPUPercent())
        cpu_times = metric.getCPUTimes()
        self.os_cpu_times.labels(pid=pid, worker_role=worker_role, role="user").set(cpu_times[0] * 1000 * 1000 * 1000)
        self.os_cpu_times.labels(pid=pid, worker_role=worker_role, role="system").set(cpu_times[1] * 1000 * 1000 * 1000)
        self.os_mem_rss.labels(pid=pid, worker_role=worker_role).set(metric.getMemoryRSS())
        self.os_uptime.labels(pid=pid, worker_role=worker_role).set(metric.getUpTime())

    def getRegistry(self):
        return self.registry

    def getMetricsContent(self):
        return generate_latest(self.registry)
