import matplotlib.pyplot
import matplotlib.cbook as cbook
import numpy as np
import pandas as pd

from bokeh.plotting import figure, show


import matplotlib.pyplot as plt
import numpy as np
import io

def create_boxplot(raw_df):

    raw_df.set_index('Date', inplace=True)
    cats = list(raw_df.columns)

    raw_df = raw_df.stack().reset_index()
    raw_df.drop(['Date'], axis=1, inplace=True)
    raw_df.rename({'level_1': 'group', 0: 'score'}, axis='columns', inplace=True)

    print(raw_df)

    # generate some synthetic time series for six different categories
    # cats = list("abcdef")
    yy = np.random.randn(2000)
    g = np.random.choice(cats, 2000)

    for i, l in enumerate(cats):
        yy[g == l] += i // 2
    df = pd.DataFrame(dict(score=yy, group=g))
    # print(df)
    df = raw_df

    # find the quartiles and IQR for each category
    groups = df.groupby('group')
    q1 = groups.quantile(q=0.25)
    q2 = groups.quantile(q=0.5)
    q3 = groups.quantile(q=0.75)
    iqr = q3 - q1
    upper = q3 + 1.5*iqr
    lower = q1 - 1.5*iqr

    # find the outliers for each category
    def outliers(group):
        cat = group.name
        return group[(group.score > upper.loc[cat]['score']) | (group.score < lower.loc[cat]['score'])]['score']
    out = groups.apply(outliers).dropna()

    # prepare outlier data for plotting, we need coordinates for every outlier.
    if not out.empty:
        outx = list(out.index.get_level_values(0))
        outy = list(out.values)

    p = figure(tools="", background_fill_color="#efefef", x_range=cats, toolbar_location=None)

    # if no outliers, shrink lengths of stems to be no longer than the minimums or maximums
    qmin = groups.quantile(q=0.00)
    qmax = groups.quantile(q=1.00)
    upper.score = [min([x,y]) for (x,y) in zip(list(qmax.loc[:,'score']),upper.score)]
    lower.score = [max([x,y]) for (x,y) in zip(list(qmin.loc[:,'score']),lower.score)]

    # stems
    p.segment(cats, upper.score, cats, q3.score, line_color="black")
    p.segment(cats, lower.score, cats, q1.score, line_color="black")

    # boxes
    p.vbar(cats, 0.7, q2.score, q3.score, fill_color="#E08E79", line_color="black")
    p.vbar(cats, 0.7, q1.score, q2.score, fill_color="#3B8686", line_color="black")

    # whiskers (almost-0 height rects simpler than segments)
    p.rect(cats, lower.score, 0.2, 0.01, line_color="black")
    p.rect(cats, upper.score, 0.2, 0.01, line_color="black")

    # outliers
    if not out.empty:
        p.circle(outx, outy, size=6, color="#F38630", fill_alpha=0.6)

    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = "white"
    p.grid.grid_line_width = 2
    p.xaxis.major_label_text_font_size="16px"

    return p
# show(p)

from matplotlib.colors import Normalize
import matplotlib.cm as cm
from matplotlib.patches import PathPatch

def matplot_box(df_col, live, lower, upper):

    x = np.array(df_col.dropna())
    flierprops = dict(marker='o', markerfacecolor='green', markersize=5)
    meanlineprops = dict(linestyle='-', linewidth=1.5, color='blue')
    fig5, ax5 = plt.subplots()
    stats = cbook.boxplot_stats(x, labels=[1])
    stats[0]['mean'] = live
    z_score = (live - df_col[-90:].mean())/df_col[-90:].std()
    scalar_color = cm.ScalarMappable(cmap="RdYlGn")
    scalar_color.set_clim(-5, 5)
    color = scalar_color.to_rgba(x=z_score)
    boxprops = dict(color=color)
    medianprops = dict(linestyle='none', linewidth=0, color='firebrick')

    ax5.bxp(stats, vert=False, showmeans=True, widths=0.45, patch_artist=True,
                 meanprops=meanlineprops, meanline=True, medianprops=medianprops,
                 showcaps=False, flierprops=flierprops, boxprops=boxprops,
                 showfliers=False)

    fig5.set_figheight(0.5)
    fig5.set_figwidth(1.5)
    plt.tight_layout(pad=0, h_pad=0)
    plt.xlim(lower, upper)
    plt.setp(ax5.get_yticklabels()[0], visible=False)
    plt.setp(ax5.get_xticklabels()[0], visible=False)
    plt.tick_params(left=False)
    ax5.spines['right'].set_visible(False)
    ax5.spines['top'].set_visible(False)
    ax5.spines['left'].set_visible(False)
    ax5.spines['bottom'].set_visible(False)

    return fig5


import seaborn as sns


def seaborn_plot(df_col, live, lower, upper):
    x = np.array(df_col)
    fig, ax = plt.subplots(figsize=(1.5, 0.4))
    plt.setp(ax.get_yticklabels()[0], visible=False)
    plt.tight_layout(pad=0, h_pad=0,)
    sns.despine(bottom=False, left=True)
    sns.color_palette("pastel")
    # sns.displot(data=x)
    # sns.scatterplot(data={'x': live,'y': 1}, x='x', y='y')
    sns.violinplot(data=x, orient='h', saturation=0.25, inner=None, color='r', cut=0.5, bw=0.1)
    plt.tick_params(left=False)
    plt.xlim(lower, upper)
    return fig

def linear_rescale(df):

    min_z = df.min().min()
    max_z = df.max().max()
    return min_z, max_z


def matplot_svg(fig):

    f = io.StringIO()
    fig.savefig(f, format="svg", transparent=True)
    svg_data = f.getvalue() # svg string
    return svg_data

import xml.dom.minidom

def main():
    df = pd.read_csv(r'/Users/Josh/Desktop/Bokeh Scripts/Iota/LinkerTimeSeries.csv')
    df.set_index('Date', inplace=True)
    bonds = df.columns
    live = 25
    for bond in bonds:
        box = seaborn_plot(df[bond], live=live)

    svg = matplot_svg(box)
    dom = xml.dom.minidom.parseString(svg)
    pretty_xml_as_string = dom.toprettyxml()
    print(pretty_xml_as_string)
