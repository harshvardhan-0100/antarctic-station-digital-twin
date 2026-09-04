class ThermalController:
    """
    Simple thermostat-based thermal controller.

    Determines the heating power required based on the
    difference between current and target indoor temperature.
    """

    def __init__(
        self,
        target_temperature: float = 20.0,
        max_heating_power_kw: float = 100.0,
        proportional_gain: float = 15.0
    ):
        self.target_temperature = target_temperature
        self.max_heating_power_kw = max_heating_power_kw
        self.proportional_gain = proportional_gain

    def calculate_heating_power(
        self,
        indoor_temperature: float
    ) -> float:
        """
        Calculate requested heating power.

        Uses a proportional control strategy.
        """

        temperature_error = (
            self.target_temperature - indoor_temperature
        )

        heating_power = (
            temperature_error * self.proportional_gain
        )

        # No cooling capability in this model
        heating_power = max(0.0, heating_power)

        # Respect physical heating capacity
        heating_power = min(
            heating_power,
            self.max_heating_power_kw
        )

        return heating_power