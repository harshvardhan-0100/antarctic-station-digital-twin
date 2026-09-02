from simulation.state import StationState
from simulation.thermal import ThermalModel
from simulation.engine import SimulationEngine
from simulation.scenarios import antarctic_storm_scenario


def main():

    station = StationState(
        timestamp="2026-01-01 00:00",
        outside_temperature=-24.0,
        wind_speed=12.0,
        humidity=70.0
    )

    environments = antarctic_storm_scenario()

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

    print("\nANTARCTIC STORM SCENARIO")
    print("=" * 75)

    for state in history:
        print(
            f"{state.timestamp} | "
            f"Indoor: {state.indoor_temperature:6.2f} °C | "
            f"Thermal Demand: {state.thermal_demand_kw:7.2f} kW"
        )


if __name__ == "__main__":
    main()