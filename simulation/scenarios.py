from simulation.environment import Environment


def antarctic_storm_scenario() -> list[Environment]:
    """
    Generate a 24-hour Antarctic storm scenario.

    The scenario represents progressively worsening weather
    followed by gradual recovery.
    """

    weather_data = [
        # Hour, Temperature (°C), Wind (m/s), Humidity (%), Pressure (hPa)

        ("00:00", -24.0, 12.0, 70.0, 995.0),
        ("01:00", -24.5, 13.0, 71.0, 994.0),
        ("02:00", -25.0, 15.0, 72.0, 993.0),
        ("03:00", -26.0, 17.0, 73.0, 991.0),
        ("04:00", -27.0, 20.0, 74.0, 989.0),
        ("05:00", -28.0, 23.0, 75.0, 987.0),

        # Storm intensifies
        ("06:00", -30.0, 27.0, 77.0, 984.0),
        ("07:00", -32.0, 30.0, 78.0, 981.0),
        ("08:00", -34.0, 34.0, 80.0, 978.0),
        ("09:00", -35.0, 38.0, 82.0, 975.0),
        ("10:00", -36.0, 42.0, 83.0, 972.0),
        ("11:00", -37.0, 45.0, 85.0, 970.0),

        # Peak storm
        ("12:00", -38.0, 48.0, 86.0, 968.0),
        ("13:00", -39.0, 50.0, 87.0, 966.0),

        # Recovery
        ("14:00", -37.0, 45.0, 85.0, 970.0),
        ("15:00", -35.0, 40.0, 83.0, 975.0),
        ("16:00", -33.0, 35.0, 81.0, 980.0),
        ("17:00", -31.0, 30.0, 79.0, 984.0),
        ("18:00", -29.0, 25.0, 77.0, 988.0),
        ("19:00", -28.0, 21.0, 75.0, 990.0),
        ("20:00", -27.0, 18.0, 74.0, 992.0),
        ("21:00", -26.0, 16.0, 73.0, 993.0),
        ("22:00", -25.0, 14.0, 72.0, 994.0),
        ("23:00", -24.0, 12.0, 71.0, 995.0),
    ]

    environments = []

    for time, temperature, wind, humidity, pressure in weather_data:
        environments.append(
            Environment(
                timestamp=f"2026-01-01 {time}",
                temperature_c=temperature,
                wind_speed_ms=wind,
                humidity_percent=humidity,
                pressure_hpa=pressure
            )
        )

    return environments