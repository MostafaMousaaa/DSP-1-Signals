"""
Digital Signal Processing Visualizations
=========================================

This module contains various DSP visualization examples.
Starting with signal decomposition into even and odd parts.

Author: DSP Student
Date: June 25, 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import warnings
warnings.filterwarnings('ignore')

def decompose_signal(x, n):
    """
    Decompose a discrete signal into even and odd parts.
    
    Parameters:
    -----------
    x : array_like
        Input signal samples
    n : array_like
        Sample indices corresponding to x
        
    Returns:
    --------
    x_even : ndarray
        Even part of the signal
    x_odd : ndarray
        Odd part of the signal
    n_extended : ndarray
        Extended sample indices for symmetric representation
    """
    # Create extended signal for negative indices
    N = len(x)
    n_extended = np.arange(-N+1, N)
    
    # Extend the signal with zeros and flip for negative indices
    x_extended = np.zeros(len(n_extended))
    
    # Place original signal at appropriate positions
    for i, sample in enumerate(x):
        if n[i] >= 0:
            x_extended[N-1+n[i]] = sample
        else:
            x_extended[N-1+n[i]] = sample
    
    # Calculate even and odd parts
    x_even = 0.5 * (x_extended + np.flip(x_extended))
    x_odd = 0.5 * (x_extended - np.flip(x_extended))
    
    return x_even, x_odd, n_extended

def plot_signal_decomposition(x, n, title="Signal Decomposition"):
    """
    Plot the original signal and its even/odd decomposition.
    
    Parameters:
    -----------
    x : array_like
        Input signal samples
    n : array_like
        Sample indices
    title : str
        Title for the plot
    """
    # Decompose the signal
    x_even, x_odd, n_extended = decompose_signal(x, n)
    
    # Create the plot
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(title, fontsize=16, fontweight='bold')
    
    # Original signal
    axes[0, 0].stem(n, x, basefmt='b-', linefmt='b-', markerfmt='bo')
    axes[0, 0].set_title('Original Signal x[n]')
    axes[0, 0].set_xlabel('n')
    axes[0, 0].set_ylabel('Amplitude')
    axes[0, 0].grid(True)
    
    # Even part
    axes[0, 1].stem(n_extended, x_even, basefmt='g-', linefmt='g-', markerfmt='go')
    axes[0, 1].set_title('Even Part x_e[n] = (x[n] + x[-n])/2')
    axes[0, 1].set_xlabel('n')
    axes[0, 1].set_ylabel('Amplitude')
    axes[0, 1].grid(True)
    
    # Odd part
    axes[1, 0].stem(n_extended, x_odd, basefmt='r-', linefmt='r-', markerfmt='ro')
    axes[1, 0].set_title('Odd Part x_o[n] = (x[n] - x[-n])/2')
    axes[1, 0].set_xlabel('n')
    axes[1, 0].set_ylabel('Amplitude')
    axes[1, 0].grid(True, )
    
    # Verification: sum of even and odd parts
    x_reconstructed = x_even + x_odd
    # Extract only the positive indices for comparison
    start_idx = len(n_extended) // 2
    x_recon_positive = x_reconstructed[start_idx:start_idx+len(n)]
    
    axes[1, 1].stem(n, x_recon_positive, basefmt='m-', linefmt='m-', markerfmt='mo', label='Reconstructed')
    axes[1, 1].stem(n, x, basefmt='k-', linefmt='k--', markerfmt='ks', label='Original')
    axes[1, 1].set_title('Verification: x[n] = x_e[n] + x_o[n]')
    axes[1, 1].set_xlabel('n')
    axes[1, 1].set_ylabel('Amplitude')
    axes[1, 1].grid(True)
    axes[1, 1].legend()
    
    plt.tight_layout()
    plt.show()

def example_1_arbitrary_signal():
    """Example 1: Arbitrary discrete signal"""
    print("Example 1: Arbitrary Discrete Signal")
    print("="*50)
    
    # Define an arbitrary signal
    n = np.array([0, 1, 2, 3, 4])
    x = np.array([2, 1, -1, 3, 2])
    
    print(f"Signal: x[n] = {x}")
    print(f"Indices: n = {n}")
    
    # Plot decomposition
    plot_signal_decomposition(x, n, "Example 1: Arbitrary Signal Decomposition")
    
    # Print mathematical breakdown
    x_even, x_odd, n_extended = decompose_signal(x, n)
    print(f"\nMathematical breakdown:")
    print(f"Even part: x_e[n] = (x[n] + x[-n])/2")
    print(f"Odd part:  x_o[n] = (x[n] - x[-n])/2")
    print(f"Verification: x[n] = x_e[n] + x_o[n]")

def example_2_exponential_signal():
    """Example 2: Exponential signal"""
    print("\n\nExample 2: Exponential Signal")
    print("="*50)
    
    # Define exponential signal
    n = np.arange(0, 6)
    a = 0.8
    x = a**n
    
    print(f"Signal: x[n] = {a}^n for n = {n}")
    print(f"Values: x[n] = {np.round(x, 3)}")
    
    # Plot decomposition
    plot_signal_decomposition(x, n, f"Example 2: Exponential Signal (a={a}) Decomposition")

def example_3_sinusoidal_signal():
    """Example 3: Sinusoidal signal"""
    print("\n\nExample 3: Sinusoidal Signal")
    print("="*50)
    
    # Define sinusoidal signal
    n = np.arange(-5, 6)
    omega = np.pi/4
    x = np.sin(omega * n)
    
    print(f"Signal: x[n] = sin(π/4 * n) for n = {n}")
    print(f"Values: x[n] = {np.round(x, 3)}")
    
    # Plot decomposition
    plot_signal_decomposition(x, n, "Example 3: Sinusoidal Signal Decomposition")
    
    print(f"\nNote: Sine is an odd function, so:")
    print(f"- Even part should be approximately zero")
    print(f"- Odd part should equal the original signal")

def main():
    """Main function to run all examples"""
    print("Digital Signal Processing: Signal Decomposition into Even and Odd Parts")
    print("="*80)
    print("This demonstration shows how any signal can be decomposed into:")
    print("• Even part: x_e[n] = (x[n] + x[-n])/2")
    print("• Odd part:  x_o[n] = (x[n] - x[-n])/2")
    print("• Original:  x[n] = x_e[n] + x_o[n]")
    print("="*80)
    
    # Run all examples
    example_1_arbitrary_signal()
    example_2_exponential_signal()
    example_3_sinusoidal_signal()
    
    print("\n" + "="*80)
    print("Key Properties:")
    print("• Even signals: x_e[n] = x_e[-n] (symmetric about n=0)")
    print("• Odd signals:  x_o[n] = -x_o[-n] (antisymmetric about n=0)")
    print("• Any signal can be uniquely decomposed into even + odd parts")
    print("• Even part of odd signal = 0, Odd part of even signal = 0")
    print("="*80)

if __name__ == "__main__":
    main()
