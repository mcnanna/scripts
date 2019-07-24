import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid

def shiftedColorMap(cmap_name, axis, midpoint, name='shiftedcmap'):
    cmap = getattr(matplotlib.cm, cmap_name)

    cdict = {
        'red': [],
        'green': [],
        'blue': [],
        'alpha': []
        }

    start = min(axis)
    stop = max(axis)
    
    mid = (midpoint - start)/(stop - start) # midpoint scaled between 0 and 1

    reg_index = np.linspace(0, 1.0, 257)

    shift_index = np.hstack([
        np.linspace(0.0, mid, 128, endpoint=False),
        np.linspace(mid, 1.0, 129, endpoint=True)
        ])

    for ri, si in zip(reg_index, shift_index):
        r, g, b, a = cmap(ri)

        cdict['red'].append((si, r, r))
        cdict['green'].append((si, g, g))
        cdict['blue'].append((si, b, b))
        cdict['alpha'].append((si, a, a))

    newcmap = matplotlib.colors.LinearSegmentedColormap(name, cdict)
    plt.register_cmap(cmap=newcmap)

    return newcmap

# This function is likely uneeded. Instead just do cmap=plt.get_cmap('cmapname', n) inside of plt.figure or whatever
# Also, to center the ticks nicely:
# cbar.set_ticks( (np.arange(n) + 0.5)*(n-1)/n )
# cbar.set_ticklabels( np.arange(n) ) or whatever else you want them to be
def discrete_cmap(N, base_cmap=None):
    """Create an N-bin discrete colormap from the specified input map"""

    # Note that if base_cmap is a string or None, you can simply do
    #    return plt.cm.get_cmap(base_cmap, N)
    # The following works for string, None, or a colormap instance:

    base = plt.cm.get_cmap(base_cmap)
    color_list = base(np.linspace(0, 1, N))
    cmap_name = base.name + str(N)
    return base.from_list(cmap_name, color_list, N)
