class ElectricalModel:
    """
    Models the electrical power demand of an Antarctic
    research station.

    The model represents non-heating electrical loads such as:

    - Lighting
    - Computing systems
    - Laboratory equipment
    - Communication systems
    - Pumps and motors
    - General infrastructure
    """

    def __init__(
        self,
        base_load_kw: float = 120.0,
        peak_load_kw: float = 180.0
    ):
        """
        Parameters
        ----------
        base_load_kw:
            Minimum continuous electrical demand.

        peak_load_kw:
            Maximum expected electrical demand.
        """

        self.base_load_kw = base_load_kw
        self.peak_load_kw = peak_load_kw

    def calculate_electrical_load(
        self,
        hour: int
    ) -> float:
        """
        Calculate electrical demand based on time of day.

        A simplified daily load profile is used.

        Higher demand occurs during active operational hours,
        while lower demand occurs during night hours.
        """

        # Night / reduced activity
        if 0 <= hour < 6:
            load_factor = 0.75

        # Morning ramp-up
        elif 6 <= hour < 9:
            load_factor = 0.90

        # Active operational period
        elif 9 <= hour < 18:
            load_factor = 1.0

        # Evening
        else:
            load_factor = 0.85

        electrical_load_kw = (
            self.base_load_kw
            * load_factor
        )

        # Ensure load remains within expected bounds
        electrical_load_kw = min(
            electrical_load_kw,
            self.peak_load_kw
        )

        return electrical_load_kw