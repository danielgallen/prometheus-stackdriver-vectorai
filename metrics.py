import prometheus_client as prom
import time
from google.cloud import monitoring_v3

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
    def __init__(self, name, desc):
        self.h = prom.Histogram(name, desc)
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
