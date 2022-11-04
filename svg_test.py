from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, TableColumn, DataTable, HTMLTemplateFormatter
from bokeh.io import show
import pandas as pd

df = pd.DataFrame({
    'SubjectID': ['Subject_01', 'Subject_02', 'Subject_03'],
    'Result_1': ['Positive', 'Negative', 'Negative'],
    'Result_2': ['Negative', 'Negative', 'Negative'],
    'Result_3': ['Negative', 'Invalid', 'Positive'],
    'Result_4': ['Positive', 'Negative', 'Negative'],
    'Result_5': ['Positive', 'Positive', 'Negative'],
    'Result_6': ['Positive', 'Negative', 'Negative'],
    'Result_7': ['Invalid', 'Negative', 'Negative'],
    'Result_8': ['Negative', 'Invalid', 'Positive'],
    'Result_9': ['Positive', 'Positive', 'Positive'],
    'Result_10': ['Positive', 'Positive', 'Negative'],
    'Result_11': ['Negative', 'Negative', 'Negative'],
    'Result_12': ['Negative', 'Negative', 'Negative'],
    'Result_13': ['Negative', 'Invalid', 'Positive'],
    'Result_14': ['Positive', 'Negative', 'Invalid'],
    'Result_15': ['Negative', 'Positive', 'Negative']
})


def get_html_results(r1, r2, r3, r4, r5):
    def get_block(my_color):
        return '<span style="color:{};font-size:18pt;text-shadow: 1px 1px 2px #000000;">&#9632;</span>'.format(my_color)

    dict_color = {'Positive': '#f14e08', 'Negative': '#8a9f42', 'Invalid': '#8f6b31'}

    html_string = ""

    for r in [r1, r2, r3, r4, r5]:
        html_string += get_block(dict_color.get(r))

    return html_string


def get_html_results(r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15):
    def get_svg_rect(result, position):
        dict_color = {'Positive': '#f14e08', 'Negative': '#8a9f42', 'Invalid': '#8f6b31'}

        y_off = (position) // 5
        x_off = (position) % 5

        ini_x = 5
        ini_y = 0

        my_text = """
        <rect x="{}" y="{}" rx="0" ry="0" width="6" height="6"
        style="fill:{};stroke:black;stroke-width:0;opacity:1;" />
        """.format(ini_x + x_off * 7, ini_y + y_off * 7, dict_color.get(result))

        return my_text

    html_text = ""
    for index, r in enumerate([r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15]):
        html_text += get_svg_rect(r, index)

    svg_text = '<svg width="40" height="20">{}</svg>'.format(html_text)

    return svg_text


def get_html_curve(plot_width, plot_height, mycolor):
    svg_points = """
    0.8 17.69,1.6 17.72,2.4 17.74,3.2 17.75,4.0 17.76,4.8 17.79,5.6 17.79,6.4 17.80,7.2 17.80,8.0 	17.81,8.8 17.81, 9.6 17.83,10.4 17.83,11.2 17.83,12.0 17.83,12.8 17.85,13.6 17.84,14.4 17.84,15.2 17.85,16.0 17.85,16.8 17.85, 17.6 17.85,18.4 17.84,19.2 17.83,20.0 17.82,20.8 17.76,21.6 17.67,22.4 17.49,23.2 17.15,24.0 16.54,24.8 15.48, 25.6 13.90,26.4 12.08,27.2 10.37,28.0 8.94,28.8 7.82,29.6 6.97,30.4 6.37,31.2 5.94,32.0 5.68,32.8 5.51,33.6 5.41, 34.4 5.34,35.2 5.29,36.0 5.25,36.8 5.22,37.6 5.20,38.4 5.18,39.2 5.17,40.0 5.15
    """

    svg_curve = """
    <svg width="{}" height="{}">
      <rect x="0" y="0" rx="0" ry="0" width="{}" height="{}"
      style="fill:white;stroke:darkgrey;stroke-width:1;opacity:0.5;" />
      <polyline points="{}" style="fill:none;stroke:{};stroke-width:1" />
    </svg>
    """.format(plot_width, plot_height, plot_width, plot_height, svg_points, mycolor)

    return svg_curve


df['Results'] = [get_html_results(r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15) \
                 for r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15 \
                 in zip(df['Result_1'], df['Result_2'], df['Result_3'], df['Result_4'], df['Result_5'],
                        df['Result_6'], df['Result_7'], df['Result_8'], df['Result_9'], df['Result_10'],
                        df['Result_11'], df['Result_12'], df['Result_13'], df['Result_14'], df['Result_15'])]

df['Curve'] = [get_html_curve(40, 20, mycolor) for mycolor in ['orangered', 'forestgreen', 'purple']]


print(df.head())


source = ColumnDataSource(df[['SubjectID', 'Results', 'Curve']])

formatter = HTMLTemplateFormatter()

columns = [
    TableColumn(field='SubjectID', title='SubjectID'),
    TableColumn(field='Results', title='Results', formatter=formatter),
    TableColumn(field='Curve', title='PCR curve preview', formatter=formatter)
]


myTable = DataTable(source=source, columns=columns)

# show(myTable)