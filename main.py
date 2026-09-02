from simulation.state import StationState
from simulation.environment import Environment
from simulation.thermal import ThermalModel


def main():
    environment = Environment(
        timestamp="2026-01-01 00:00",
        temperature_c=-25.0,
        wind_speed_ms=18.0,
        humidity_percent=70.0,
        pressure_hpa=990.0
    )

    station = StationState(
        timestamp=environment.timestamp,
        outside_temperature=environment.temperature_c,
        wind_speed=environment.wind_speed_ms,
        humidity=environment.humidity_percent
    )

    thermal_model = ThermalModel()

    heat_loss = thermal_model.calculate_heat_loss(
        indoor_temperature=station.indoor_temperature,
        outdoor_temperature=environment.temperature_c,
        wind_speed=environment.wind_speed_ms
    )

    station.thermal_demand_kw = heat_loss


    print(environment)
    print(station)
    print(f"\nCalculated Heat Loss: {heat_loss:.2f} kW")


if __name__ == "__main__":
    main()