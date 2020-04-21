# Perform imports here:
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import plotly.figure_factory as ff
import pandas as pd

# Launch the application:
app = dash.Dash()
app.title = "Modern Warfare"
server = app.server

# 0-14 AR
# 14-25 SMG
# 25-30 LMG
# 30-36 Sniper
# 36-41 Pistol
# 41-45 Shotgun

# Create a DataFrame from the .csv file:
df = pd.read_excel('Warzone.xlsx')

arsenal = [{'label':'ARs', 'value':'ARs'}, {'label':'SMGs', 'value':'SMGs'}, {'label':'LMGs', 'value':'LMGs'}, {'label':'Snipers', 'value':'Snipers'}, {'label':'Pistols', 'value':'Pistols'}, {'label':'Shotguns', 'value':'Shotguns'}]
options = [{'label':'Damage', 'value':'Damage'}, {'label':'Rate of Fire', 'value':'Rate of Fire'}, {'label':'Damage per Second', 'value':'DPS'}, {'label':'Shots to Kill', 'value':'STK'}, {'label':'Time to Kill', 'value':'TTK'}, 
            {'label':'STK with 1 Sheild', 'value':'STK1'}, {'label':'TTK with 1 Sheild', 'value':'TTK1'}, {'label':'STK with 2 Sheild', 'value':'STK2'}, {'label':'TTK with 2 Sheild', 'value':'TTK2'}, {'label':'STK with 3 Sheild', 'value':'STK3'}, {'label':'TTK with 3 Sheild', 'value':'TTK3'}]
plots = [{'label':'Bar', 'value':'bar'}, {'label':'Line', 'value':'scatter'}]

fig = ff.create_distplot([df['Damage'], df['Rate of Fire'], df['DPS']], ['Damage', 'Rate of Fire', 'DPS'])

# Create a Dash layout that contains a Graph component:
app.layout = html.Div([
    html.H1('Warzone Statistics'),
    html.Div([
        html.H3('Select Arsenal:', style={'paddingRight':'30px'}),
        # replace dcc.Input with dcc.Options, set options=options
        dcc.Dropdown(
            id='select_gun',
            options=arsenal,
            value=['ARs','SMGs', 'LMGs', 'Snipers', 'Pistols', 'Shotguns'],
            multi=True
        )
    # widen the Div to fit multiple inputs
    ], style={'display':'inline-block', 'verticalAlign':'top', 'width':'20%', 'paddingRight':'20px'}),
    
    html.Div([
        html.H3('Select options'),
        dcc.Dropdown(
            id='select_option',
            options=options,
            value='Damage',
        )
    ], style={'display':'inline-block', 'verticalAlign':'top', 'width':'20%', 'paddingRight':'20px'}),
    
    html.Div([
        html.H3('Select Graph'),
        dcc.RadioItems(
            id='select_plot',
            options=[{'label': 'Bar', 'value': 'bar'}, {'label':'Line', 'value':'scatter'}, {'label':'Bubble', 'value':'bubble'}],
            value='bar'
            ),
    ], style={'display':'inline-block', 'verticalAlign':'top', 'width':'20%', 'paddingRight':'20px'}),

    dcc.Graph(
        id='main_plot',
        figure={
            'data': [
                {'x' : df['Guns'].iloc[0:14], 'y' : df['Damage'], 'type':'bar', 'name':'Assualt Rifles', 'opacity': '0.75'},
                {'x' : df['Guns'].iloc[14:25], 'y' : df['Damage'], 'type':'bar', 'name':'SMG', 'opacity': '0.75'},
                {'x' : df['Guns'].iloc[25:30], 'y' : df['Damage'], 'type':'bar', 'name':'LMG', 'opacity': '0.75'},
                {'x' : df['Guns'].iloc[30:36], 'y' : df['Damage'], 'type':'bar', 'name':'Snipers', 'opacity': '0.75'},
                {'x' : df['Guns'].iloc[36:41], 'y' : df['Damage'], 'type':'bar', 'name':'Pistols', 'opacity': '0.75'},
                {'x' : df['Guns'].iloc[41:45], 'y' : df['Damage'], 'type':'bar', 'name':'Shotguns', 'opacity': '0.75'}
            ],
            'layout' : go.Layout(
                title = 'Guns Damage',
                xaxis = {'title': 'Total Arsenal'},
                yaxis = {'title': 'Damage'},
                hovermode ='closest',
                height = 500
            )
        }
    ),
    
    html.H3('Box Plot'),

    dcc.Graph(
        id='box_plot',
        figure={
            'data': [
                {'y' : df['Rate of Fire'], 'type': 'box', 'name':'Damage', 'boxpoints':'all', '​jitter':0.3, 'pointpos':-1.8},
                {'y' : df['DPS'], 'type': 'box', 'name':'DPS', 'boxpoints':'all', '​jitter':0.3, 'pointpos':-1.8},
                {'y': df['TTK'], 'type': 'box', 'name': 'Rate of Fire', 'boxpoints':'all', '​jitter':0.3, 'pointpos':-1.8}
                ],
            'layout': go.Layout(
                title = 'Rate, DPS and TTK comparison',
                height = 600,
                )
        }
    ),

    html.H3('Distribution Graph'),

    dcc.Graph(
        id='dist_plot',
        figure= fig
    )

])

@app.callback(
    Output('main_plot', 'figure'),
    [Input('select_gun', 'value'),
    Input('select_option', 'value'),
    Input('select_plot', 'value')])
def update_maingraph(arsenal, options, plot):
    # since arsenal is now a list of symbols, create a list of traces
    traces = []
    if plot != 'bubble':
        for guns in arsenal:
            if guns == 'ARs':
                traces.append({'x' : df['Guns'].iloc[0:14 ], 'y' : df[options].iloc[0:14 ], 'type':plot, 'name':'Assualt Rifles', 'opacity': '0.75'})
            elif guns == 'SMGs':
                traces.append({'x' : df['Guns'].iloc[14:25], 'y' : df[options].iloc[14:25], 'type':plot, 'name':'SMG', 'opacity': '0.75'})
            elif guns == 'LMGs':
                traces.append({'x' : df['Guns'].iloc[25:30], 'y' : df[options].iloc[25:30], 'type':plot, 'name':'LMG', 'opacity': '0.75'})
            elif guns == 'Snipers':
                traces.append({'x' : df['Guns'].iloc[30:36], 'y' : df[options].iloc[30:36], 'type':plot, 'name':'Snipers', 'opacity': '0.75'})
            elif guns == 'Pistols':
                traces.append({'x' : df['Guns'].iloc[36:41], 'y' : df[options].iloc[36:41], 'type':plot, 'name':'Pistols', 'opacity': '0.75'})
            elif guns == 'Shotguns':
                traces.append({'x' : df['Guns'].iloc[41:45], 'y' : df[options].iloc[41:45], 'type':plot, 'name':'Shotguns', 'opacity': '0.75'})
    else:
        normalize = {'size':df[options]*10}
        if options in ['Rate of Fire', 'DPS', 'TTK', 'TTK1', 'TTK2', 'TTK3']:
            normalize = {'size':df[options]/10}
        elif options == 'Damage':
            normalize = {'size':df[options]*2}
        for guns in arsenal:
            if guns == 'ARs':
                traces.append(go.Scatter(x=df['Guns'].iloc[0:14], y=df[options ].iloc[0:14 ], name='ARs', mode='markers', marker=normalize, opacity=0.75))
            elif guns == 'SMGs':
                traces.append(go.Scatter(x=df['Guns'].iloc[14:25], y=df[options].iloc[14:25], name='SGMs', mode='markers', marker=normalize, opacity=0.75))
            elif guns == 'LMGs':
                traces.append(go.Scatter(x=df['Guns'].iloc[25:30], y=df[options].iloc[25:30], name='LMGs', mode='markers', marker=normalize, opacity=0.75))
            elif guns == 'Snipers':
                traces.append(go.Scatter(x=df['Guns'].iloc[30:36], y=df[options].iloc[30:36], name='Snipers', mode='markers', marker=normalize, opacity=0.75))
            elif guns == 'Pistols':
                traces.append(go.Scatter(x=df['Guns'].iloc[36:41], y=df[options].iloc[36:41], name='Pistols', mode='markers', marker=normalize, opacity=0.75))
            elif guns == 'Shotguns':
                traces.append(go.Scatter(x=df['Guns'].iloc[41:45], y=df[options].iloc[41:45], name='Shotguns', mode='markers', marker=normalize, opacity=0.75))
# or you could just create data in the loop and just return with go.Scatter(data)...
    fig = {
        # set data equal to traces
        'data': traces,
        # use string formatting to include all symbols in the chart title
        'layout': go.Layout(
            title = ", ".join(arsenal) + " " + options,
            xaxis = {'title': 'Guns'},
            yaxis = {'title': options},
            hovermode = 'closest',
            height = 500
        )
    }
    return fig

@app.callback(
    Output('box_plot', 'figure'),
    [Input('select_gun', 'value'),
    Input('select_option', 'value')])
def update_boxgraph(arsenal, options):
    traces = []
    for guns in arsenal:
        if guns == 'ARs':
            traces.append({'y' : df[options].iloc[0:14], 'type': 'box', 'name':'Rifles', 'boxpoints':'all', '​jitter':0.3})
        elif guns == 'SMGs':
            traces.append({'y' : df[options].iloc[14:25], 'type': 'box', 'name':'SMGs', 'boxpoints':'all', '​jitter':0.3})
        elif guns == 'LMGs':
            traces.append({'y' : df[options].iloc[25:30], 'type': 'box', 'name':'LMGs', 'boxpoints':'all', '​jitter':0.3})
        elif guns == 'Snipers':
            traces.append({'y' : df[options].iloc[30:36], 'type': 'box', 'name':'Snipers', 'boxpoints':'all', '​jitter':0.3})
        elif guns == 'Pistols':
            traces.append({'y' : df[options].iloc[36:41], 'type': 'box', 'name':'Pistols', 'boxpoints':'all', '​jitter':0.3})
        elif guns == 'Shotguns':
            traces.append({'y' : df[options].iloc[41:45], 'type': 'box', 'name':'Shotguns', 'boxpoints':'all', '​jitter':0.3})

    fig={
            'data': traces,
            'layout': go.Layout(
                title = ", ".join(arsenal) + ' ' + options + " stats",
                height = 600
                )
        }
    return fig

@app.callback(
    Output('dist_plot', 'figure'),
    [Input('select_gun', 'value'),
    Input('select_option', 'value')])
def update_distgraph(arsenal, options):
    # label = options + " of total arsenal"
    # fig = ff.create_distplot([df[options]], [label])
    traces = []
    label = []
    for guns in arsenal:
        if guns == 'ARs':
            traces.append(df[options].iloc[0:14])
            label.append('Assualt Rifle')
        elif guns == 'SMGs':
            traces.append(df[options].iloc[14:25])
            label.append('SMGs')
        elif guns == 'LMGs':
            traces.append(df[options].iloc[25:30])
            label.append('LMGs')
        elif guns == 'Snipers':
            traces.append(df[options].iloc[30:36])
            label.append('Snipers')
        elif guns == 'Pistols':
            traces.append(df[options].iloc[36:41])
            label.append('Pistols')
        elif guns == 'Shotguns':
            traces.append(df[options].iloc[41:45])
            label.append('Shotguns')

    return ff.create_distplot(traces, label)

if __name__ == '__main__':
    app.run_server()
