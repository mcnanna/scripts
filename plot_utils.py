import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid

def shiftedColorMap(cmap_name, mn, mx, midpoint, name='shiftedcmap'):
    cmap = getattr(matplotlib.cm, cmap_name)

    cdict = {
        'red': [],
        'green': [],
        'blue': [],
        'alpha': []
        }

    start = mn
    stop = mx
    
    mid = float((midpoint - start))/(stop - start) # midpoint scaled between 0 and 1

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


def truncatedColorMap(cmap,n_min=0,n_max=256):
    """ Generate a truncated colormap
    Colormaps have a certain number of colors (usually 255) which is
    available via cmap.N
    This is a simple function which returns a new color map from a
    subset of the input colormap. For example, if you only want the jet
    colormap up to green colors you may use
    tcmap = truncate_cmap(plt.cm.jet,n_max=150)
    This function is especially useful when you want to remove the white
    bounds of a colormap
    Parameters
    cmap : plt.matplotlib.colors.Colormap
    n_min : int
    n_max : int
    Return
    truncated_cmap : plt.matplotlib.colors.Colormap
    """
    cmap = plt.matplotlib.cm.get_cmap(cmap)
    color_index = np.arange(n_min,n_max).astype(int)
    colors = cmap(color_index)
    name = "truncated_{}".format(cmap.name)
    return plt.matplotlib.colors.ListedColormap(colors,name=name)

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
