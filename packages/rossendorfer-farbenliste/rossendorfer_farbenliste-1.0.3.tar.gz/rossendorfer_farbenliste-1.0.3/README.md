rossendorfer_farbenliste
Written 2020, Michal Smid

This package contains colors and colorscales which correspond to the style guideline of HZDR.

USAGE:
import rossendorfer_farbenliste as rofl
plt.imshow(some_image,cmap=rofl.cmap())  # standard colormap
plt.imshow(some_image,cmap=rofl.cmap_nw())  # colormap without white topping
