from simulation.controller import ThermalController

from copy import deepcopy

from simulation.state import StationState
from simulation.environment import Environment
from simulation.thermal import ThermalModel


class SimulationEngine:
    """
    Coordinates the different physical models and advances
    the station simulation through time.
    """

    def __init__(
        self,
        thermal_model: ThermalModel,
        thermal_controller: ThermalController | None = None,
        time_step_hours: float = 1.0
    ):
        self.thermal_model = thermal_model
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

        Parameters
        ----------
        station:
            Current state of the station.

        environment:
            External environmental conditions.

        heating_power_kw:
            Thermal power supplied to the station.
        """

        # Determine heating power
        if self.thermal_controller is not None:
            heating_power_kw = (
                self.thermal_controller.calculate_heating_power(
                    indoor_temperature=station.indoor_temperature
                )
            )

        elif heating_power_kw is None:
            heating_power_kw = 0.0

        # Calculate heat loss to the environment
        heat_loss_kw = self.thermal_model.calculate_heat_loss(
            indoor_temperature=station.indoor_temperature,
            outdoor_temperature=environment.temperature_c,
            wind_speed=environment.wind_speed_ms
        )

        # Update thermal demand
        station.thermal_demand_kw = heat_loss_kw

        # Calculate new indoor temperature
        new_indoor_temperature = (
            self.thermal_model.update_indoor_temperature(
                current_temperature=station.indoor_temperature,
                heating_power_kw=heating_power_kw,
                heat_loss_kw=heat_loss_kw,
                time_step_hours=self.time_step_hours
            )
        )

        # Updata station state
        station.indoor_temperature = new_indoor_temperature

        return station

    def run(
        self,
        station: StationState,
        environments: list[Environment],
        heating_power_kw: float | None = None
    ) -> list[StationState]:
        """
        Run the simulation across multiple environmental timesteps.

        Parameters
        ----------
        station:
            Initial state of the station.

        environments:
            Sequence of environmental conditions,
            one for each timestep.

        heating_power_kw:
            Fixed heating power supplied during the simulation.
            Ignored if a thermal controller is present.

        Returns
        -------
        list[StationState]:
            History of station states over the simulation.
        """

        history = []

        for environment in environments:

            # Synchronize simulation time
            station.timestamp = environment.timestamp

            # Advance one timestep
            station = self.step(
                station=station,
                environment=environment,
                heating_power_kw=heating_power_kw
            )

            # Store independent snapshot
            history.append(deepcopy(station))

        return history