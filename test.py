from simulation.electrical import ElectricalModel


electrical_model = ElectricalModel()

load = electrical_model.calculate_electrical_load(
    hour=12
)

print(f"Electrical Load: {load:.2f} kW")