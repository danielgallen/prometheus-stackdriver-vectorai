import prometheus_client as prom
import time
from google.cloud import monitoring_v3

class Gauge:
    """Gauge"""
    def __init__(self, name, desc, service, metric_type=None):
        """ Create the gauge metric """
        self.service = service
        if self.service == "prometheus":
            self.g = prom.Gauge(name, desc)
            print('Prometheus Created {}.'.format(name))
        else:
            # STACKDRIVER
            self.client = monitoring_v3.MetricServiceClient()
            self.project_name = self.client.project_path(name)
            descriptor = monitoring_v3.types.MetricDescriptor()
            descriptor.type = 'custom.googleapis.com/{}'.format(metric_type)
            # Gauge
            descriptor.metric_kind = (
                    monitoring_v3.enums.MetricDescriptor.MetricKind.GAUGE)
            # Double type (Will add switch for types later)
            descriptor.value_type = (
                    monitoring_v3.enums.MetricDescriptor.ValueType.DOUBLE)
            descriptor.description = desc
            
            # Create the metric descriptor and print a success message
            descriptor = self.client.create_metric_descriptor(self.project_name, descriptor)
            print('StackDriver Created {}.'.format(descriptor.name))

    def inc(self, v=1):
        self.g.inc(v)

    def dec(self, v=1):
        self.g.dec(v)

    def set(self, v):
        if self.service == "prometheus":
            self.g.set(v)
        else:
            # STACKDRIVER
            # Can only write maximum of one point call per minute for an individual time series
            point = self.g.points.add()
            point.value.double_value = v
            now = time.time()
            point.interval.end_time.seconds = int(now)
            point.interval.end_time.nanos = int(
                    (now - point.interval.end_time.seconds) * 10 ** 9)
            
            self.client.create_time_series(project_name, [self.g])

    def delete(self):
        """ Delete the metric """
        if self.service == "prometheus":
        else:
            self.client.delete_metric_descriptor(self.name)

class Histogram:
    """Histogram"""
    def __init__(self, name, desc, service, buckets=None, client=None, valueType=None):
        self.service = service
        self.name = name
        if self.service == "prometheus":
            if buckets:
                self.h = prom.Histogram(name, desc, buckets=buckets)
            else:
                self.h = prom.Histogram(name, desc)
        else:
            metrics_descriptor = {
                    "type": custom_type,
                    "name": name,
                    "metric_type": metric_type,
                    "metricKind": "CUMULATIVE",
                    "valueType": "DISTRIBUTION",
                    "description": desc
            }
            self.h = client.projects().metricDescriptors().create(
                     name=name, body=metrics_descriptor).execute()
    def observe(self, v):
        self.h.observe(v)
    def write(self, v):
        if self.service == "prometheus":
            return
        else:
            point = self.h.points.add()
            point.value.
    def delete(self):
        if self.service == "prometheus":

        else:
            self.client.delete_metric_descriptor(self.name)
