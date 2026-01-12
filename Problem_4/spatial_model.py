import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def gaussian(x, y, x0, y0, sigma, amplitude):
    return amplitude * np.exp(-((x - x0)**2 + (y - y0)**2) / (2 * sigma**2))

def run_groundwater_model():
    # Grid Setup
    N = 100
    x = np.linspace(0, 100, N)
    y = np.linspace(0, 100, N)
    X, Y = np.meshgrid(x, y)
    
    # 1. Define Consumption Sources (Drawdown effects)
    # Head is typically reduced by consumption, so these are negative impacts (drawdowns)
    # or we can model "Consumption Pressure" as positive fields.
    
    # Source A: Agriculture (Wide, heavy consumption)
    Z_agri = gaussian(X, Y, 25, 75, 15, 0.8)
    
    # Source B: Built-up (Concentrated, very heavy)
    Z_built = gaussian(X, Y, 75, 75, 10, 1.0)
    
    # Source C: Forest (Low consumption, stable) - Maybe acts as recharge?
    # Let's assume it has a small positive effect (recharge) or very low consumption.
    # Assignment says "consumption sources", so we'll model as low consumption.
    Z_forest = gaussian(X, Y, 25, 25, 20, 0.3)
    
    # Source D: Water Bodies (Recharge source usually, or evaporation loss)
    # Let's model as a strong Recharge zone (Positive Head contribution) to make it interesting
    # OR if strictly "consumption", maybe evaporation? 
    # Let's treat it as a stabilizing factor (Recharge).
    Z_water = -1.0 * gaussian(X, Y, 75, 25, 12, 0.6) # Negative consumption = Recharge
    
    # Total Impact Field (Net Groundwater Head Change)
    # Base head = 10 units. Subtract consumption, add recharge.
    # Z_total_impact = Consumption Sum
    Z_consumption_field = Z_agri + Z_built + Z_forest + Z_water
    
    # 2. Critical Zone (Red Triangle)
    # Let's place it in the middle where interactions happen
    poi_x, poi_y = 50, 50
    
    # 3. Calculate Gradients (Flow vectors)
    # Groundwater flows from High Head to Low Head. 
    # If Z represents "Drawdown", flow is TOWARDS high Z.
    # If Z represents "Head", flow is AWAY from high Z.
    # Let's assume Z_consumption_field is "Stress/Drawdown". 
    # So flow is induced towards the peaks of this field.
    Dy, Dx = np.gradient(Z_consumption_field)
    
    # Visualization
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Heatmap
    c = ax.pcolormesh(X, Y, Z_consumption_field, cmap='RdYlGn_r', shading='auto', alpha=0.8)
    cbar = fig.colorbar(c, ax=ax)
    cbar.set_label('Groundwater Stress / Consumption Intensity')
    
    # Streamlines / Gradient Vectors
    # Visualizing the "Pull" of consumption zones
    ax.streamplot(X, Y, Dx, Dy, color='k', density=1.5, linewidth=0.5, arrowsize=1)
    
    # Annotations
    ax.text(25, 75, 'Agriculture', ha='center', va='center', fontsize=12, fontweight='bold', color='white')
    ax.text(75, 75, 'Built-up', ha='center', va='center', fontsize=12, fontweight='bold', color='white')
    ax.text(25, 25, 'Forest', ha='center', va='center', fontsize=12, fontweight='bold', color='white')
    ax.text(75, 25, 'Water Body\n(Recharge)', ha='center', va='center', fontsize=12, fontweight='bold', color='blue')
    
    # Critical Zone Marker
    triangle = patches.RegularPolygon((poi_x, poi_y), numVertices=3, radius=5, orientation=0, color='red', label='Critical Zone', ec='white', lw=1.5)
    ax.add_patch(triangle)
    ax.text(poi_x, poi_y-8, 'Critical Zone', ha='center', color='red', fontweight='bold')
    
    ax.set_title('Spatial Interaction of Groundwater Consumption Sources')
    ax.set_xlabel('X Coordinate (km)')
    ax.set_ylabel('Y Coordinate (km)')
    
    plt.tight_layout()
    plt.savefig('groundwater_model.png')
    print("Spatial model complete. Heatmap saved to groundwater_model.png")

if __name__ == "__main__":
    run_groundwater_model()
