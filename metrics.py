import prometheus_client as prom
import time
from google.cloud import monitoring_v3

class PromCounter:
    """Prometheus counter"""
    def __init__(self, name, desc, labels):
        self.c = Counter(name, desc, labels)
    def inc(self, v=1):
        self.c.inc(v)

class PromGauge:
    """Prometheus gauge"""
    def __init__(self, name, desc):
        self.g = prom.Gauge(name, desc)
    def inc(self, v=1):
        return self.g.inc(v)
    def dec(self, v=1):
        return self.g.dec(v)
    def set(self, v):
        return self.g.set(v)

class PromHistogram:
    """Prometheus histogram"""
    def __init__(self, name, desc, labels):
        self.h = prom.Histogram(name, desc, labels)
    def observe(self, v):
        return self.h.observe(v)

#def create_stack_gauge(client, project_id, metric_type):

class StackGauge:
    def __init__(self, client, project_id, metric_type, metric_kind, name, desc):
        CUSTOM_METRIC_TYPE = "custom.googleapis.com/{}".format(metric_type)
        self.client = client
        metric_descriptor = {
                "type": metric_type,
                "labels": [
                    {
                        "key": "environment"
                        "valueType": STRING,
                        "description": desc
                    }
                ],
                "metricKind": metric_kind,
                "valueType": "INT64",
                "unit": "items",
                "description": desc,
                "displayName": name
        }
        client.projects().metricDescriptors().create(
                name=project_id, body=metrics_descriptor).execute()

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
        """ Take value and time point and add to TimeSeries """
        point = self.series.points.add()
        point.value.double_value = v
        point.interval.end_time.seconds = int(t)
