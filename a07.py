"""
LINK TO DEPLOYED DASHBOARD: https://assignment-7-myfr.onrender.com/
"""

import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import pandas as pd

world_cup_finals = [
    {"year": 1930, "winner": "Uruguay", "runner_up": "Argentina"},
    {"year": 1934, "winner": "Italy", "runner_up": "Czechoslovakia"},
    {"year": 1938, "winner": "Italy", "runner_up": "Hungary"},
    {"year": 1950, "winner": "Uruguay", "runner_up": "Brazil"},
    {"year": 1954, "winner": "West Germany", "runner_up": "Hungary"},
    {"year": 1958, "winner": "Brazil", "runner_up": "Sweden"},
    {"year": 1962, "winner": "Brazil", "runner_up": "Czechoslovakia"},
    {"year": 1966, "winner": "England", "runner_up": "West Germany"},
    {"year": 1970, "winner": "Brazil", "runner_up": "Italy"},
    {"year": 1974, "winner": "West Germany", "runner_up": "Netherlands"},
    {"year": 1978, "winner": "Argentina", "runner_up": "Netherlands"},
    {"year": 1982, "winner": "Italy", "runner_up": "West Germany"},
    {"year": 1986, "winner": "Argentina", "runner_up": "West Germany"},
    {"year": 1990, "winner": "West Germany", "runner_up": "Argentina"},
    {"year": 1994, "winner": "Brazil", "runner_up": "Italy"},
    {"year": 1998, "winner": "France", "runner_up": "Brazil"},
    {"year": 2002, "winner": "Brazil", "runner_up": "Germany"},
    {"year": 2006, "winner": "Italy", "runner_up": "France"},
    {"year": 2010, "winner": "Spain", "runner_up": "Netherlands"},
    {"year": 2014, "winner": "Germany", "runner_up": "Argentina"},
    {"year": 2018, "winner": "France", "runner_up": "Croatia"},
    {"year": 2022, "winner": "Argentina", "runner_up": "France"},
]

df_finals = pd.DataFrame(world_cup_finals)
df_finals['winner'] = df_finals['winner'].replace("West Germany", "Germany")
df_finals['runner_up'] = df_finals['runner_up'].replace("West Germany", "Germany")
df_winners_count = df_finals['winner'].value_counts().reset_index()
df_winners_count.columns = ['country', 'wins']
all_winning_countries = df_winners_count['country'].tolist()

fig_choropleth = go.Figure(
    data=go.Choropleth(
        locations=df_winners_count['country'],
        locationmode='country names',
        z=df_winners_count['wins'],
        colorscale='Blues',
        colorbar_title='Number of Wins'
    )
)
fig_choropleth.update_layout(
    title='FIFA World Cup Wins by Country',
    geo=dict(showframe=False, showcoastlines=False)
)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("FIFA World Cup Dashboard", style={'textAlign': 'center'}),
    html.Div([
        html.H3("All Countries That Have Won the World Cup:"),
        html.Div(", ".join(all_winning_countries), id="display-winning-countries")
    ], style={'margin-bottom': '20px'}),
    html.Div([
        html.H3("Select a Country to See How Many Times It Has Won:"),
        dcc.Dropdown(
            id="country-dropdown",
            options=[{"label": c, "value": c} for c in all_winning_countries],
            value="Brazil",
            clearable=False
        ),
        html.Div(id="country-win-output", style={'margin-top': '10px', 'font-weight': 'bold'})
    ], style={'margin-bottom': '20px'}),
    html.Div([
        html.H3("Select a Year to See the Winner and Runner-Up:"),
        dcc.Dropdown(
            id="year-dropdown",
            options=[{"label": row['year'], "value": row['year']} for _, row in df_finals.iterrows()],
            value=2022,
            clearable=False
        ),
        html.Div(id="year-final-output", style={'margin-top': '10px', 'font-weight': 'bold'})
    ], style={'margin-bottom': '20px'}),
    html.Div([
        dcc.Graph(id='world-cup-choropleth', figure=fig_choropleth)
    ])
])

server = app.server

@app.callback(
    Output("country-win-output", "children"),
    Input("country-dropdown", "value")
)
def update_country_win_output(selected_country):
    if selected_country in df_winners_count['country'].values:
        wins = df_winners_count.loc[df_winners_count['country'] == selected_country, 'wins'].iloc[0]
        return f"{selected_country} has won the World Cup {wins} time(s)."
    else:
        return "No data available."

@app.callback(
    Output("year-final-output", "children"),
    Input("year-dropdown", "value")
)
def update_year_final_output(selected_year):
    row = df_finals.loc[df_finals['year'] == selected_year]
    if not row.empty:
        winner = row['winner'].iloc[0]
        runner_up = row['runner_up'].iloc[0]
        return f"For {selected_year}, Winner: {winner}, Runner-Up: {runner_up}."
    else:
        return "Year not found in data."


