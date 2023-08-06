# Empirical Mode Decomposition, EMD
## Installation
```python
    pip install emdpy-z
```
## Quick Start
```python
    # Import 
    from emdpy.emd import *
    import numpy as np

    # Input
    t = np.linspace(0, 1, 1000)
    modes = np.sin(2 * np.pi * 5 * t) + np.sin(2 * np.pi * 10 * t)
    y = modes + t
    x, y = t, y

    # EMD
    imfs, res, (mean, std) = emd(x, y, mode=0, ps=len(x), max_iter_num = 20)
    
    # Plot the figs
    plot_imfs(imfs, res, col=1)
```