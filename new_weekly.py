import numpy as np
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go
from plotly import tools
import dash_html_components as html
from plotly.subplots import make_subplots


def clicks_weekly(df_clicks,device):
    trace1 = go.Bar(
        x=df_clicks.columns,
        y=df_clicks.iloc[0],
        name = device[0],
        marker=dict(color='#58508d')
    )
    trace2 = go.Bar(
         x=df_clicks.columns,
        y=df_clicks.iloc[1],
        name=device[1],
        marker=dict(color='#003f5c')
    )
    trace3 = go.Bar(
         x=df_clicks.columns,
        y=df_clicks.iloc[2],
        name = device[2],
        marker=dict(color='#bc5090')
    )

    trace4 = go.Bar(
         x=df_clicks.columns,
        y=df_clicks.iloc[3],
        name=device[3],
        marker=dict(color='#ff6361') # set the marker color to coral
    )


    trace5 = go.Bar(
         x=df_clicks.columns,
        y=df_clicks.iloc[4],
        name = device[4],
        marker=dict(color='#ffa600')
    )

    data = [trace1,trace2,trace3, trace4, trace5]
    layout = go.Layout(
        title='Touches of Each Module by Device',
        barmode='stack',
        hovermode='closest'
    )
    # fig = go.Figure(data=data, layout=layout)
    # pyo.plot(fig, filename='weekly_clicks.html')

    return {"data": data, "layout": layout}

def duration_weekly(df_duration,device):
    trace1 = go.Bar(
    x=df_duration.columns,
    y=df_duration.iloc[0],
    name = device[0],
    marker=dict(color='#58508d')
)
    trace2 = go.Bar(
         x=df_duration.columns,
        y=df_duration.iloc[1],
        name=device[1],
        marker=dict(color='#003f5c')
    )
    trace3 = go.Bar(
         x=df_duration.columns,
        y=df_duration.iloc[2],
        name = device[2],
        marker=dict(color='#bc5090')
    )

    trace4 = go.Bar(
         x=df_duration.columns,
        y=df_duration.iloc[3],
        name = device[3],
        marker=dict(color='#ff6361') # set the marker color to coral
    )


    trace5 = go.Bar(
        x=df_duration.columns,
        y=df_duration.iloc[4],
        name = device[4],
        marker=dict(color='#ffa600'),
    )

    data = [trace1,trace2,trace3, trace4, trace5]
    layout = go.Layout(
        title='Duration(hours) of Each Module by Device',
        barmode='stack',
        hovermode='closest',
        # plot_bgcolor="#082255"
    )

    return {"data": data, "layout": layout}

#  pie charts
#  pie charts subplots
# def pie_chart(df_clicks, df_duration):
#     # Create subplots, using 'domain' type for pie charts
#     specs = [[{'type':'domain'}, {'type':'domain'}], [{'type':'domain'}, {'type':'domain'}]]
#     fig = make_subplots(rows=2, cols=2, specs=specs)
#
#     # Define pie charts
#     fig.add_trace(go.Pie(labels = df_clicks.index.values.tolist(), values = df_clicks.sum(axis = 1, skipna = True),name='touches per device'), 1, 1)
#     fig.add_trace(go.Pie(labels = df_duration.index.values.tolist(),values = df_duration.sum(axis = 1, skipna = True),name='duration per device'),1, 2)
#     fig.add_trace(go.Pie(labels = df_clicks.columns,values = df_clicks.sum(axis = 0, skipna = True),name='touches per module'), 2, 1)
#     fig.add_trace(go.Pie(labels = df_duration.columns,values = df_duration.sum(axis = 0, skipna = True),name='duration per module'), 2, 2)
#
#     # Tune layout and hover info
#     fig.update_traces(hoverinfo='label+percent+name', textinfo='label+percent')
#     fig.update(layout_title_text='',
#                layout_showlegend=False)
#
#     return fig

def pie_chart1(df_clicks):
    labels = df_clicks.index.values.tolist()
    values = df_clicks.sum(axis = 1, skipna = True)

    layout = go.Layout(
            title='Touches',
            showlegend=False,
            margin= dict(l=10,r=10,b=20,t=100,pad=5),
            # titlefont={'family':'bold'}
        )

    trace = go.Pie(
            labels=labels,
            values=values
        )
    fig={"data": [trace], "layout": layout}
    fig['data'][0].update({'hole':.3,'textinfo' : 'label+percent'})
    return fig

def pie_chart2(df_duration):
    labels = df_duration.index.values.tolist()
    values = df_duration.sum(axis = 1, skipna = True)

    layout = go.Layout(
            title='Duration',
            showlegend=False,
            margin= dict(l=10,r=10,b=20,t=100,pad=5)
        )

    trace = go.Pie(
            labels=labels,
            values=values
        )

    fig={"data": [trace], "layout": layout}
    fig['data'][0].update({'textinfo' : 'label+percent'})
    return fig

def pie_chart3(df_clicks):
    labels = df_clicks.columns
    values = df_clicks.sum(axis = 0, skipna = True)

    layout = go.Layout(
            title='Touches',
            showlegend=False,
            margin= dict(l=10,r=10,b=20,t=100,pad=10)
        )

    trace = go.Pie(
            labels=labels,
            values=values
        )

    fig={"data": [trace], "layout": layout}
    fig['data'][0].update({'textinfo' : 'label+percent'})
    return fig

def pie_chart4(df_duration):
    labels = df_duration.columns
    values = df_duration.sum(axis = 0, skipna = True)

    layout = go.Layout(
            title='Duration',
            showlegend=False,
            margin= dict(l=10,r=10,b=20,t=100,pad=10),
        )

    trace = go.Pie(
            labels=labels,
            values=values
        )
    fig={"data": [trace], "layout": layout}
    fig['data'][0].update({'textinfo' : 'label+percent'})
    return fig

# def indicator(color, text, id_value):
#     return html.Div(
#         [
#             # html.P(id_value),
#             # html.P(text)
#             html.P("hi")
#         ],
#         style={
#           'class':'column',
#           'flex': '1',
#           'padding': '0.75rem 1.75rem',
#           'text-align': 'center'
#         }
#     )
