import prometheus_client as prom
import time
from google.cloud import monitoring_v3

class Gauge:
    """Gauge"""
    def __init__(self, name, desc, service):
        self.service = service
        if self.service == "prometheus":
            self.g = prom.Gauge(name, desc)
        else:
            metrics_descriptor = {
                    "type": custom_type,
                    "metricKind": "GAUGE",
                    "valueType": "INT64",
                    "unit": "items",
                    "description": desc,
                    "displayName": name
            }
            self.g = client.projects().metricDescriptors().create(
                     name=name, body=metrics_descriptor).execute() 
    def inc(self, v=1):
        self.g.inc(v)
    def dec(self, v=1):
        self.g.dec(v)
    def set(self, v):
        self.g.set(v)
    def get(self):
        self.g

class Histogram:
    """Prometheus histogram"""
    def __init__(self, name, desc, service, buckets=None):
        self.service = service
        if self.service == "prometheus":
            if buckets:
                self.h = prom.Histogram(name, desc, buckets=buckets)
            else:
                self.h = prom.Histogram(name, desc)
    def observe(self, v):
        return self.h.observe(v)

"""
class StackTimeSeries:
    def __init__(self, project_id, metric_type, v):
        client = monitoring_v3.MetricServiceClient()
        self.project = client.project_path(project_id)
        self.metric_type = "custom.googleapis.com/{}".format(metric_type)
        self.series = monitoring_v3.types.TimeSeries()
        self.series.metric.type = self.metric_type 
        point = self.series.points.add()
        point.value.double_value = v
        t = time.time()
        point.interval.end_time.seconds = int(t)
        point.interval.end_time.nanos = int((t - point.interval.end_time.seconds) * 10**9)
        client.create_time_series(project_id, [self.series])

    def addPoint(v, t):
        #Take value and time point and add to TimeSeries 
        point = self.series.points.add()
        point.value.double_value = v
        point.interval.end_time.seconds = int(t)
"""
