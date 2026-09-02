from dataclasses import dataclass, field
from typing import List


@dataclass
class GeneratorState:
    """
    Represents the operational state of one CHP generator.
    """

    id: int
    is_running: bool = False
    load_kw: float = 0.0
    runtime_hours: float = 0.0

    def __str__(self):
        status = "RUNNING" if self.is_running else "OFF"

        return (
            f"CHP-{self.id}: {status} | "
            f"Load: {self.load_kw:.1f} kW | "
            f"Runtime: {self.runtime_hours:.1f} h"
        )


@dataclass
class StationState:
    """
    Represents the complete state of the Antarctic station
    at a particular point in simulated time.
    """

    # Time
    timestamp: str

    # Environmental state
    outside_temperature: float
    wind_speed: float
    humidity: float = 0.0

    # Building state
    indoor_temperature: float = 20.0

    # Energy demand
    electrical_demand_kw: float = 0.0
    thermal_demand_kw: float = 0.0

    # Fuel system
    fuel_level_liters: float = 300000.0

    # CHP generators
    generators: List[GeneratorState] = field(
        default_factory=lambda: [
            GeneratorState(id=1),
            GeneratorState(id=2),
            GeneratorState(id=3),
        ]
    )

    def __str__(self):
        generator_info = "\n".join(
            f"  {generator}" for generator in self.generators
        )

        return (
            "\n"
            "========================================\n"
            "      BHARATI STATION DIGITAL TWIN\n"
            "========================================\n"
            f"Time:                {self.timestamp}\n"
            "\n"
            "ENVIRONMENT\n"
            f"  Outside Temp:      {self.outside_temperature:.1f} °C\n"
            f"  Wind Speed:        {self.wind_speed:.1f} m/s\n"
            f"  Humidity:          {self.humidity:.1f} %\n"
            "\n"
            "STATION\n"
            f"  Indoor Temp:       {self.indoor_temperature:.1f} °C\n"
            f"  Electrical Demand: {self.electrical_demand_kw:.1f} kW\n"
            f"  Thermal Demand:    {self.thermal_demand_kw:.1f} kW\n"
            "\n"
            "FUEL\n"
            f"  Remaining:         {self.fuel_level_liters:,.0f} L\n"
            "\n"
            "CHP UNITS\n"
            f"{generator_info}\n"
            "========================================"
        )