"""
Complex Sinusoids and Periodicity Analysis
==========================================

This module demonstrates when complex sinusoids are periodic and explores
the relationships between different complex exponential signals.

Key Concepts:
- Complex sinusoids: x[n] = e^(jωn) = cos(ωn) + j*sin(ωn)
- Periodicity condition: x[n] = x[n+N] for some integer N
- Relationship between continuous and discrete-time frequencies
- Aliasing effects in discrete-time complex sinusoids

Author: DSP Student
Date: June 25, 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import warnings
warnings.filterwarnings('ignore')

def is_periodic(omega, max_N=100):
    """
    Check if a complex sinusoid with frequency omega is periodic.
    
    Parameters:
    -----------
    omega : float
        Digital frequency in radians
    max_N : int
        Maximum period to check
        
    Returns:
    --------
    is_periodic : bool
        True if signal is periodic within max_N samples
    period : int or None
        Fundamental period if periodic, None otherwise
    """
    # For periodicity: e^(jω(n+N)) = e^(jωn)
    # This means: e^(jωN) = 1
    # Therefore: ωN = 2πk for some integer k
    # So: ω = 2πk/N (rational multiple of 2π)
    
    for N in range(1, max_N + 1):
        # Check if ωN is a multiple of 2π
        k = omega * N / (2 * np.pi)
        if abs(k - round(k)) < 1e-10:  # Check if k is essentially an integer
            return True, N
    
    return False, None

def generate_complex_sinusoid(omega, N_samples=50):
    """
    Generate a complex sinusoid.
    
    Parameters:
    -----------
    omega : float
        Digital frequency in radians
    N_samples : int
        Number of samples to generate
        
    Returns:
    --------
    n : ndarray
        Sample indices
    x : ndarray
        Complex sinusoid samples
    """
    n = np.arange(N_samples)
    x = np.exp(1j * omega * n)
    return n, x

def plot_complex_sinusoid(omega, N_samples=50, title_suffix=""):
    """
    Plot a complex sinusoid showing real, imaginary, and magnitude components.
    
    Parameters:
    -----------
    omega : float
        Digital frequency in radians
    N_samples : int
        Number of samples
    title_suffix : str
        Additional text for the plot title
    """
    n, x = generate_complex_sinusoid(omega, N_samples)
    
    # Check periodicity
    is_per, period = is_periodic(omega)
    period_text = f"Period = {period}" if is_per else "Not periodic"
    
    # Create the plot
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'Complex Sinusoid: $e^{{j{omega:.3f}n}}$ {title_suffix}\n'
                f'Digital Frequency: ω = {omega:.3f} rad/sample ({period_text})', 
                fontsize=14, fontweight='bold')
    
    # Real part
    axes[0, 0].stem(n, np.real(x), basefmt='b-', linefmt='b-', markerfmt='bo')
    axes[0, 0].set_title('Real Part: cos(ωn)')
    axes[0, 0].set_xlabel('n (samples)')
    axes[0, 0].set_ylabel('Amplitude')
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].axhline(y=0, color='k', linestyle='-', alpha=0.3)
    
    # Imaginary part
    axes[0, 1].stem(n, np.imag(x), basefmt='r-', linefmt='r-', markerfmt='ro')
    axes[0, 1].set_title('Imaginary Part: sin(ωn)')
    axes[0, 1].set_xlabel('n (samples)')
    axes[0, 1].set_ylabel('Amplitude')
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].axhline(y=0, color='k', linestyle='-', alpha=0.3)
    
    # Magnitude
    axes[1, 0].stem(n, np.abs(x), basefmt='g-', linefmt='g-', markerfmt='go')
    axes[1, 0].set_title('Magnitude: |e^(jωn)|')
    axes[1, 0].set_xlabel('n (samples)')
    axes[1, 0].set_ylabel('Magnitude')
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].set_ylim([0, 1.2])
    
    # Phase
    phase = np.angle(x)
    axes[1, 1].stem(n, phase, basefmt='m-', linefmt='m-', markerfmt='mo')
    axes[1, 1].set_title('Phase: ∠e^(jωn) = ωn')
    axes[1, 1].set_xlabel('n (samples)')
    axes[1, 1].set_ylabel('Phase (radians)')
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].axhline(y=0, color='k', linestyle='-', alpha=0.3)
    
    # Add period markers if periodic
    if is_per and period <= N_samples:
        for ax in axes.flat:
            for p in range(period, N_samples, period):
                ax.axvline(x=p, color='orange', linestyle='--', alpha=0.7, linewidth=2)
    
    plt.tight_layout()
    plt.show()
    
    return is_per, period

def demonstrate_periodicity_conditions():
    """Demonstrate different periodicity conditions"""
    print("Complex Sinusoids Periodicity Analysis")
    print("="*60)
    print("A complex sinusoid x[n] = e^(jωn) is periodic if:")
    print("ω = 2πk/N for integers k and N")
    print("This means ω must be a rational multiple of 2π")
    print("="*60)
    
    # Test cases
    test_frequencies = [
        (np.pi/4, "π/4 (Periodic)"),
        (np.pi/3, "π/3 (Periodic)"),
        (np.pi/2, "π/2 (Periodic)"),
        (np.pi, "π (Periodic)"),
        (2*np.pi/3, "2π/3 (Periodic)"),
        (np.pi*np.sqrt(2)/2, "π√2/2 (Non-periodic)"),
        (1.0, "1.0 rad (Non-periodic)"),
    ]
    
    results = []
    for omega, description in test_frequencies:
        is_per, period = is_periodic(omega)
        results.append((omega, description, is_per, period))
        
        status = f"Period = {period}" if is_per else "Not periodic"
        k_over_N = omega / (2*np.pi) if is_per else "N/A"
        
        print(f"ω = {omega:.4f} ({description})")
        print(f"  Status: {status}")
        print(f"  ω/(2π) = {k_over_N}")
        print()
    
    return results

def example_1_periodic_vs_nonperiodic():
    """Example 1: Compare periodic and non-periodic complex sinusoids"""
    print("\nExample 1: Periodic vs Non-Periodic Complex Sinusoids")
    print("="*60)
    
    # Periodic case: ω = π/4
    omega1 = np.pi/4
    print(f"Case 1: ω = π/4 = {omega1:.4f} rad/sample")
    print(f"ω/(2π) = {omega1/(2*np.pi):.4f} = 1/8 (rational)")
    is_per1, period1 = plot_complex_sinusoid(omega1, 40, "- Periodic Case")
    
    # Non-periodic case: ω = 1.0
    omega2 = 1.0
    print(f"\nCase 2: ω = 1.0 rad/sample")
    print(f"ω/(2π) = {omega2/(2*np.pi):.4f} ≈ 0.159 (irrational)")
    is_per2, period2 = plot_complex_sinusoid(omega2, 40, "- Non-Periodic Case")

def example_2_aliasing_relationship():
    """Example 2: Demonstrate aliasing relationship between complex sinusoids"""
    print("\nExample 2: Aliasing Relationship in Complex Sinusoids")
    print("="*60)
    print("Complex sinusoids with frequencies differing by 2πk are identical:")
    print("e^(j(ω+2πk)n) = e^(jωn) * e^(j2πkn) = e^(jωn)")
    print()
    
    # Base frequency
    omega_base = np.pi/6
    
    # Aliased frequencies
    omega_alias1 = omega_base + 2*np.pi
    omega_alias2 = omega_base - 2*np.pi
    
    n = np.arange(20)
    x_base = np.exp(1j * omega_base * n)
    x_alias1 = np.exp(1j * omega_alias1 * n)
    x_alias2 = np.exp(1j * omega_alias2 * n)
    
    # Verify they are identical
    diff1 = np.max(np.abs(x_base - x_alias1))
    diff2 = np.max(np.abs(x_base - x_alias2))
    
    print(f"Base frequency: ω₀ = π/6 ≈ {omega_base:.4f} rad/sample")
    print(f"Alias 1: ω₁ = ω₀ + 2π ≈ {omega_alias1:.4f} rad/sample")
    print(f"Alias 2: ω₂ = ω₀ - 2π ≈ {omega_alias2:.4f} rad/sample")
    print(f"Max difference |x₀[n] - x₁[n]|: {diff1:.2e}")
    print(f"Max difference |x₀[n] - x₂[n]|: {diff2:.2e}")
    
    # Plot comparison
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Aliasing in Complex Sinusoids: Identical Signals', fontsize=14, fontweight='bold')
    
    # Plot real parts
    axes[0].stem(n, np.real(x_base), basefmt='b-', linefmt='b-', markerfmt='bo', label=f'ω = π/6')
    axes[0].set_title('Base Frequency: π/6')
    axes[0].set_xlabel('n')
    axes[0].set_ylabel('Real Part')
    axes[0].grid(True, alpha=0.3)
    
    axes[1].stem(n, np.real(x_alias1), basefmt='r-', linefmt='r-', markerfmt='ro')
    axes[1].set_title('Alias 1: π/6 + 2π')
    axes[1].set_xlabel('n')
    axes[1].set_ylabel('Real Part')
    axes[1].grid(True, alpha=0.3)
    
    axes[2].stem(n, np.real(x_alias2), basefmt='g-', linefmt='g-', markerfmt='go')
    axes[2].set_title('Alias 2: π/6 - 2π')
    axes[2].set_xlabel('n')
    axes[2].set_ylabel('Real Part')
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def example_3_frequency_resolution():
    """Example 3: Demonstrate frequency resolution and minimum period"""
    print("\nExample 3: Frequency Resolution and Minimum Period")
    print("="*60)
    print("The minimum resolvable frequency difference is 2π/N")
    print("where N is the observation length")
    print()
    
    frequencies = [2*np.pi/16, 2*np.pi/8, 2*np.pi/4]  # Different periods
    names = ["Period = 16", "Period = 8", "Period = 4"]
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Frequency Resolution: Different Periods', fontsize=14, fontweight='bold')
    
    for i, (omega, name) in enumerate(zip(frequencies, names)):
        n = np.arange(32)
        x = np.exp(1j * omega * n)
        
        axes[i].stem(n, np.real(x), basefmt='b-', linefmt='b-', markerfmt='bo')
        axes[i].set_title(f'{name}\nω = 2π/{int(2*np.pi/omega)}')
        axes[i].set_xlabel('n')
        axes[i].set_ylabel('Real Part')
        axes[i].grid(True, alpha=0.3)
        
        # Mark one complete period
        period = int(2*np.pi/omega)
        axes[i].axvspan(0, period-1, alpha=0.2, color='yellow', label=f'One Period')
        axes[i].legend()
    
    plt.tight_layout()
    plt.show()

def main():
    """Main function to run all examples"""
    print("Digital Signal Processing: Complex Sinusoids and Periodicity")
    print("="*70)
    print("This demonstration explores:")
    print("• When complex sinusoids e^(jωn) are periodic")
    print("• Relationship between frequency and periodicity")
    print("• Aliasing effects in discrete-time complex sinusoids")
    print("• Frequency resolution and observation length")
    print("="*70)
    
    # Demonstrate periodicity conditions
    results = demonstrate_periodicity_conditions()
    
    # Run examples
    example_1_periodic_vs_nonperiodic()
    example_2_aliasing_relationship()
    example_3_frequency_resolution()
    
    print("\n" + "="*70)
    print("Key Takeaways:")
    print("• Complex sinusoids are periodic only when ω = 2πk/N (rational multiple of 2π)")
    print("• Frequencies differing by 2π are identical (aliasing)")
    print("• Minimum resolvable frequency difference is 2π/N")
    print("• Discrete-time frequency is fundamentally different from continuous-time")
    print("="*70)

if __name__ == "__main__":
    main()
