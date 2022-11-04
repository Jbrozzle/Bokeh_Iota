import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd

# Fixing random state for reproducibility
np.random.seed(19680801)

raw_df = pd.read_csv(r'/Users/Josh/Desktop/Bokeh Scripts/Iota/LinkerTimeSeries.csv')
df_col = raw_df['IL26']

def random_walk(df_col,num_steps, max_step=0.05):
    """Return a 3D random walk as (num_steps, 3) array."""
    print(df_col.dropna())
    # arr = np.array[df_col]
    start_pos = np.random.random(3)
    steps = np.random.uniform(-max_step, max_step, size=(num_steps, 3))

    start_pos_1 = df_col.iloc[-num_steps]
    # steps = arr[-num_steps:-0]
    print(start_pos)
    print(start_pos_1)

    walk = start_pos + np.cumsum(steps, axis=0)
    return walk


def update_lines(num, walks, lines):
    for line, walk in zip(lines, walks):
        # NOTE: there is no .set_data() for 3 dim data...
        line.set_data(walk[:num, :2].T)
        line.set_3d_properties(walk[:num, 2])
    return lines


# Data: 40 random walks as (num_steps, 3) arrays
num_steps = 90
walks = [random_walk(df_col, num_steps) for index in range(90)]

# # Attaching 3D axis to the figure
# fig = plt.figure()
# ax = fig.add_subplot(projection="3d")

# # Create lines initially without data
# lines = [ax.plot([], [], [])[0] for _ in walks]
#
# # Setting the axes properties
# ax.set(xlim3d=(0, 1), xlabel='X')
# ax.set(ylim3d=(0, 1), ylabel='Y')
# ax.set(zlim3d=(0, 1), zlabel='Z')
#
# # Creating the Animation object
# ani = animation.FuncAnimation(
#     fig, update_lines, num_steps, fargs=(walks, lines), interval=100)
#
# plt.show()




import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import matplotlib.cm as cm
from matplotlib.patches import PathPatch


def color_test():

    data_1 = np.random.normal(100, 10, 200)
    data_2 = np.random.normal(90, 20, 200)
    data_3 = np.random.normal(80, 30, 200)
    data_4 = np.random.normal(70, 40, 200)
    data = [data_1, data_2, data_3, data_4]

    values = [t.mean() for t in data]

    # create a normalizer
    norm = Normalize(vmin=min(values), vmax=max(values))
    # normalize values
    norm_values = norm(values)
    # choose a colormap
    cmap = cm.magma
    # create colors
    colors = cmap(norm_values)
    # map values to a colorbar
    mappable = cm.ScalarMappable(norm=norm, cmap=cmap)
    mappable.set_array(colors)

    fig1, ax1 = plt.subplots()
    ax1.set_title('Basic Plot')
    ba = ax1.boxplot(data, patch_artist=True)
    patches = ba["boxes"]

    for p, c in zip(patches, colors):
        p.set_facecolor(c)

    cb = fig1.colorbar(mappable)
    cb.set_label("Mean")