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
        time_step_hours: float = 1.0
    ):
        self.thermal_model = thermal_model
        self.time_step_hours = time_step_hours

    def step(
        self,
        station: StationState,
        environment: Environment,
        heating_power_kw: float
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

        # Calculate heat loss to the environment
        heat_loss_kw = self.thermal_model.calculate_heat_loss(
            indoor_temperature=station.indoor_temperature,
            outdoor_temperature=environment.temperature_c,
            wind_speed=environment.wind_speed_ms
        )

        # Update thermal demand
        station.thermal_demand_kw = heat_loss_kw

        # Update indoor temperature
        new_indoor_temperature = (
            self.thermal_model.update_indoor_temperature(
                current_temperature=station.indoor_temperature,
                heating_power_kw=heating_power_kw,
                heat_loss_kw=heat_loss_kw,
                time_step_hours=self.time_step_hours
            )
        )

        station.indoor_temperature = new_indoor_temperature

        return station

    def run(
    self,
    station: StationState,
    environments: list[Environment],
    heating_power_kw: float
) -> list[StationState]:
        """
        Run the simulation across multiple environmental timesteps.

        Parameters
        ----------
        station:
            Initial state of the station.

        environments:
            Sequence of environmental conditions, one for each timestep.

        heating_power_kw:
            Constant thermal power supplied during the simulation.

        Returns
        -------
        list[StationState]:
            History of station states over the simulation.
        """

        history = []

        for environment in environments:
            station.timestamp = environment.timestamp

            station = self.step(
                station=station,
                environment=environment,
                heating_power_kw=heating_power_kw
            )

            history.append(deepcopy(station))

        return history