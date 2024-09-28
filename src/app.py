from os import environ

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from flask import Flask
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pandas.api.types import is_numeric_dtype

import numpy as np
import webbrowser


descriptors = ['Adults', 'Youth', 'Female', 'Male',
       'Gender Diverse', 'Indigenous', 'Caucasian', 'People of Colour',
       'Rough Sleepers', 'Veterans']

food = ['Sandwiches', 'Bottled Water',
       'Other Drinks (fizzy water, juice, pop, etc)',
       'Meal Replacement Drinks (Ensure, Boost, Protein Drinks, etc...)',
       'Protein Snacks (beef jerky, pepperoni, etc...)',
       'Baked Goods (cookies, cakes, Rice Krispies Squares, etc)',
       'Chips, Crackers, etc',
       'Electrolytes, etc (Gatorade, electrolyte powder, Emergen-C)',
       'Canned Goods & Noodles (soup, chili, ravioli, etc...)',
       'Fruit (fresh, canned, fruit cups)',
       'Candy (chocolate, gummies, etc...)',
       'Other Snacks (popcorn, granola bars, etc...)']

hygiene_supplies = ['Hygiene Kits',
       'Dental Kits', 'Shaving Kits', 'Menstrual Product Kits',
       'Hand Sanitizer', 'Mini First Aid Kit', 'Wet Wipes']

clothing = ['Underwear',
       'Socks', 'Sweaters', 'Jackets', 'Long Johns', 'Hand/Foot warmers',
       'Hats (Toques in Winter/Baseball in summer)', 'Gloves']

harm_reduction = ['Bubbles', 'Naloxone', 'Straights', 'Longs', 'Shorts',
       'Foil', 'Sharps Disposal', 'Condoms/Dental Dams']

living_supplies = ['Emergency Blankets', 'Sunscreen/Petroleum Jelly',
       'Emergency Shelter.1', 'Tents', 'Tarps', 'Sleeping Bags', 'Blankets',
       'Ponchos', 'Backpacks/Tote Bags', 'Battery Packs',
       'Bus Tickets']

misc = ["Gift Cards"]

referrals = ['Detox/Treatment', 'Housing', 'Mental Health', 'ID Clinic',
       'Food Source', 'Harm Reduction', 'Medical',
       'Clothing Source', 'Legal', 'Financial', 'Employment', 'Youth.1',
       'Immigrant Services', 'Indigenous Services']

medical = ['Syringes/Paraphernalia Discarded', 'Police Called',
       'EMS Called', 'DOAP Called', 'First Aid Administered',
       'Naloxone Administered']

shift_info = ['Start Time', 'End Time', 'Team Lead', "Location"
       'Outreach Workers', 'Shift Notes']


category_dict = {
    "descriptors": descriptors,
    "food": food,
    "hygiene_supplies": hygiene_supplies,
    "clothing": clothing,
    "harm_reduction": harm_reduction,
    "living_supplies": living_supplies,
    "referrals": referrals,
    "medical": medical
}
categories = list(category_dict.keys())


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

server = Flask(__name__)
app = dash.Dash(
    server=server,
    url_base_pathname=environ.get("JUPYTERHUB_SERVICE_PREFIX", "/"),
    external_stylesheets=external_stylesheets,
)

app.layout = html.Div(
    [
        dcc.Dropdown(
            id="category",
            options=categories,
            value=categories[0],
        ),
        dcc.RadioItems(id="figure_type", options=['timeseries', 'bar'], value='timeseries'),
        dcc.Graph(id="figure"),
    ]
)

#webbrowser.open("http://0.0.0.0:8050/")

df = pd.read_csv("./data/daily_outreach_support.csv")
df = df.sort_values(by=["Date:"])

sum_categories = []
sums = []

for c in df.columns:
    if is_numeric_dtype(df[c]):
       sum_categories.append(c)
       sums.append(np.sum(df[c]))

sums = np.array(sums)


# can put the categories in a diff file so they're easier to change..
@app.callback(
    Output(component_id='figure', component_property='figure'),
    Input(component_id='category', component_property='value'),
    Input(component_id='figure_type', component_property='value'),
)
def update_figure(category, figure_type):
    category_elements = category_dict[category]

    if figure_type == "timeseries":
       figure = px.line(df, x="Date:", y=category_elements)
        
    elif figure_type == "bar":
       inds = [sum_categories[i] in category_elements for i in range(len(sum_categories))]
       figure = go.Figure([go.Bar(x=category_elements, y=sums[inds])])
    
    return figure



if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)