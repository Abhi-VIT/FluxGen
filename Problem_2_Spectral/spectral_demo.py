import numpy as np
import matplotlib.pyplot as plt

def plot_spectral_signatures():
    # Wavelengths (nm) - Blue, Green, Red, NIR
    wavelengths = np.array([450, 550, 650, 850])
    bands = ['Blue', 'Green', 'Red', 'NIR']
    
    # Reflectance Signatures (Hypothetical)
    
    # 1. Clear Water: Low everywhere, slightly higher in Blue/Green, absorbs NIR completely
    water = np.array([0.05, 0.04, 0.01, 0.00])
    
    # 2. Algae Bloom: High Green (chlorophyll), absorbed Red, High NIR (vegetation red edge)
    algae = np.array([0.06, 0.15, 0.05, 0.40])
    
    # 3. Atmospheric Haze/Glitch: High scattering in Blue (Rayleigh), decreases with wavelength
    haze = np.array([0.30, 0.25, 0.20, 0.10])
    
    # 4. Sun Glint: High across all bands (specular reflection)
    glint = np.array([0.50, 0.50, 0.50, 0.45])

    plt.figure(figsize=(10, 6))
    
    plt.plot(wavelengths, water, 'b-o', label='Clear Water (Ground Truth)', linewidth=2)
    plt.plot(wavelengths, algae, 'g-o', label='Algae Bloom (Biological)', linewidth=3)
    plt.plot(wavelengths, haze, 'c--s', label='Atmospheric Haze (Non-Bio)', alpha=0.7)
    plt.plot(wavelengths, glint, 'y--^', label='Sun Glint (Non-Bio)', alpha=0.7)
    
    plt.title('Spectral Signatures: Why the Satellite might be confused')
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Reflectance')
    plt.xticks(wavelengths, bands)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Annotation
    plt.axvspan(750, 900, color='gray', alpha=0.1)
    plt.text(800, 0.2, 'NIR Band\nCritical for Distinguishing', ha='center')
    
    plt.tight_layout()
    plt.savefig('Problem_2_Spectral/spectral_signature.png')
    print("Spectral plot saved to Problem_2_Spectral/spectral_signature.png")

if __name__ == "__main__":
    plot_spectral_signatures()
