class ThermalModel:
    """
    Simplified thermal model for estimating heat loss
    from an Antarctic research station.
    """

    def __init__(
        self,
        heat_transfer_coefficient: float = 0.25,
        surface_area_m2: float = 2500.0,
        wind_factor: float = 0.02
    ):
        """
        Parameters
        ----------
        heat_transfer_coefficient:
            Overall U-value of the station envelope (W/m²·K).

        surface_area_m2:
            Effective heat transfer surface area (m²).

        wind_factor:
            Simplified coefficient representing increased
            heat loss due to wind and infiltration.
        """

        self.u_value = heat_transfer_coefficient
        self.surface_area = surface_area_m2
        self.wind_factor = wind_factor

    def calculate_heat_loss(
        self,
        indoor_temperature: float,
        outdoor_temperature: float,
        wind_speed: float
    ) -> float:
        """
        Calculate thermal heat loss in kW.
        """

        temperature_difference = max(
            0,
            indoor_temperature - outdoor_temperature
        )

        base_heat_loss_watts = (
            self.u_value
            * self.surface_area
            * temperature_difference
        )

        wind_multiplier = (
            1 + self.wind_factor * wind_speed
        )

        total_heat_loss_watts = (
            base_heat_loss_watts * wind_multiplier
        )

        return total_heat_loss_watts / 1000

    def update_indoor_temperature(
        self,
        current_temperature: float,
        heating_power_kw: float,
        heat_loss_kw: float,
        time_step_hours: float = 1.0,
        thermal_capacity_j_per_k: float = 5e8
    ) -> float:
        """
        Update indoor temperature based on the net thermal energy
        entering or leaving the building.

        Parameters
        ----------
        current_temperature:
            Current indoor temperature in °C.

        heating_power_kw:
            Thermal power supplied to the building in kW.

        heat_loss_kw:
            Thermal power lost to the environment in kW.

        time_step_hours:
            Simulation timestep in hours.

        thermal_capacity_j_per_k:
            Effective thermal capacitance of the station in J/K.
        """

        net_power_kw = heating_power_kw - heat_loss_kw

        net_energy_joules = (
            net_power_kw
            * 1000
            * time_step_hours
            * 3600
        )

        temperature_change = (
            net_energy_joules / thermal_capacity_j_per_k
        )

        return current_temperature + temperature_change