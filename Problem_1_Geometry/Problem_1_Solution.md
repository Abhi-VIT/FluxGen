# Problem 1: The Incomplete Geometry - Solution

**Task:** Estimate total storage capacity of an irregular reservoir with 35% missing data.

---

### 1. Mathematical Approaches for Estimation

**Why Simple Averaging is Inadequate:**
Simple averaging ($V = Area_{total} \times \bar{Depth}_{observed}$) makes the dangerous assumption that the unmeasured 35% is statistically identical to the measured 65%.
- **Bias Risk:** If the obstruction is caused by a deep feature (like a collapsed cavern roof) or a shallow feature (like a rock shelf), the average of the accessible area will heavily skew the result.
- **Topological Ignorance:** Averaging ignores trends. If the depth is steadily increasing as you approach the boundary of the unmeasured zone, averaging ignores this vector and assumes a flat bottom.

**Proposed Mathematical Approaches:**

*   **1. Ordinary Kriging (Geostatistical):**
    *   **Logic:** Kriging treats the depth as a spatially correlated random variable. It uses a **variogram** to quantify how depth similarity decreases with distance.
    *   **Benefit:** It provides not just an estimate, but also an **error variance** map, showing exactly where the model is least confident (the unmeasured zone).

*   **2. Spline Interpolation (Thin Plate Spline):**
    *   **Logic:** This fits a minimum-curvature surface through the known points, similar to bending a flexible sheet.
    *   **Benefit:** Ideal for "Natural" smooth formations. It extrapolates trends effectively (e.g., if the ground is sloping down, the spline continues that slope).

*   **3. Inverse Distance Weighting (IDW) with Trend:**
    *   A simpler heuristic where unknown points are weighted averages of neighbors, often coupled with a polynomial trend surface ($Z = aX + bY + c$) to capture the global slope before interpolating residuals.

---

### 2. Influence of "Naturally Formed" Physical Characteristics

A "naturally formed" reservoir implies specific geometric constraints that engineered structures do not have:

*   **Continuity ($C^1$ Continuity):** Natural erosion or deposition processes rarely create perfect vertical walls or right angles. The depth likely changes smoothly.
    *   *Strategy:* Use **Radial Basis Functions (RBF)** or splines (like in the generated Python simulation) which enforce smoothness derivatives, preventing jagged artifacts.
*   **Autocorrelation:** Depth at point $(x, y)$ is strongly predictive of depth at $(x+\delta, y+\delta)$.
*   **Boundary Conditions:** Natural basins often taper to zero depth at the edges (banks).
    *   *Strategy:* If we know the outline/perimeter of the reservoir, we can add "virtual survey points" with Depth=0 along the perimeter. This "anchors" the interpolation and prevents the model from mathematically exploding into infinite depths in the unmeasured void.

---

### 3. Quantifying and Reducing Uncertainty

**Quantifying Uncertainty:**
*   **Kriging Variance:** The Kriging algorithm outputs a secondary map of "Estimation Variance". The uncertainty will be low near survey points and high in the 35% void. Integrating this volume gives a $\pm$ Margin of Error (e.g., $10,000 m^3 \pm 1,500 m^3$).
*   **Cross-Validation (Leave-One-Out):** Systematically hide one survey point, predict it using the others, and calculate the error. This generates a Root Mean Square Error (RMSE) metric for the model itself.

**Reducing Uncertainty:**
*   **Perimeter Data:** Accessing just the *edge* of the unmeasured zone to confirm if it tapers to zero.
*   **Non-Invasive Sensing:** Using GPR (Ground Penetrating Radar) or Sonar from the accessible edge to get a profile line into the dark zone.
*   **Geological Homogeneity Check:** Determining if the rock type is consistent. If the unmeasured zone is a different rock type, the extrapolation trends might remain valid.

---

### Computational Demonstration
I have generated a simulation (`geometry_demo.py`) in this folder to visualize this.
**See `geometry_analysis.png` containing:**
1.  **Ground Truth:** The actual shape.
2.  **Survey Data:** The incomplete view we have.
3.  **Reconstruction:** How RBF interpolation recovers the missing shape much better than averaging.
