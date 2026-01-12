import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata, Rbf

def demo_incomplete_geometry():
    # 1. Generate a "True" Synthetic Reservoir (Ground Truth)
    # Let's create a basin shape: z = - (1 - r^2) * depth
    gx, gy = np.mgrid[-1:1:100j, -1:1:100j]
    radius = np.sqrt(gx**2 + gy**2)
    # Mask outside radius 1
    mask = radius <= 1.0
    
    # Natural distinct shape: deeper in middle, varying slope
    true_depth = -10 * (1 - radius**1.5) 
    true_depth[~mask] = np.nan
    
    # 2. Simulate "Survey Points" (The 65% accessible area)
    # Let's say top-right quadrant is inaccessible (Structural Obstruction)
    # Accessible: x < 0.3 or y < 0.3 (Just a cut to simulate 35% missing)
    
    # Generate random sample points
    np.random.seed(42)
    n_points = 100
    px = np.random.uniform(-1, 1, n_points)
    py = np.random.uniform(-1, 1, n_points)
    
    # Filter for "Reservoir" (radius < 1) AND "Accessible" (Let's block the top-right corner)
    # Obstruction zone: x > 0.2 and y > 0.2
    is_inside = (px**2 + py**2) <= 1.0
    is_accessible = ~((px > 0.2) & (py > 0.2))
    
    valid_mask = is_inside & is_accessible
    survey_x = px[valid_mask]
    survey_y = py[valid_mask]
    
    # Get depth measurements at these points
    survey_z = -10 * (1 - (np.sqrt(survey_x**2 + survey_y**2))**1.5)
    
    # Limit to ~40 points as per problem statement
    if len(survey_z) > 40:
        survey_x = survey_x[:40]
        survey_y = survey_y[:40]
        survey_z = survey_z[:40]
        
    # 3. Method A: Simple Averaging (The "Bad" Approach)
    avg_depth = np.mean(survey_z)
    estimated_volume_avg = avg_depth * np.sum(mask) # Area * Avg Depth
    
    # 4. Method B: Spatial Interpolation (RBF / Spline / Proxy for Kriging)
    # We want to extrapolate into the missing zone (x > 0.2, y > 0.2)
    
    # Create grid for interpolation
    grid_x, grid_y = np.mgrid[-1:1:100j, -1:1:100j]
    
    # Radial Basis Function interpolation (good for smooth natural surfaces)
    rbf = Rbf(survey_x, survey_y, survey_z, function='multiquadric', smooth=0.1)
    z_interp = rbf(grid_x, grid_y)
    
    # Mask outline again
    z_interp[radius > 1] = np.nan
    
    # Volume Calc
    # Pixel area = (2/100) * (2/100) = 0.0004
    pixel_area = 0.0004
    vol_true = np.nansum(true_depth) * pixel_area
    vol_interp = np.nansum(z_interp) * pixel_area
    
    # Visualization
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # Plot 1: Ground Truth
    im1 = axes[0].imshow(true_depth.T, extent=(-1,1,-1,1), origin='lower', cmap='terrain_r')
    axes[0].set_title(f'Ground Truth\nVolume: {abs(vol_true):.2f} units')
    axes[0].add_patch(plt.Rectangle((0.2, 0.2), 0.8, 0.8, fill=False, hatch='//', color='red', label='Unmeasured Zone'))
    
    # Plot 2: Survey Points (The Incomplete Data)
    axes[1].imshow(np.full_like(true_depth.T, np.nan), extent=(-1,1,-1,1), origin='lower') # Blank bg
    axes[1].scatter(survey_x, survey_y, c=survey_z, cmap='terrain_r', edgecolors='k', s=60)
    axes[1].add_patch(plt.Rectangle((0.2, 0.2), 0.8, 0.8, fill=True, color='gray', alpha=0.3))
    axes[1].text(0.5, 0.5, "OBSTRUCTION\n(Missing Data)", ha='center', color='red', fontweight='bold')
    axes[1].set_title(f'Available Data (40 pts)\nAvg Depth Estimate: {abs(avg_depth):.2f}')
    axes[1].set_xlim(-1, 1)
    axes[1].set_ylim(-1, 1)

    # Plot 3: Mathematical Reconstruction (Interpolation)
    im3 = axes[2].imshow(z_interp.T, extent=(-1,1,-1,1), origin='lower', cmap='terrain_r', vmin=np.nanmin(true_depth), vmax=0)
    axes[2].scatter(survey_x, survey_y, c='k', s=10, alpha=0.3, label='Survey Pts')
    axes[2].set_title(f'Reconstruction (RBF Interpolation)\nEst. Vol: {abs(vol_interp):.2f} (Error: {abs(vol_interp-vol_true)/abs(vol_true)*100:.1f}%)')
    
    plt.colorbar(im3, ax=axes[2], label='Depth')
    plt.tight_layout()
    plt.savefig('Problem_1_Geometry/geometry_analysis.png')
    print("Geometry analysis complete. Saved to Problem_1_Geometry/geometry_analysis.png")

if __name__ == "__main__":
    demo_incomplete_geometry()
