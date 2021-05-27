import pandas as pd
from bokeh.embed import components
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    LassoSelectTool,
    PointDrawTool,
    WheelZoomTool,
)
from bokeh.palettes import Category20, Category20c, Spectral6
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.transform import cumsum
from django.http import HttpResponse
from django.shortcuts import render
from numpy import pi

from database.models import PesticidalProteinDatabase
from graphs.models import Products

# def graphs_home(request):
#     first_graph = "My first bokeh graph will be rendered on this page"
#     return HttpResponse(first_graph)


def protein_table(request):
    context = {"proteins": PesticidalProteinDatabase.objects.all()}
    return render(request, "graphs/proteintable.html", context)


def starter(request):
    plot = figure()
    plot.circle([1, 10, 35, 27], [0, 0, 0, 0], size=20, color="blue")

    script, div = components(plot)

    return render(
        request, "graphs/starter.html", {"script": script, "div": div}
    )


def graphs_home(request):
    x = [1, 2, 3, 4, 5]
    y = [6, 10, 2, -4, 10]
    title = "My Leaning Graphs"

    plot = figure(
        title=title,
        x_axis_label="High and Lows",
        y_axis_label="Learning Topics",
        plot_width=700,
        plot_height=700,
        tools="",
        toolbar_location=None,
    )

    # Formating Graph
    cr = plot.circle(
        x,
        y,
        size=10,
        color="blue",
        fill_color="grey",
        hover_fill_color="firebrick",
        line_color=None,
        hover_line_color="white",
    )

    plot.add_tools(
        HoverTool(tooltips=None, renderers=[cr], mode="hline")
    )
    plot.title.text_font_size = "20pt"
    plot.line(
        x,
        y,
        legend_label="Leaning Line",
        line_width=4,
        line_color="brown",
        line_dash="dashed",
    )
    plot.background_fill_color = "lightgrey"
    plot.border_fill_color = "whitesmoke"
    plot.min_border_left = 40
    plot.min_border_right = 40
    plot.outline_line_width = 7
    plot.outline_line_alpha = 0.2
    plot.outline_line_color = "purple"

    # Store components
    script, div = components(plot)

    return render(
        request, "graphs/home.html", {"script": script, "div": div}
    )


def combo(request):

    # prepare some data
    x = [0.1, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    # using list comprehension to create 3 other data sets
    y0 = [i ** 2 for i in x]
    y1 = [10 ** i for i in x]
    y2 = [10 ** (i ** 2) for i in x]

    # create a new plot
    p = figure(
        tools="pan,wheel_zoom,box_zoom,reset, hover, tap, crosshair",  # this gives us our tools
        y_axis_type="log",
        y_range=[0.001, 10 ** 11],
        title="log axis example",
        x_axis_label="sections",
        y_axis_label="particles",
    )

    # add some renderers
    p.line(x, x, legend_label="y=x")  # thin blue line
    p.circle(
        x, x, legend_label="y=x", fill_color="white", size=8
    )  # adds circles to y=x line
    p.line(x, y0, legend_label="y=x^2", line_width=3)  # thick blue line
    p.line(x, y1, legend_label="y=10^x", line_color="red")  # red line
    p.circle(
        x,
        y1,
        legend_label="y=10^x",
        fill_color="red",
        line_color="red",
        size=6,
    )  # adds red circles
    p.line(
        x,
        y2,
        legend_label="y=10^x^2",
        line_color="orange",
        line_dash="4 4",
    )  # orange dotted line

    script, div = components(p)

    return render(
        request, "graphs/combo.html", {"script": script, "div": div}
    )


def programming(request):

    # language = ['Python', 'JavaScript', 'C#', 'PHP', 'C++', 'Java']
    # counts = [25, 30, 8, 22, 12, 17]
    histo = {
        "A": 21,
        "C": 0,
        "D": 26,
        "E": 37,
        "F": 14,
        "G": 28,
        "H": 3,
        "I": 39,
        "K": 43,
        "L": 44,
        "M": 11,
        "N": 19,
        "P": 9,
        "Q": 22,
        "R": 15,
        "S": 24,
        "T": 20,
        "V": 20,
        "W": 3,
        "Y": 10,
    }
    # fixed_list = [x.items() for x in list(histo)]
    # keys,values = zip(*fixed_list)
    keys, values = zip(*histo.items())
    language = list(keys)
    counts = list(values)
    print("language", language)
    print("counts", counts)

    p = figure(
        x_range=language,
        plot_height=1000,
        plot_width=1000,
        title="Aminoacid histogram",
        toolbar_location="below",
        tools="pan, wheel_zoom, box_zoom, reset, hover, tap, crosshair",
    )
    # Spectral =

    source = ColumnDataSource(
        data=dict(
            language=language, counts=counts, color=Category20[20]
        )
    )
    p.add_tools(LassoSelectTool())
    p.add_tools(WheelZoomTool())

    p.vbar(
        x="language",
        top="counts",
        width=0.8,
        color="color",
        legend_group="language",
        source=source,
    )
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"

    # p.xgrid.grid_line_color = "black"
    p.y_range.start = 0
    # p.line(x=language, y= counts, color="black", line_width=2)
    # p.line(x=language, y= counts, color="black", line_width=2)

    script, div = components(p)

    return render(
        request,
        "graphs/programming.html",
        {"script": script, "div": div},
    )
    # return render(request, 'graphs/programming.html')


def multiplot(request):

    from bokeh.models import Range1d

    # create some data
    x1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y1 = [0, 8, 2, 4, 6, 9, 5, 6, 25, 28, 4, 7]
    x2 = [2, 5, 7, 15, 18, 19, 25, 28, 9, 10, 4]
    y2 = [2, 4, 6, 9, 15, 18, 0, 8, 2, 25, 28]
    x3 = [0, 1, 0, 8, 2, 4, 6, 9, 7, 8, 9]
    y3 = [0, 8, 4, 6, 9, 15, 18, 19, 19, 25, 28]

    # select the tools we want
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

    # the red and blue graphs will share this data range
    xr1 = Range1d(start=0, end=30)
    yr1 = Range1d(start=0, end=30)

    # only the green will use this data range
    xr2 = Range1d(start=0, end=30)
    yr2 = Range1d(start=0, end=30)

    # build our figures
    p1 = figure(
        x_range=xr1,
        y_range=yr1,
        tools=TOOLS,
        plot_width=600,
        plot_height=300,
    )
    p1.scatter(
        x1, y1, size=12, color="red", alpha=0.5, legend_label="Bread"
    )

    p2 = figure(
        x_range=xr1,
        y_range=yr1,
        tools=TOOLS,
        plot_width=600,
        plot_height=300,
    )
    p2.scatter(
        x2, y2, size=12, color="blue", alpha=0.5, legend_label="Milk"
    )

    p3 = figure(
        x_range=xr2,
        y_range=yr2,
        tools=TOOLS,
        plot_width=600,
        plot_height=300,
    )
    p3.scatter(
        x3, y3, size=12, color="green", alpha=0.5, legend_label="Tofu"
    )

    # plots can be a single Bokeh Model, a list/tuple, or even a dictionary
    plots = {"Red": p1, "Blue": p2, "Green": p3}

    script, div = components(plots)

    return render(
        request, "graphs/multiplot.html", {"script": script, "div": div}
    )


def products(request):

    shoes = 0
    belts = 0
    shirts = 0
    counts = []
    items = ["Shoes", "Belts", "Shirts"]
    prod = Products.objects.values()

    for i in prod:
        if "Shoes" in i.values():
            shoes += 1
        elif "Belts" in i.values():
            belts += 1
        elif "Shirts" in i.values():
            shirts += 1
    counts.extend([shoes, belts, shirts])

    plot = figure(
        x_range=items,
        plot_height=600,
        plot_width=600,
        title="Products",
        toolbar_location="right",
        tools="pan,wheel_zoom,box_zoom,reset, hover, tap, crosshair",
    )
    plot.title.text_font_size = "20pt"

    plot.xaxis.major_label_text_font_size = "14pt"
    plot.vbar(
        items,
        top=counts,
        width=0.4,
        color="firebrick",
        legend_label="Product Counts",
    )
    plot.legend.label_text_font_size = "14pt"

    script, div = components(plot)

    return render(
        request, "graphs/products.html", {"script": script, "div": div}
    )


def pie(request):

    x = {
        "United States": 157,
        "United Kingdom": 93,
        "Japan": 89,
        "China": 63,
        "Germany": 44,
        "India": 42,
        "Italy": 40,
        "Australia": 35,
        "Brazil": 32,
        "France": 31,
        "Taiwan": 31,
        "Spain": 29,
    }

    data = (
        pd.Series(x)
        .reset_index(name="value")
        .rename(columns={"index": "country"})
    )
    data["angle"] = data["value"] / data["value"].sum() * 2 * pi
    data["color"] = Category20c[len(x)]

    p = figure(
        plot_height=600,
        plot_width=800,
        title="Pie Chart",
        toolbar_location=None,
        tools="hover",
        tooltips="@country: @value",
    )

    p.wedge(
        x=0,
        y=1,
        radius=0.4,
        start_angle=cumsum("angle", include_zero=True),
        end_angle=cumsum("angle"),
        line_color="royalblue",
        fill_color="color",
        legend_group="country",
        source=data,
    )

    script, div = components(p)

    return render(
        request, "graphs/pie.html", {"script": script, "div": div}
    )


def test_html(request):

    plot1 = figure()
    plot1.circle([1, 10, 35, 27], [2, 0, 45, 0], size=20, color="blue")

    plot2 = figure()
    plot2.circle([1, 10, 35, 27], [3, 25, 3, 44], size=20, color="blue")

    plots = [plot1, plot2]

    (
        script,
        div,
    ) = components(plots, CDN)
    # script, divs = test_html(request)
    # return render(request, 'test_html.html', {'script': script, 'div':div})

    # return render(request, 'test_html.html', script=script, div_plot1=divs['plot1'], div_plot2=divs['plot2'])
    return render(
        request, "graphs/test_html.html", {"script": script, "div": div}
    )
