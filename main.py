# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
from data import countries_df, totals_df, dropdown_options,make_global_df,make_country_df
from builder import make_table


stylesheets = ["https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.min.css"]

app = Dash(__name__, external_stylesheets=stylesheets)


bubble_map = px.scatter_geo(countries_df,
                     template="plotly_dark",
                     title="Confirmed By Country",
                     color_continuous_scale=px.colors.sequential.Pinkyl,
                     size="Confirmed",
                     size_max=50,
                     locations="Country_Region", 
                     locationmode='country names', 
                     color = "Confirmed", 
                     hover_name = "Country_Region", 
                     projection="natural earth",
                     hover_data = {
                         "Confirmed":":,.0f", 
                         "Deaths":":,.0f", 
                         "Recovered":":,.0f", 
                         "Country_Region":False
                     })

bubble_map.update_layout(
    margin=dict(l=0, r=0, t=50, b=0), coloraxis_colorbar=dict(xanchor="left", x=0)
)


bars_graph = px.bar(
    totals_df, 
    color=["Confirmed", "Deaths", "Recovered"],
    x="conditions", 
    y="count", 
    hover_data={'count':":,"},
    template="plotly_dark", 
    title="Total Global Cases",
    color_discrete_map={"Confirmed": "#ffeaa7", "Deaths": "#d63031", "Recovered": "#00b894"},
    labels={"condition":"Condition", "count":"Count", "color":"Condition"},
    )



app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "backgroundColor": "#111111",
        "color": "white",
        "fontFamily": "Open Sans, sans-serif",
    },
    children=[
        html.Header(
            style={"textAlign": "center", "paddingTop": "50px"},
            children=[html.H1("Corona Dashboard", style={"fontSize": 40})],
        ),
        html.Div(
            style={"display":"grid", "gap" : 50, "gridTemplateColumns":"repeat(5,1fr)"},
            children=[
                html.Div(style={"grid-column":"span 4"}, children=[dcc.Graph(figure=bubble_map)]),
                html.Div(
                    children=[
                        html.Table(
                            children=[
                                make_table(countries_df)
                            ]
                        )
                    ]
                )
            ]
        ),
        html.Div(
            style={"display":"grid", "gap" : 50, "gridTemplateColumns":"repeat(4,1fr)"},
            children=[
                html.Div(style={"grid-column":"span 1"}, children=[dcc.Graph(figure=bars_graph)]),
                html.Div(
                    style={"grid-column":"span 3"},
                    children=[
                        dcc.Dropdown( style={
                                "width": 320,
                                "margin": "0 auto",
                                "color": "#111111",
                            },
                            placeholder="Select a Country",
                            id="country", 
                            options=[
                            {'label':country, 'value':country} for country in dropdown_options
                        ]),
                        dcc.Graph(id="country_graph")
                    ]
                )
            ]
        ),
    ],
)


@app.callback(
    Output("country_graph","figure"),[Input("country", "value")])
def update_hello(value):
    if value:
        df = make_country_df(value)
    else:
        df = make_global_df()
    fig = px.line(
        df, 
        x="date",
        y=["confirmed", "deaths", "recovered"], 
        template="plotly_dark",
        labels={"value":"Cases","variable":"Condition","date":"Date"},
        hover_data={"value":":,","variable":False,"date":False})
    
    fig.update_xaxes(rangeslider_visible=True)
    fig["data"][0]["line"]["color"] = "#ffeaa7"
    fig["data"][1]["line"]["color"] = "#d63031"
    fig["data"][2]["line"]["color"] = "#00b894"
    return fig