# Collectors Base Classes

Base classes and utilities for Prometheus-style metrics collection.

## Summary

- [`MetricValue`](#metricvalue) — Container for a single metric value with labels
- [`Metric`](#metric) — Single metric with type, labels, and multiple values
- [`BaseCollector`](#basecollector) — Base class for implementing metric collectors
- [`labels_to_string()`](#labels_to_string) — Utility for converting label dict to Prometheus format

## Reference

### `MetricValue`

Container holding a single metric value and its associated labels.

**Attributes:**

- `labels` (dict[str, str]): Label key-value pairs (e.g., `{"endpoint": "issues"}`)
- `value` (float | int): The numeric metric value

**Properties:**

- `labels_string` (str, read-only): Returns labels formatted as Prometheus string (e.g., `{endpoint="issues"}`), or empty string if no labels

---

### `Metric`

Prometheus-format metric with type, name, help string, and labeled values.

**Class Attributes:**

- `Types` (Enum): Metric type enumeration with values:
  - `COUNTER` — monotonically increasing counter ("counter")
  - `GAUGE` — value that can go up or down ("gauge")

**Constructor:**

- `__init__(name: str, metric_type: Types = "gauge", help_string: str = "")`
  - `name`: Metric identifier (e.g., "read_comics_db_count")
  - `metric_type`: Counter or Gauge (default: Gauge)
  - `help_string`: Human-readable description for Prometheus

**Attributes:**

- `_name` (str): Metric name (read-only via property)
- `_values` (dict): Map of `{labels_string → MetricValue}`
- `metric_type` (Metric.Types): Metric type
- `help_string` (str): Description

**Properties:**

- `name` (str, read-only): Returns metric name; setter raises AttributeError

**Methods:**

- `set_value(labels: dict[str, str], value: float | int) → None`
  - Sets or overwrites value for given labels
  - Raises KeyError if value doesn't exist for get operations

- `get_value(labels: dict[str, str]) → int | float`
  - Retrieves current value for given labels
  - Raises KeyError if not found

- `increment_value(labels: dict[str, str], increment: float | int = 1) → None`
  - Adds increment to current value
  - Raises KeyError if value doesn't exist

- `decrement_value(labels: dict[str, str], decrement: float | int = 1, timestamp: float | None = None) → None`
  - Subtracts decrement from current value
  - `timestamp`: Optional Prometheus timestamp (unused in current implementation)

- `to_string(timestamp: float | None = None) → str`
  - Returns metric in Prometheus text format
  - Includes HELP, TYPE, and all labeled values
  - Format: `metric_name{labels} value timestamp`

**Usage Example:**

```python
metric = Metric("requests_total", Metric.Types.COUNTER, "Total HTTP requests")
metric.set_value({"endpoint": "/api/issues"}, 100)
metric.increment_value({"endpoint": "/api/issues"}, 5)
print(metric.to_string())
# Output:
# # HELP requests_total Total HTTP requests
# # TYPE requests_total counter
# requests_total{endpoint="/api/issues"} 105 <timestamp>
```

---

### `BaseCollector`

Abstract base class for implementing metric collectors. Subclasses override `collect()` to gather metrics from various sources.

**Constructor:**

- `__init__()`
  - Initializes empty `_metrics` dictionary

**Protected Methods:**

- `_register_metric(name: str, metric_type: Metric.Types = Metric.Types.GAUGE, help_string: str = "") → None`
  - Creates and registers a new metric
  - Raises KeyError if metric already registered with same name

- `_unregister_metric(name: str) → None`
  - Removes metric from registry (no error if not found)

- `_get_metric(name: str) → Metric`
  - Retrieves registered metric by name
  - Raises KeyError if not found

- `_set_metric(name: str, labels: dict[str, str], value: float | int) → None`
  - Sets value for labeled metric
  - Requires metric to be registered first

- `_increment_metric(name: str, labels: dict[str, str], increment: float | int = 1) → None`
  - Increments labeled metric value
  - Requires metric to be registered first

- `_decrement_metric(name: str, labels: dict[str, str], decrement: float | int = 1) → None`
  - Decrements labeled metric value
  - Requires metric to be registered first

**Public Methods:**

- `report() → str`
  - Returns all metrics in Prometheus text format
  - Timestamp: Unix milliseconds from `timezone.now()`

- `collect() → None`
  - Abstract method to be implemented by subclasses
  - Should call `_register_metric()` and `_set_metric()` to populate metrics
  - Raises NotImplementedError if not overridden

---

### `labels_to_string()`

Utility function converting label dictionary to Prometheus label format.

**Signature:**

```python
def labels_to_string(labels: dict[str, str]) -> str
```

**Parameters:**

- `labels` (dict[str, str]): Label key-value pairs

**Returns:**

- String in format `{key1="value1",key2="value2"}` (sorted by key)
- Empty string `""` if labels dict is empty
- Escapes special characters in values: `\` → `\\`, `"` → `\"`, newline → `\n`

**Example:**

```python
labels_to_string({"table": "issues", "status": "matched"})
# Returns: '{status="matched",table="issues"}'  (sorted by key)
```

---

## Implementation Pattern

Subclasses typically follow this pattern:

```python
class MyCollector(BaseCollector):
    def collect(self):
        # Register metrics with metadata
        self._register_metric("metric_name", help_string="Description")

        # Gather data and set values
        for item in data_source:
            self._set_metric("metric_name", {"label": "value"}, count)

        # Increment totals
        self._increment_metric("metric_name", {"label": "total"}, increment)
```

See [`DBCollector`](db.md#dbcollector), [`MongoCollector`](mongo.md#mongocollector), and [`ApiQueueCollector`](api_queue.md#apiqueuecollector) for concrete examples.