import numpy as np
import matplotlib.pyplot as plt

def run_simulation():
    # Simulation Parameters
    timesteps = 24  # Hours
    time = np.arange(timesteps)
    
    # Inputs
    rainfall_total = 1000
    # Assume rainfall happens at t=0 as an impulse or over the first hour
    rainfall_input = np.zeros(timesteps)
    rainfall_input[0] = rainfall_total
    
    # System Components
    # 1. Losses (Evaporation, Infiltration) - The "Missing" 400 units
    # Let's assume this happens relatively quickly or proportionally
    loss_fraction = 0.4  # 400 / 1000
    effective_water = rainfall_input * (1 - loss_fraction)
    losses = rainfall_input * loss_fraction
    
    # 2. Lake Storage Dynamics
    # K * dLake/dt = Inflow - Outflow
    # This is a reservoir routing problem.
    # But we are told: Lake rose by 400 (Storage). Outlet showed 200 (Output).
    # Total effective = 600. 
    # Current status: 400 stored, 200 left? Or is this over a specific event duration?
    # "After a heavy rainfall... rain gauge shows 1000... Lake rose by 400... Outlet shows 200"
    # This implies integrated totals over the event duration so far.
    
    # Let's model the delay (Problem 3, Q2).
    # Rainfall at Hour 0. Outlet increases at Hour 12.
    # This implies a Time of Concentration or Lag Time of 12 hours.
    
    lake_storage = np.zeros(timesteps)
    outlet_flow = np.zeros(timesteps)
    cumulative_outlet = np.zeros(timesteps)
    
    # Simple discrete reservoir model with delay
    # Lake Level (Storage) accumulates immediately from rain (fast runoff to lake)
    # but Outlet flow is controlled by a weir/valve that might have a threshold or long transit time.
    
    # Scenario A: Fast Inflow to Lake, Slow Outflow
    # Inflow to Lake
    lake_inflow = effective_water # 600 units enter lake at t=0
    
    current_lake_volume = 0
    k_discharge = 0.1 # Discharge coefficient
    
    # For the specific scenario of "Outlet didn't show increase until Hour 12"
    # We can model this as a travel time delay or a threshold level.
    delay_hours = 12
    
    for t in range(timesteps):
        # 1. Add Inflow to Lake
        current_lake_volume += lake_inflow[t]
        
        # 2. Calculate Outflow (delayed)
        outflow = 0
        if t >= delay_hours:
            # Simple linear reservoir model: Outflow proportional to storage spread over time
            # Or just a pulse for simplicity of matching the numbers?
            # Let's use a linear reservoir model but shifted.
            outflow = current_lake_volume * k_discharge
        
        # 3. Update Storage
        current_lake_volume -= outflow
        
        # Record states
        lake_storage[t] = current_lake_volume
        outlet_flow[t] = outflow
        if t > 0:
            cumulative_outlet[t] = cumulative_outlet[t-1] + outflow
        else:
            cumulative_outlet[t] = outflow

    # Visualization
    plt.figure(figsize=(12, 10))
    
    # Plot 1: Hyetograph & Hydrograph
    plt.subplot(3, 1, 1)
    plt.bar(time, rainfall_input, color='blue', alpha=0.5, label='Rainfall Input (1000)')
    plt.bar(time, losses, color='red', alpha=0.3, label='Initial Losses/Infiltration (400)', bottom=effective_water)
    plt.ylabel('Volume Units')
    plt.title('System Input & Losses')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 2: Lake Storage
    plt.subplot(3, 1, 2)
    plt.plot(time, lake_storage, 'g-', linewidth=2, label='Lake Storage (Vol)')
    plt.axhline(y=400, color='g', linestyle='--', alpha=0.5, label='Observed Rise (400)')
    plt.ylabel('Lake Volume Units')
    plt.title('Lake Storage Dynamics (Buffer Effect)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 3: Outlet Flow
    plt.subplot(3, 1, 3)
    plt.plot(time, outlet_flow, 'b-', linewidth=2, label='Outlet Rate')
    plt.plot(time, cumulative_outlet, 'b--', linewidth=2, label='Cumulative Outlet')
    plt.axvline(x=12, color='orange', linestyle='--', label='12hr Lag Time')
    plt.text(12.5, np.max(cumulative_outlet)/2, 'Lag due to routing/travel time', color='orange')
    plt.ylabel('Flow Units')
    plt.xlabel('Time (Hours)')
    plt.title('Outlet Response (Lag & Attenuation)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('mass_balance_simulation.png')
    print("Simulation complete. Chart saved to mass_balance_simulation.png")

if __name__ == "__main__":
    run_simulation()
