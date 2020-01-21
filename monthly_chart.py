import plotly.offline as pyo
import plotly.graph_objs as go
import pandas as pd

# df = pd.read_excel('C:/Users/Jie/Documents/dev/duke/data/crashes vs clicks.xlsx').fillna(0)
# df2=df.loc[2].to_frame().T


def duration(df_d):
    traces=[go.Bar(
        x = df_d.columns,
        y = df_d.iloc[0],
        marker={'color':'#6B8E23'}
        )]
    layout = go.Layout(
        title = 'Hours in the last 30 days',
        xaxis = {'title': 'Date'},
        yaxis = {'title': 'Hours'},
        paper_bgcolor="LightSteelBlue",
        )
    return {"data": traces, "layout": layout}

def touches(df_t):
    traces=[go.Bar(
        x = df_t.columns,
        y = df_t.iloc[0],
        marker={'color':'#ffdb58'},
        # marker=dict(color='#cd5c5c')
        )]
    layout = go.Layout(
        title = 'Touches in the last 30 days',
        xaxis = {'title': 'Date'},
        yaxis = {'title': 'Touches'},
        paper_bgcolor="LightSteelBlue",
        # height='100px'
        )

    return {"data": traces, "layout": layout}


def crashes(df_c):
    traces=[go.Bar(
        x = df_c.columns,
        y = df_c.iloc[0],
        marker=dict(color='#cd5c5c')
        )]
    layout = go.Layout(
        title = 'Crashes in the last 30 days',
        paper_bgcolor="LightSteelBlue",
            xaxis = {'title': 'Date'},
            yaxis = {'title': 'Number of Crashes'},
        # color='indianred',
        )

    return {"data": traces, "layout": layout}
