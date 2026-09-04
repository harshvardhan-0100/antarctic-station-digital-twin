from simulation.state import StationState
from simulation.thermal import ThermalModel
from simulation.controller import ThermalController
from simulation.electrical import ElectricalModel
from simulation.engine import SimulationEngine
from simulation.scenarios import antarctic_storm_scenario


def main():

    # -------------------------------------------------
    # INITIAL STATION STATE
    # -------------------------------------------------

    station = StationState(
        timestamp="2026-01-01 00:00",
        outside_temperature=-24.0,
        wind_speed=12.0,
        humidity=70.0
    )

    # -------------------------------------------------
    # ENVIRONMENTAL SCENARIO
    # -------------------------------------------------

    environments = antarctic_storm_scenario()

    # -------------------------------------------------
    # PHYSICAL MODELS
    # -------------------------------------------------

    thermal_model = ThermalModel()

    electrical_model = ElectricalModel()

    thermal_controller = ThermalController(
        target_temperature=20.0,
        max_heating_power_kw=150.0,
        proportional_gain=8.0
    )

    # -------------------------------------------------
    # SIMULATION ENGINE
    # -------------------------------------------------

    engine = SimulationEngine(
        thermal_model=thermal_model,
        electrical_model=electrical_model,
        thermal_controller=thermal_controller,
        time_step_hours=1.0
    )

    # -------------------------------------------------
    # RUN SIMULATION
    # -------------------------------------------------

    history = engine.run(
        station=station,
        environments=environments
    )

    # -------------------------------------------------
    # DISPLAY RESULTS
    # -------------------------------------------------

    print("\nANTARCTIC STORM - ENERGY SIMULATION")
    print("=" * 95)

    for state in history:

        print(
            f"{state.timestamp} | "
            f"Indoor: {state.indoor_temperature:5.2f} °C | "
            f"Thermal: {state.thermal_demand_kw:6.2f} kW | "
            f"Electrical: {state.electrical_demand_kw:6.2f} kW"
        )


if __name__ == "__main__":
    main()