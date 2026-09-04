class ThermalController:
    """
    Physics-aware thermal controller.

    Combines feed-forward heat-loss compensation with
    proportional temperature feedback.
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
        indoor_temperature: float,
        heat_loss_kw: float
    ) -> float:
        """
        Calculate required heating power.

        Uses:
        - Feed-forward compensation for predicted heat loss
        - Proportional feedback for temperature correction
        """

        temperature_error = (
            self.target_temperature - indoor_temperature
        )

        feedback_power_kw = (
            temperature_error * self.proportional_gain
        )

        heating_power_kw = (
            heat_loss_kw + feedback_power_kw
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