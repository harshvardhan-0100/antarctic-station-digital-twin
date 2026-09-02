from simulation.state import StationState


def main():
    station = StationState(
        timestamp="2026-01-01 00:00",
        outside_temperature=-25.0,
        wind_speed=18.0,
        humidity=70.0
    )

    print(station)


if __name__ == "__main__":
    main()