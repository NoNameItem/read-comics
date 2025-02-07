from enum import Enum
from math import floor

from django.utils import timezone


def labels_to_string(labels: dict[str, str]) -> str:
    def _escape_label_value(label: str) -> str:
        return label.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")

    return (
        "{" + ",".join([f'{k}="{_escape_label_value(v)}"' for k, v in sorted(labels.items(), key=lambda x: x[0])]) + "}"
    )


class MetricValue:
    def __init__(
        self,
        labels: dict[str, str],
        value: float | int,
    ):
        self.labels = labels
        self.value = value

    @property
    def labels_string(self) -> str:
        if self.labels:
            return labels_to_string(self.labels)
        return ""


class Metric:
    class Types(Enum):
        COUNTER = "counter"
        GAUGE = "gauge"

    def __init__(self, name: str, metric_type: Types = "gauge", help_string: str = ""):
        self._name: str = name
        self._values: {str, MetricValue} = {}
        self.metric_type: Metric.Types = metric_type
        self.help_string: str = help_string

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        raise AttributeError("Metric name cannot be changed")

    def set_value(self, labels: dict[str, str], value) -> None:
        self._values[labels_to_string(labels)] = MetricValue(labels, value)

    def get_value(self, labels: dict[str, str]) -> int | float:
        if labels_to_string(labels) in self._values:
            return self._values[labels_to_string(labels)].value
        raise KeyError(f"No value found for label {labels_to_string(labels)}")

    def increment_value(
        self,
        labels: dict[str, str],
        increment: float | int = 1,
    ) -> None:
        current_value = self.get_value(labels)
        self._values[labels_to_string(labels)] = MetricValue(labels, current_value + increment)

    def decrement_value(
        self, labels: dict[str, str], decrement: float | int = 1, timestamp: float | None = None
    ) -> None:
        current_value = self.get_value(labels)
        self._values[labels_to_string(labels)] = MetricValue(labels, current_value - decrement)

    def to_string(self, timestamp: float | None = None) -> str:
        result = ""

        if self.help_string:
            result += f"# HELP {self.help_string}\n"

        result += f"# TYPE {self.name} {self.metric_type.value}\n"

        for value in self._values.values():
            result += f"{self.name}{value.labels_string} {value.value} {timestamp}\n"

        return result + "\n"


class BaseCollector:
    def __init__(self):
        self._metrics: dict[str, Metric] = {}

    def _register_metric(self, name: str, metric_type: Metric.Types = Metric.Types.GAUGE, help_string: str = ""):
        if name in self._metrics:
            raise KeyError(f"Metric `{name}` already registered")

        self._metrics[name] = Metric(name, metric_type, help_string)

    def _unregister_metric(self, name: str):
        if name in self._metrics:
            del self._metrics[name]

    def _get_metric(self, name: str) -> Metric:
        if name not in self._metrics:
            raise KeyError(f"Metric `{name}` not registered")
        return self._metrics[name]

    def _set_metric(self, name: str, labels: dict[str, str], value: float | int) -> None:
        metric = self._get_metric(name)
        metric.set_value(labels, value)

    def _increment_metric(self, name: str, labels: dict[str, str], increment: float | int = 1) -> None:
        metric = self._get_metric(name)
        metric.increment_value(labels, increment)

    def _decrement_metric(self, name: str, labels: dict[str, str], decrement: float | int = 1) -> None:
        metric = self._get_metric(name)
        metric.decrement_value(labels, decrement)

    def report(self):
        timestamp = floor(timezone.now().timestamp() * 1000)
        result = ""
        for metric in self._metrics.values():
            result += metric.to_string(timestamp)

        return result

    def collect(self):
        raise NotImplementedError()
