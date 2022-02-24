from dash import dash, dcc, dash_table, html
from dash.dependencies import Input, Output
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)

# Read Data
assay_results = pd.read_csv("./assay_results.csv")
labels = pd.read_csv("./compound_labels.csv")
IC50 = pd.read_csv("./compound_ic50.csv")


# Utility Methods for Data
def lineWeaverVo(record):
    record['1/Vo'] = 0.5 * (1 / record['Concentration (M)']) + 1 / record[' IC50 (M)']
    return record


def inverseConcentration(record):
    record['1/[s]'] = 1 / record['Concentration (M)']
    return record


# build dataframes
df_results = pd.merge(left=assay_results, right=labels, how='left', left_on='Compound ID', right_on='Compound ID')
df_results = pd.merge(left=df_results, right=IC50, how='left', left_on='Compound ID', right_on='Compound ID')
df_results["Compound ID"] = df_results["Compound ID"].astype(str)
grouped_data = df_results.groupby(['Compound ID', ' Assay Result Label', ' IC50 (M)'])['% Inhibition'].max().reset_index(name='Maximum % Inhibition')

line_weaver = df_results.groupby(['Compound ID', ' Assay Result Label', ' IC50 (M)', 'Concentration (M)']).apply(
    lineWeaverVo)
line_weaver = line_weaver.groupby(
    ['Compound ID', ' Assay Result Label', ' IC50 (M)', 'Concentration (M)', '1/Vo']).apply(inverseConcentration)


# instantiate main scatter plot
main_scatter = px.scatter(grouped_data, x="Maximum % Inhibition", y=" IC50 (M)", color=" Assay Result Label",
                          log_y=True, log_x=True, custom_data=["Compound ID", " Assay Result Label"])
main_scatter.update_traces(marker_size=20)
main_scatter.update_layout(
    clickmode='event',
    margin=dict(t=10, ),
)

app.layout = html.Div([

    html.Div([
        html.H2("Distribution of Compound by Assay Result", style={'text-align': 'center', 'line-height': 12, 'fontSize':'1.3em'}),
        html.P("Hover over an Assay Result Marker to see compound details on the right",
               style={'text-align': 'center'}),
        dcc.Graph(
            id='scatter-compound-category',
            style={"height": "89vh", "marginTop": 0, "paddingTop": 0},
            figure=main_scatter
        )]),
    html.Div([
        html.H2("Compound Activity Details", style={'text-align': 'center', 'line-height': 12, 'fontSize':'1.3em'}),
        html.P("A very rough attempt at a Line-weaver (guessing inhibition type) and dose-response curve",
               style={'text-align': 'center'}),
            dcc.Graph(
                id='scatter-compound-level',
                style={"height": "42vh", "marginTop": 0, "paddingTop": 0},
            ),
            dcc.Graph(
                id='line-log',
                style={"height": "46vh", "marginTop": 0, "paddingTop": 0},
            )
    ])
], style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'height': '96vh', 'boxSizing': 'borderBox'})


@app.callback(
    Output('line-log', 'figure'),
    Input('scatter-compound-category', 'hoverData'))
def update_individual_compound_line(hoverData):
    rows_with_compound = df_results[(df_results['Compound ID'] == '1')] if hoverData is None else df_results[
        (df_results['Compound ID'] == hoverData['points'][0]['customdata'][0])]
    fig = px.line(rows_with_compound, x="Concentration (M)", y="% Inhibition", color='Compound ID', log_x=True,
                  markers=True,
                  range_x=(
                  rows_with_compound["Concentration (M)"].min(), rows_with_compound["Concentration (M)"].max()))
    fig.update_layout(
        margin=dict(t=10,),
    )
    return fig


@app.callback(
    Output('scatter-compound-level', 'figure'),
    Input('scatter-compound-category', 'hoverData'))
def update_sad_lineweaver_plot(hoverData):
    rows_with_compound = line_weaver[(line_weaver['Compound ID'] == '1')] if hoverData is None else line_weaver[
        (line_weaver['Compound ID'] == hoverData['points'][0]['customdata'][0])]
    fig = px.scatter(rows_with_compound, x="1/[s]", y="1/Vo", log_y=True,
                     color="Compound ID",
                     hover_name="Compound ID")

    fig.update_traces(mode='lines+markers')
    fig.update_xaxes(showgrid=False,
                     range=[0 - rows_with_compound[" IC50 (M)"].unique() * 5, rows_with_compound["1/[s]"].max() * 1.25])
    fig.update_yaxes(type='linear', range=[-10, rows_with_compound["1/Vo"].max() * 1.25])
    fig.update_layout(
        margin=dict(t=0, b=0),
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
