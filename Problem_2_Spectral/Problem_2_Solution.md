# Problem 2: The Spectral Discrepancy - Solution

**Task:** Diagnose the conflict between Satellite Alerts (Algae Bloom) and Ground Truth (Clear Water).

---

### 1. Non-Biological Factors & Spectral Differentiation

**Three Non-Biological Factors:**
1.  **Atmospheric Scattering (Haze/Aerosols):** Nanoparticles in the air (dust, smoke) scatter short wavelengths (Blue/Green). The satellite clearly sees "brightness" in the green band and misinterprets it as algae reflectance.
2.  **Sun Glint (Specular Reflection):** If the sun angle matches the sensor viewing angle, the water surface acts like a mirror. This saturates all bands, including Green.
3.  **Bottom Reflectance (Benthic Signal):** In shallow clear water, light hits the sand/mud bottom and reflects back. If the bottom is bright or has submerged weeds, it mimics surface algae.

**Using Bands to Prove Error:**
*   **Near-Infrared (NIR) Band:**
    *   **Water:** Absorbs NIR almost completely (looks black).
    *   **Algae (Floating):** Strong reflection in NIR (The "Red Edge" effect of chlorophyll).
    *   **Haze/Glint:** Haze usually drops off in NIR. Glint remains high.
    *   **Test:** If the "Greenness" is high but NIR is low/zero, it is **Bottom Reflectance** (submerged) or **Atmospheric Scattering** (Rayleigh scattering affects Blue/Green more than NIR). If NIR is extremely high alongside Green/Red/Blue, it is likely **Sun Glint** (mirror effect).

---

### 2. Spatial Decision Logic (Cancel vs. Keep)

**Scenario:** 5 sites are clear (Ground Truth). 45 are unverified. Satellite shows +40% Greenness everywhere.

**Logic: Spatial Autocorrelation & Bayes' Rule**
Given the "Greenness Index" rose uniformly (+40%) across *all* 50 sites simultaneously:
*   **Hypothesis A (Biological):** Massive regional bloom exploded in 7 days exactly everywhere.
*   **Hypothesis B (Sensor/Atmosphere):** A large-scale weather front (haze) or sensor calibration drift affected the whole tile.

**Mathematically:**
Since the 5 verifications are random samples from the population:
1.  Calculate the probability that 5 random sites are clear given a real regional bloom. It is extremely low ($P(Clear|Bloom) \approx 0$).
2.  **Spatial Correlation:** Atmospheric effects (haze) are spatially continuous over large scales (100km+). Algae blooms can be patchy. The uniformity of the signal (+40% everywhere) strongly suggests an atmospheric/sensor artifact.
3.  **Decision Weighting:**
    $$ Weight_{Satellite} = 0 \quad (Disproven \ by \ Ground \ Truth) $$
    $$ Weight_{Field} = 1.0 $$
    Since the signal error is *systematic* (verified at 5 representative points), we assume the error function $Error(x,y)$ applies to the whole image.
    
**Action:** **CANCEL THE ALERT** for the whole region. Flag the satellite data for "Atmospheric Correction Failure".

---

### 3. Validation Framework Design

A "Middleware" validation layer sitting between Raw Data and User Alert.

**Secondary Data Checks (The "Gatekeepers"):**

1.  **Meteorological Gate (Weather Model):**
    *   *Check:* Cloud Probability > 20%? Humidity > 85%?
    *   *Logic:* High humidity/clouds cause signal scattering.
    *   *Action:* If MET_RISK is High, downgrade Alert to "Potential Data Anomaly".

2.  **Temporal Consistency Gate (Time Series):**
    *   *Check:* $\Delta Index / \Delta t > Threshold$?
    *   *Logic:* Algae grows exponentially but follows a logistic curve. A vertical spike (instant jump) is physically impossible for biology.
    *   *Action:* If change is "Instantaneous", flag as Glitch.

3.  **Temperature Gate (Thermodynamics):**
    *   *Check:* Is Water Surface Temperature (SST) > 20°C?
    *   *Logic:* Algae needs warm water to bloom.
    *   *Action:* If SST < 10°C, a massive bloom is biologically unlikely. Flag as False Positive.

**Workflow:**
`Satellite_Raw -> Cloud_Mask -> Glint_Correction -> [Validation_Framework] -> Alert_System`
Only if all gates pass (Clear sky, low wind, warm water, realistic growth rate) is the notification sent.
