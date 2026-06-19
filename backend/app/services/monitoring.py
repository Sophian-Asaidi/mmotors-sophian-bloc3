import logging
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field

logger = logging.getLogger("mmotors")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


@dataclass
class RuntimeMetrics:
    requests_total: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    errors_total: int = 0
    alert_total: int = 0
    durations: deque[float] = field(default_factory=lambda: deque(maxlen=200))

    def record_request(self, method: str, path: str, status_code: int, duration: float) -> None:
        key = f'{method}_{path}_{status_code}'.replace("/", "_").replace("-", "_").replace(".", "_")
        self.requests_total[key] += 1
        self.durations.append(duration)
        if status_code >= 500:
            self.errors_total += 1

    def trigger_alert(self, reason: str) -> dict[str, str | int]:
        self.alert_total += 1
        logger.warning("ALERT simulated reason=%s count=%s", reason, self.alert_total)
        return {"status": "alert_simulated", "reason": reason, "count": self.alert_total}

    def prometheus_text(self) -> str:
        lines = [
            "# HELP mmotors_requests_total Total HTTP requests grouped by route and status.",
            "# TYPE mmotors_requests_total counter",
        ]
        for key, value in sorted(self.requests_total.items()):
            lines.append(f'mmotors_requests_total{{route="{key}"}} {value}')
        lines.extend([
            "# HELP mmotors_errors_total Total server errors.",
            "# TYPE mmotors_errors_total counter",
            f"mmotors_errors_total {self.errors_total}",
            "# HELP mmotors_alerts_total Total simulated alerts.",
            "# TYPE mmotors_alerts_total counter",
            f"mmotors_alerts_total {self.alert_total}",
            "# HELP mmotors_request_duration_average_seconds Average request duration.",
            "# TYPE mmotors_request_duration_average_seconds gauge",
            f"mmotors_request_duration_average_seconds {self.average_duration():.6f}",
        ])
        return "\n".join(lines) + "\n"

    def average_duration(self) -> float:
        if not self.durations:
            return 0.0
        return sum(self.durations) / len(self.durations)


metrics = RuntimeMetrics()


def now() -> float:
    return time.perf_counter()
