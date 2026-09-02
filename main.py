from simulation.state import StationState
from simulation.environment import Environment
from simulation.thermal import ThermalModel
from simulation.engine import SimulationEngine


def main():
    environment = Environment(
        timestamp="2026-01-01 00:00",
        temperature_c=-25.0,
        wind_speed_ms=18.0,
        humidity_percent=70.0,
        pressure_hpa=990.0
    )

    station = StationState(
        timestamp=environment.timestamp,
        outside_temperature=environment.temperature_c,
        wind_speed=environment.wind_speed_ms,
        humidity=environment.humidity_percent
    )

    thermal_model = ThermalModel()

    engine = SimulationEngine(
        thermal_model=thermal_model,
        time_step_hours=1.0
    )

    station = engine.step(
        station=station,
        environment=environment,
        heating_power_kw=30.0
    )

    print(environment)
    print(station)


if __name__ == "__main__":
    main()