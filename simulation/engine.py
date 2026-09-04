from copy import deepcopy

from simulation.state import StationState
from simulation.environment import Environment
from simulation.thermal import ThermalModel
from simulation.controller import ThermalController
from simulation.electrical import ElectricalModel


class SimulationEngine:
    """
    Coordinates the physical models and advances
    the Antarctic station Digital Twin through time.

    Current responsibilities:
    - Environmental state synchronization
    - Thermal demand calculation
    - Adaptive thermal control
    - Indoor temperature dynamics
    - Electrical load calculation
    - Simulation history management

    Future extensions:
    - CHP generator dispatch
    - Fuel consumption
    - Energy optimisation
    - Fault injection
    - Resilience analysis
    """

    def __init__(
        self,
        thermal_model: ThermalModel,
        electrical_model: ElectricalModel,
        thermal_controller: ThermalController | None = None,
        time_step_hours: float = 1.0
    ):
        self.thermal_model = thermal_model
        self.electrical_model = electrical_model
        self.thermal_controller = thermal_controller
        self.time_step_hours = time_step_hours

    def step(
        self,
        station: StationState,
        environment: Environment,
        heating_power_kw: float | None = None
    ) -> StationState:
        """
        Advance the station simulation by one timestep.
        """

        # -------------------------------------------------
        # 1. Synchronize environmental conditions
        # -------------------------------------------------

        station.timestamp = environment.timestamp
        station.outside_temperature = environment.temperature_c
        station.wind_speed = environment.wind_speed_ms
        station.humidity = environment.humidity_percent

        # -------------------------------------------------
        # 2. Calculate thermal heat loss
        # -------------------------------------------------

        heat_loss_kw = (
            self.thermal_model.calculate_heat_loss(
                indoor_temperature=station.indoor_temperature,
                outdoor_temperature=environment.temperature_c,
                wind_speed=environment.wind_speed_ms
            )
        )

        station.thermal_demand_kw = heat_loss_kw

        # -------------------------------------------------
        # 3. Determine heating power
        # -------------------------------------------------

        if self.thermal_controller is not None:

            heating_power_kw = (
                self.thermal_controller.calculate_heating_power(
                    indoor_temperature=station.indoor_temperature,
                    heat_loss_kw=heat_loss_kw
                )
            )

        elif heating_power_kw is None:
            heating_power_kw = 0.0

        # -------------------------------------------------
        # 4. Update indoor temperature
        # -------------------------------------------------

        station.indoor_temperature = (
            self.thermal_model.update_indoor_temperature(
                current_temperature=station.indoor_temperature,
                heating_power_kw=heating_power_kw,
                heat_loss_kw=heat_loss_kw,
                time_step_hours=self.time_step_hours
            )
        )

        # -------------------------------------------------
        # 5. Calculate electrical demand
        # -------------------------------------------------

        hour = int(
            environment.timestamp.split()[1].split(":")[0]
        )

        station.electrical_demand_kw = (
            self.electrical_model.calculate_electrical_load(
                hour=hour
            )
        )

        return station

    def run(
        self,
        station: StationState,
        environments: list[Environment],
        heating_power_kw: float | None = None
    ) -> list[StationState]:
        """
        Run the simulation across multiple timesteps.
        """

        history = []

        for environment in environments:

            station = self.step(
                station=station,
                environment=environment,
                heating_power_kw=heating_power_kw
            )

            # Store an independent snapshot
            history.append(
                deepcopy(station)
            )

        return history