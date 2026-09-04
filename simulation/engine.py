from copy import deepcopy

from simulation.state import StationState
from simulation.environment import Environment
from simulation.thermal import ThermalModel
from simulation.controller import ThermalController


class SimulationEngine:
    """
    Coordinates the physical models and advances
    the Antarctic station Digital Twin through time.

    Current responsibilities:
    - Process environmental conditions
    - Calculate station heat loss
    - Determine heating power
    - Update thermal demand
    - Update indoor temperature
    - Store timestep history

    Future extensions:
    - Electrical load modelling
    - CHP dispatch
    - Fuel consumption
    - Asset health
    - Fault injection
    - Resilience analysis
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
        Advance the Digital Twin by one simulation timestep.

        Parameters
        ----------
        station:
            Current station state.

        environment:
            Environmental conditions for the current timestep.

        heating_power_kw:
            Fixed heating power to use when no thermal controller
            is attached.

            If a thermal controller exists, this value is ignored
            and heating power is determined automatically.

        Returns
        -------
        StationState
            Updated station state after one timestep.
        """

        # ---------------------------------------------------------
        # 1. Synchronize environmental state
        # ---------------------------------------------------------

        station.timestamp = environment.timestamp

        station.outside_temperature = (
            environment.temperature_c
        )

        station.wind_speed = (
            environment.wind_speed_ms
        )

        station.humidity = (
            environment.humidity_percent
        )

        # ---------------------------------------------------------
        # 2. Calculate heat loss
        # ---------------------------------------------------------

        heat_loss_kw = (
            self.thermal_model.calculate_heat_loss(
                indoor_temperature=station.indoor_temperature,
                outdoor_temperature=environment.temperature_c,
                wind_speed=environment.wind_speed_ms
            )
        )

        # Thermal demand currently corresponds to the heat
        # required to compensate for environmental heat loss.
        station.thermal_demand_kw = heat_loss_kw

        # ---------------------------------------------------------
        # 3. Determine heating power
        # ---------------------------------------------------------

        if self.thermal_controller is not None:

            heating_power_kw = (
                self.thermal_controller.calculate_heating_power(
                    indoor_temperature=station.indoor_temperature,
                    heat_loss_kw=heat_loss_kw
                )
            )

        elif heating_power_kw is None:

            # No controller and no externally supplied heat.
            heating_power_kw = 0.0

        # ---------------------------------------------------------
        # 4. Update indoor temperature
        # ---------------------------------------------------------

        new_indoor_temperature = (
            self.thermal_model.update_indoor_temperature(
                current_temperature=station.indoor_temperature,
                heating_power_kw=heating_power_kw,
                heat_loss_kw=heat_loss_kw,
                time_step_hours=self.time_step_hours
            )
        )

        station.indoor_temperature = (
            new_indoor_temperature
        )

        # ---------------------------------------------------------
        # 5. Return updated station state
        # ---------------------------------------------------------

        return station

    def run(
        self,
        station: StationState,
        environments: list[Environment],
        heating_power_kw: float | None = None
    ) -> list[StationState]:
        """
        Run the Digital Twin across multiple timesteps.

        Parameters
        ----------
        station:
            Initial station state.

        environments:
            Environmental conditions for each timestep.

        heating_power_kw:
            Constant heating power used when no thermal controller
            is attached.

        Returns
        -------
        list[StationState]
            Independent snapshots of the station state across time.
        """

        history: list[StationState] = []

        for environment in environments:

            station = self.step(
                station=station,
                environment=environment,
                heating_power_kw=heating_power_kw
            )

            # Deep copy is essential because StationState is mutable.
            # Without this, every history entry would point to the
            # same final station object.
            history.append(
                deepcopy(station)
            )

        return history