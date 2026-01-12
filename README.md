# FluxGen R&D Internship Assignment | Round 1

**Candidate Name:** Abhishek Kumar
**Date:** January 13, 2026

## Overview
This repository contains the solutions for the R&D Internship Round 1 Assignment. The solutions address four distinct problems involving mathematical modeling, spatial analysis, and system dynamics.

For each problem, I have provided:
1.  **Detailed Solution Document (Markdown):** Explaining the physics, math, and logic.
2.  **Presentation (HTML):** A modern, interactive slide deck summarizing the approach.
3.  **Python Simulation/Model:** Scripts used to generate the graphs and validate the theories.

---

## Structure

### [Problem 1: The Incomplete Geometry](Problem_1_Geometry/)
*Type: Spatial Interpolation & Uncertainty*
*   **Solution:** Uses **Kriging/RBF Interpolation** to estimate the volume of an irregular reservoir with 35% missing data.
*   **Key File:** `Problem_1_Geometry/Problem_1_Solution.md`
*   **Presentation:** `Problem_1_Geometry/presentation.html`
*   **Simulation:** `Problem_1_Geometry/geometry_demo.py` (Visually compares Averaging vs. Interpolation)

### [Problem 2: The Spectral Discrepancy](Problem_2_Spectral/)
*Type: Remote Sensing & Validation Frameworks*
*   **Solution:** Diagnoses a false "Algae Bloom" alert using spectral signatures distinguishing Atmospheric Haze from Chlorophyll.
*   **Key File:** `Problem_2_Spectral/Problem_2_Solution.md`
*   **Presentation:** `Problem_2_Spectral/presentation.html`
*   **Simulation:** `Problem_2_Spectral/spectral_demo.py` (Plots spectral reflectance curves)

### [Problem 3: The Balancing Act](Problem_3_MassBalance/)
*Type: System Dynamics & Mass Balance*
*   **Solution:** Models the "Missing 400 Units" as a combination of Hydraulic Lag (Buffer Storage) and Infiltration, using a Digital Twin approach.
*   **Key File:** `Problem_3_MassBalance/Problem_3_Solution.md`
*   **Presentation:** `Problem_3_MassBalance/presentation.html`
*   **Simulation:** `Problem_3_MassBalance/simulation_model.py` (Simulates the 12-hour delay graph)

### [Problem 4: Groundwater Spatial Model](Problem_4/)
*Type: Hydro-Spatial Modeling*
*   **Solution:** A grid-based superposition model quantifying the interaction of Agriculture, Built-up areas, Forests, and Water Bodies.
*   **Key File:** `Problem_4/Problem_4_Solution.md`
*   **Presentation:** `Problem_4/presentation.html`
*   **Simulation:** `Problem_4/spatial_model.py` (Generates the Impact Heatmap and Flow Vectors)

---

## How to Run the Simulations
The models are written in Python. Ensure you have `numpy` and `matplotlib` installed.
```bash
pip install numpy matplotlib scipy
```

**Run specific models:**
```bash
# Problem 1
python Problem_1_Geometry/geometry_demo.py

# Problem 2
python Problem_2_Spectral/spectral_demo.py

# Problem 3
python Problem_3_MassBalance/simulation_model.py

# Problem 4
python Problem_4/spatial_model.py
```

## Viewing the Presentations
Open the `presentation/index.html` file in any modern web browser to view the **Master Presentation**. From there, or via the file explorer, you can access the detailed presentations for each problem.
