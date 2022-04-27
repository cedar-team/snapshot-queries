import datetime


class TimeDelta(datetime.timedelta):
    def __add__(self, other):
        result = super().__add__(other)
        return TimeDelta.from_python_timedelta(result)

    def __str__(self):
        return self.humanize()

    @classmethod
    def from_python_timedelta(cls, delta: datetime.timedelta) -> "TimeDelta":
        return cls(seconds=delta.total_seconds())

    def humanize(self) -> str:
        """Return a natural description of this TimeDelta."""

        if self.total_milliseconds() < 1:
            return "< 1 ms"

        for unit, val in (
            ("h", self.total_hours()),
            ("m", self.total_minutes()),
            ("s", self.total_seconds()),
        ):
            if (val > 1.5 or (val >= 1 and unit == "s")) and val < 10:
                return f"{val:1.2f} {unit}"  # e.g. '2.21 s'
            elif 10 <= val < 100:
                return f"{val:2.1f} {unit}"  # e.g. '22.1 m'
            elif 100 <= val < 1000:
                return f" {val:3.0f} {unit}"  # e.g. ' 221 h'
            elif val >= 1000:
                return f" >1k {unit}"  # e.g. '> 1k h'

        return f"{int(self.total_milliseconds())} ms"

    def total_hours(self) -> float:
        return self.total_seconds() / 3600

    def total_milliseconds(self) -> float:
        return self.total_seconds() * 1000

    def total_minutes(self) -> float:
        return self.total_seconds() / 60
