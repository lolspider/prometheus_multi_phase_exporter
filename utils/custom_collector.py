from prometheus_client.core import GaugeMetricFamily


class CustomCollector(object):
    def __init__(self, metric_name, doc, labels, status):
        self._metric_name = metric_name
        self._doc = doc
        self._labels = labels
        self._status = status

    def collect(self):
        g = GaugeMetricFamily(self._metric_name, self._doc, labels=self._labels)
        for i, j in self._status.items():
            g.add_metric([i], j)
        yield g