import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

DATA_URL = "https://raw.githubusercontent.com/asifikbalpro/Applied-Data-Science-Capstone/main/dataset_part_2.csv"
df = pd.read_csv(DATA_URL)

app = Dash(__name__)
sites = ["ALL"] + sorted(df["LaunchSite"].dropna().unique().tolist())

app.layout = html.Div([
    html.H1("SpaceX Launch Records Dashboard"),
    dcc.Dropdown(
        id="site-dropdown",
        options=[{"label":"All Sites","value":"ALL"}] +
                [{"label":s,"value":s} for s in sites[1:]],
        value="ALL", clearable=False
    ),
    dcc.Graph(id="success-pie"),
    dcc.RangeSlider(
        id="payload-slider",
        min=float(df["PayloadMass"].min()),
        max=float(df["PayloadMass"].max()),
        step=500,
        value=[float(df["PayloadMass"].min()), float(df["PayloadMass"].max())]
    ),
    dcc.Graph(id="payload-scatter")
])

@app.callback(
    Output("success-pie","figure"),
    Output("payload-scatter","figure"),
    Input("site-dropdown","value"),
    Input("payload-slider","value")
)
def update_dashboard(site, payload_range):
    filtered = df[(df["PayloadMass"] >= payload_range[0]) &
                  (df["PayloadMass"] <= payload_range[1])].copy()
    if site != "ALL":
        filtered = filtered[filtered["LaunchSite"] == site]

    pie_df = filtered["Class"].value_counts().rename_axis("Class").reset_index(name="Count")
    pie = px.pie(pie_df, names="Class", values="Count", title="Landing outcome distribution")
    scatter = px.scatter(filtered, x="FlightNumber", y="PayloadMass",
                         color="Class", hover_data=["LaunchSite","Orbit"],
                         title="Payload mass vs flight number")
    return pie, scatter

if __name__ == "__main__":
    app.run(debug=True)
