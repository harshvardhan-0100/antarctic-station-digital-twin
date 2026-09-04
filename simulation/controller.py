class ThermalController:
    """
    Thermal controller for maintaining station indoor temperature.

    Uses a combination of:
    1. Temperature error correction.
    2. Compensation for ongoing environmental heat loss.

    This provides a simplified physics-informed heating control
    mechanism suitable for the Digital Twin.
    """

    def __init__(
        self,
        target_temperature: float = 20.0,
        max_heating_power_kw: float = 100.0,
        proportional_gain: float = 15.0
    ):
        """
        Parameters
        ----------
        target_temperature:
            Desired indoor station temperature in °C.

        max_heating_power_kw:
            Maximum available heating capacity in kW.

        proportional_gain:
            Heating response per degree of temperature error.
        """

        self.target_temperature = target_temperature
        self.max_heating_power_kw = max_heating_power_kw
        self.proportional_gain = proportional_gain

    def calculate_heating_power(
        self,
        indoor_temperature: float,
        heat_loss_kw: float
    ) -> float:
        """
        Calculate required heating power.

        Heating demand consists of:

        1. Environmental heat-loss compensation.
        2. Proportional correction based on indoor temperature error.
        """

        # Difference between desired and actual temperature
        temperature_error = (
            self.target_temperature - indoor_temperature
        )

        # Additional power required to recover temperature
        correction_power_kw = (
            temperature_error * self.proportional_gain
        )

        # Heating required to compensate for environmental losses
        heating_power_kw = (
            heat_loss_kw + correction_power_kw
        )

        # No negative heating
        heating_power_kw = max(
            0.0,
            heating_power_kw
        )

        # Respect physical heating capacity
        heating_power_kw = min(
            heating_power_kw,
            self.max_heating_power_kw
        )

        return heating_power_kw