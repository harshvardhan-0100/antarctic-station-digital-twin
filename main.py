from simulation.state import StationState
from simulation.environment import Environment
from simulation.thermal import ThermalModel
from simulation.engine import SimulationEngine


def main():

    # Initial station state
    station = StationState(
        timestamp="2026-01-01 00:00",
        outside_temperature=-25.0,
        wind_speed=18.0,
        humidity=70.0
    )

    # Environmental conditions over multiple timesteps
    environments = [
        Environment(
            timestamp="2026-01-01 00:00",
            temperature_c=-25.0,
            wind_speed_ms=18.0,
            humidity_percent=70.0,
            pressure_hpa=990.0
        ),

        Environment(
            timestamp="2026-01-01 01:00",
            temperature_c=-27.0,
            wind_speed_ms=20.0,
            humidity_percent=72.0,
            pressure_hpa=988.0
        ),

        Environment(
            timestamp="2026-01-01 02:00",
            temperature_c=-29.0,
            wind_speed_ms=23.0,
            humidity_percent=75.0,
            pressure_hpa=985.0
        ),

        Environment(
            timestamp="2026-01-01 03:00",
            temperature_c=-30.0,
            wind_speed_ms=25.0,
            humidity_percent=76.0,
            pressure_hpa=983.0
        ),

        Environment(
            timestamp="2026-01-01 04:00",
            temperature_c=-28.0,
            wind_speed_ms=22.0,
            humidity_percent=74.0,
            pressure_hpa=987.0
        ),
    ]

    thermal_model = ThermalModel()

    engine = SimulationEngine(
        thermal_model=thermal_model,
        time_step_hours=1.0
    )

    history = engine.run(
        station=station,
        environments=environments,
        heating_power_kw=30.0
    )

    print("\nSIMULATION RESULTS")
    print("=" * 60)

    for state in history:
        print(
            f"{state.timestamp} | "
            f"Indoor: {state.indoor_temperature:.2f} °C | "
            f"Thermal Demand: {state.thermal_demand_kw:.2f} kW"
        )


if __name__ == "__main__":
    main()