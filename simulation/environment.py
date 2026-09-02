from dataclasses import dataclass


@dataclass
class Environment:
    """
    Represents external environmental conditions surrounding
    the Antarctic research station at a given point in time.
    """

    timestamp: str

    # Atmospheric conditions
    temperature_c: float
    wind_speed_ms: float
    humidity_percent: float

    # Optional atmospheric condition
    pressure_hpa: float = 1013.25

    def __str__(self):
        return (
            "\n"
            "ENVIRONMENTAL CONDITIONS\n"
            "------------------------\n"
            f"Time:        {self.timestamp}\n"
            f"Temperature: {self.temperature_c:.1f} °C\n"
            f"Wind Speed:  {self.wind_speed_ms:.1f} m/s\n"
            f"Humidity:    {self.humidity_percent:.1f} %\n"
            f"Pressure:    {self.pressure_hpa:.1f} hPa"
        )