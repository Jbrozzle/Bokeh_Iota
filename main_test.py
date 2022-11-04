# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.



from bokeh.models import DataTable, ColumnDataSource, TableColumn,\
    HTMLTemplateFormatter, Patch, CustomJS
from bokeh.layouts import column, row
from boxplot import *
from bokeh.io import curdoc
import pandas as pd
import numpy as np
from bokeh.plotting import figure, show



class BokehApp:

    def __init__(self, type, data, formatters=[], tools=[], x_col='', y_col='', height=200, width=200):
        self.app_type = type
        self.src = data
        self.formatters = formatters
        self.tools = tools
        self.x_col = x_col if x_col is not None else 0
        self.y_col = y_col if y_col is not None else 0
        self.width = width
        self.height = height

    def create_plot(self, data, subtype, fit_line, patch):
        source = ColumnDataSource(data={'x_values': data[self.x_col],
                                        'y_values': data[self.y_col]})
        plot = figure(width=self.width, height=self.height)
        if subtype == 'line':
            xvals = np.array(pd.to_datetime(data[self.x_col], format="%d/%m/%Y"))
            source = ColumnDataSource(data={'x_values': xvals,
                                            'y_values': data[self.y_col]})
            plot = figure(width=self.width, height=self.height, x_axis_type='datetime')
            if patch:
            #do patch work here for standard deviations, make dynamic with slide widgets
                selected_z = 1.5
                selected_lookback = 90
                upper = [i + selected_z*data[self.y_col][max([0, (idx-selected_lookback)]):idx].std()
                         for idx, i in enumerate(data[self.y_col])][2:]
                lower = [i - selected_z*data[self.y_col][max([0, (idx-selected_lookback)]):idx].std()
                         for idx, i in enumerate(data[self.y_col])][2:]
                patch_y_vals = np.hstack((upper, lower))
                patch_x_vals = np.hstack((xvals[2:], xvals[2:][::-1]))
                patch_source = ColumnDataSource(data={'x_values': patch_x_vals,
                                                'y_values': patch_y_vals})
                glyph = Patch(x="x_values", y="y_values", fill_color="green", fill_alpha=0.5, line_width=0)
                plot.add_glyph(patch_source, glyph)
            plot.line(x='x_values', y='y_values', source=source, line_width=2)
            plot.xaxis.axis_label, plot.yaxis.axis_label = self.x_col, self.y_col
            if fit_line:
                poly_coefs = np.polyfit(data[self.x_col], data[self.y_col], 3)
                poly_vals = np.polyval(poly_coefs, np.array(data[self.x_col]))
                plot.line(x=data[self.x_col], y=poly_vals)
        if subtype == "scatter":
            plot.scatter(x='x_values', y='y_values', source=source)
            plot.xaxis.axis_label, plot.yaxis.axis_label = self.x_col, self.y_col
            if fit_line:
                poly_coefs = np.polyfit(data[self.x_col], data[self.y_col], 3)
                poly_vals = np.polyval(poly_coefs, np.array(data[self.x_col]))
                plot.line(x=data[self.x_col], y=poly_vals)
                patch_source=None
        if subtype == "vbar":
            plot.vbar(x='x_values', y='y_values', source=source)
            patch_source = None

        return plot, source, patch_source

    def create_widget(self, data, columns):
        source = ColumnDataSource(data)
        if self.app_type == DataTable:
            data_table = DataTable(source=source, columns=columns, width=self.width, height=self.height, autosize_mode='none')

            return data_table, source

    def create_callback(self, data, widget):
        pass

class CallBack():
    def __init__(self, type, in_widget, out_plot):
        self.type = type
        self.in_widget = in_widget
        self.out_plot = out_plot



def launch(layout_object, server):

    if server:
        curdoc().add_root(layout_object)
    else:
        show(layout_object)

def main():

    linker_path = r'/Users/Josh/Desktop/Bokeh Scripts/Iota/LinkerList.csv'
    dt_formatters = [HTMLTemplateFormatter()]
    dt_tools =['']

    plt_formatters =['']
    plt_tools =[]
    live_df = pd.read_csv(linker_path)
    main_scatter = BokehApp(figure(), live_df, plt_formatters, plt_tools,
                             x_col="Maturity", y_col='Z spread', width=400, height=400)
    scatter_plot, scatter_ds, scatter_patch_ds = main_scatter.create_plot(main_scatter.src, "scatter", fit_line=True, patch=False)
    raw_df = pd.read_csv(r'/Users/Josh/Desktop/Bokeh Scripts/Iota/LinkerTimeSeries.csv')
    raw_df.set_index('Date', inplace=True)
    bonds = raw_df.columns
    lives = list(live_df['Z spread'])
    lower, upper = linear_rescale(raw_df)
    box_list = [matplot_box(raw_df[bond], lives[idx], lower, upper) for idx, bond in enumerate(bonds)]
    sns_list = [seaborn_plot(raw_df[bond], lives[idx], lower, upper) for idx, bond in enumerate(bonds)]
    svg_list = [matplot_svg(box) for box in box_list]
    table_df = pd.read_csv(linker_path)
    table_df['SVG'] = svg_list
    html_formatter = HTMLTemplateFormatter()

    dt_columns = [
                TableColumn(field="Linker", title="Linker", width=50),
                TableColumn(field="Z spread", title="Z Spread", width=75),
                TableColumn(field='SVG', title='SVG curve', formatter=html_formatter, width=200)
            ]

    main_table = BokehApp(DataTable, table_df, dt_formatters, dt_tools, height=1000, width=325)
    table, table_ds = main_table.create_widget(main_table.src, columns=dt_columns)

    hist_chart = BokehApp(figure(), pd.read_csv(r'/Users/Josh/Desktop/Bokeh Scripts/Iota/LinkerTimeSeries.csv').dropna(), plt_formatters, plt_tools,
                             x_col='Date', y_col='IL26', width=400, height=400)
    hist_chart_plot, hist_chart_ds, hist_patch_ds = hist_chart.create_plot(hist_chart.src, "line", fit_line=False, patch=True)
    #Datable callback
    source_code = """
     var grid = document.getElementsByClassName('grid-canvas')[0].children;
     var row, column = '';

     for (var i = 0,max = grid.length; i < max; i++){
         if (grid[i].outerHTML.includes('active')){
             row = i;
             for (var j = 0, jmax = grid[i].children.length; j < jmax; j++)
                 if(grid[i].children[j].outerHTML.includes('active')) 
                     { column = j }
         }
     }
     
     console.log(row)
     const new_data = Object.assign({}, row_col.data)
     new_data.row = [row]
     row_col.data = new_data;

     """
    row_col_dict = {'row': [0], 'col_1': [0]}
    row_col = ColumnDataSource(row_col_dict)
    callback = CustomJS(args=dict(source=table_ds, row_col=row_col), code=source_code)
    table_ds.selected.js_on_change('indices', callback)

    def py_callback(attr, old, new):
        selected_index = (row_col.data)['row']
        new_y_col = bonds[selected_index]
        df = pd.read_csv(r'/Users/Josh/Desktop/Bokeh Scripts/Iota/LinkerTimeSeries.csv').dropna()
        xvals = np.array(pd.to_datetime(df['Date'], format="%d/%m/%Y"))
        yvals = np.array(df[new_y_col])
        new_data = {'x_values':xvals, 'y_values': yvals}
        hist_chart_ds.data = new_data
        selected_z = 1.5
        selected_lookback = 90

        # upper = [i + selected_z * df[new_y_col][max([0, (idx - selected_lookback)]):idx].std()
        #          for idx, i in enumerate(df[new_y_col])][2:]
        # lower = [i - selected_z * df[new_y_col][max([0, (idx - selected_lookback)]):idx].std()
        #          for idx, i in enumerate(df[new_y_col])][2:]

        upper = [i + selected_z * yvals[max([0, (idx - selected_lookback)]):idx].std()
                 for idx, i in enumerate(yvals)][2:]
        lower = [i - selected_z * yvals[max([0, (idx - selected_lookback)]):idx].std()
                 for idx, i in enumerate(yvals)][2:]

        print(lower)
        print(xvals)

        patch_y_vals = np.hstack((upper, lower))
        print(patch_y_vals)
        #here need to pull out list items outside of the list on patch y vals
        # patch_y_vals =
        patch_x_vals = np.hstack((xvals[2:], xvals[2:][::-1]))
        print(patch_x_vals)
        new_patch_data = {'x_values':patch_x_vals, 'y_values':patch_y_vals}
        hist_patch_ds.data = new_patch_data

    table_ds.selected.on_change('indices', py_callback)

    rw = row(scatter_plot, table, hist_chart_plot)

    curdoc().title = "Iota RV Tool"
    curdoc().add_root(rw)
    show(rw)
    # launch(col, server=False)


main()
# if __name__ == '__main__':
#     main()
