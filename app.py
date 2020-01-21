import dash
# import dash_auth
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from dash.dependencies import Input, Output
# import dash_table

import new_weekly
import monthly_chart

# USERNAME_PASSWORD = [
#     ['t1user', '123456'],['dukeuser', '123456']
# ]

app = dash.Dash()
# auth = dash_auth.BasicAuth(app,USERNAME_PASSWORD)
server = app.server

# ======================================data frames===============================================
# import weekly activity from .txt files(python dictionary)
# df=pd.DataFrame(eval(open('data/week.txt', 'r').read()))
from datetime import timedelta, datetime, date
import connect

conn = connect.connect()

device=['Connector','Forlines','Vestibule1','Vestibule2','Welcomedesk']
modules=['Events','Athletics','History','Notable Alumni','Campus Map','Donor Impact','DukeAroundTheWorld']
device_alias=['dukealumni-connector','dukealumni-forlineswall1','dukealumni-vestibule1','dukealumni-vestibule2','dukealumni-welcomedesk']

one_week_ago=(datetime.now() - timedelta(days=8)).date()
one_month_ago=(datetime.now() - timedelta(days=31)).date()
today=(datetime.now() - timedelta(days=1)).date()

query = """
select cast(date_trunc('{}', date) as date) AS period,device,
sum(cast(info->>'active_hours' as float)) as total_duration,
sum(cast(info->>'totalTouches' as float)) as total_clicks,
sum(cast(info->>'Fullscreen_clicks' as float)) as fullscreen_clicks,
sum(cast(info->>'Events_duration' as float))/3600.0 as events_duration,
sum(cast(info->>'Events_clicks' as float)) as events_clicks,
sum(cast(info->>'Athletics_duration' as float))/3600.0 as athletics_duration,
sum(cast(info->>'Athletics_clicks' as float)) as athletics_clicks,
sum(cast(info->>'History_duration' as float))/3600.0 as history_duration,
sum(cast(info->>'History_clicks' as float)) as history_clicks,
sum(cast(info->>'Notable Alumni_duration' as float))/3600.0 as notablealumni_duration,
sum(cast(info->>'Notable Alumni_clicks' as float)) as notablealumni_clicks,
sum(cast(info->>'Campus Map_duration' as float))/3600.0 as campusmap_duration,
sum(cast(info->>'Campus Map_clicks' as float)) as campusmap_clicks,
sum(cast(info->>'Donor Impact_duration' as float))/3600.0 as donor_duration,
sum(cast(info->>'Donor Impact_clicks' as float)) as donor_clicks,
sum(cast(info->>'Duke Around The Globe_duration' as float))/3600.0 as globe_duration,
sum(cast(info->>'Duke Around The Globe_clicks' as float)) as globe_clicks,
sum(cast(info->>'alumni-detected' as float)) as alumni_detected,
sum(cast(info->>'alumni-selected' as float)) as alumni_selected,
sum(cast(info->>'accessibility-tapped' as float)) as accessibility_tapped
from daily_device_summary where device in ('dukealumni-connector','dukealumni-forlineswall1','dukealumni-vestibule1','dukealumni-vestibule2','dukealumni-welcomedesk') and
date {}
group by {},1--,2
order by 1--,2
limit {}
"""

# create dataframe for weekly charts
dateFilter1 = "BETWEEN '{}' and '{}'".format(one_week_ago, today)
interval1="week"
query_weekly=query.format(interval1,dateFilter1,'device',5)

df_weekly_orig = pd.read_sql_query(query_weekly,con=conn).fillna(0)
alumni_detected=df_weekly_orig.iloc[0]['alumni_detected']
alumni_login=df_weekly_orig.iloc[0]['alumni_selected']
accessbility_tapped=df_weekly_orig.loc[:,'accessibility_tapped'].sum(axis=0)

# df_weekly_orig['device'].str.slice(start=11)
device1=df_weekly_orig['device'].str.slice(start=11)

df_weekly=df_weekly_orig.drop(columns=['period','device','alumni_detected','alumni_selected','accessibility_tapped'])

df_weekly.index=device1

# find columns that satisfy: 1) not fullscreen, 2) don't contain total touches and duration
bol=~(np.logical_or(df_weekly.columns.str.contains('ullscreen'),df_weekly.columns.str.contains('otal')))
df_weekly=df_weekly.loc[:,bol]

# touches and duration
df_clicks=df_weekly[(df_weekly.filter(like='click').columns)]
df_duration=df_weekly[(df_weekly.filter(like='duration').columns)]
df_clicks.index=device1
df_duration.index=device1
df_clicks.columns=modules
df_duration.columns=modules

print(device1)
print(df_clicks)
print(df_duration)
print(df_weekly)

# create dataframe for 30day chart
dateFilter2= "BETWEEN '{}' and '{}'".format((datetime.now() - timedelta(days=30)).date(), (datetime.now() - timedelta(days=0)).date())
interval2="day"

query_monthly=query.format(interval2,dateFilter2,'device,period',150)
df_monthly_orig=(pd.read_sql_query(query_monthly,con=conn).fillna(0))
df_monthly= df_monthly_orig.iloc[:,:4]
df_monthly.index=df_monthly['period']

df_monthly_touches=pd.Series({})
df_monthly_hours=pd.Series({})


for i in device_alias:
    d1=df_monthly[df_monthly['device']==i].T.loc['total_duration']
    t1=df_monthly[df_monthly['device']==i].T.loc['total_clicks']
    df_monthly_touches=pd.concat([df_monthly_touches, t1], axis=1, sort=True)
    df_monthly_hours=pd.concat([df_monthly_hours, d1], axis=1, sort=True)


df_monthly_hours=df_monthly_hours.fillna(0).drop(columns=0)
df_monthly_touches=df_monthly_touches.fillna(0).drop(columns=0)

df_monthly_hours.columns=device
df_monthly_touches.columns=device


df_monthly_hours=df_monthly_hours.T
df_monthly_touches=df_monthly_touches.T

# ==============================dashboard styles===============================================

colors = {
    'background': '#082255',
    'text':'#fff'
    }
pie_chart_style={
    "width":"49%", 'display':'inline-block'
    }
h2_style={
    'textAlign': 'center',
    'color': colors['text'],
    'width':'49%',
    'display':'inline-block',
    }
indicator={
  'text-align': 'center',
  'width':'27%',
  'display':'inline-block',
  'border-radius': '5px',
  'background-color': 'white',
  'margin': '0.5rem',
  'padding': '1rem',
  'position': 'relative',
  'border': '1px solid'
}

indicator_value= {
  'font-size': '2rem',
  'margin': '1rem 0'
}

# =====================================layout==============================================

app.layout = html.Div(children=[
    html.Br(),
    html.H1(children='Virtual Duke Activity Report',
            style={
            'textAlign': 'center',
            'color': colors['text'],
            'margin-top':'0'
        }),

    html.Div(children=str(one_week_ago)+' - '+str(today),
        style={
        'textAlign': 'center',
        'color': colors['text'],
        'margin-bottom': '0.5cm'
        }),

    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.P(
                        "Total Alumni Detected",
                        className="indicator_text"
                ),
                html.P(
                        alumni_detected,
                        className="indicator_value"
                ),

            ],
            style=indicator),
            html.Div(children=[
                html.P(
                        "Alumni Logged In",
                        className="indicator_text"
                ),
                html.P(
                        alumni_login,
                        className="indicator_value"
                ),

            ],
            style=indicator),
            html.Div(children=[
                html.P(
                        "Accessbility Feature Tapped",
                        className="indicator_text"
                ),
                html.P(
                        accessbility_tapped,
                        className="indicator_value"
                ),

            ],
            style=indicator),
        ],
        style={'display':'inline-block','width':'98%'},
        )],
    style={'textAlign':'center'}),

    html.H2(children='Percent Usage by Device and Module',
            style=h2_style),
    html.H2(children='Touches& Duration by Device and Module',
            style=h2_style),
        html.Div(children=[
                html.Div(children=[
                    html.Div(children=[
                            # html.Div(children=[
                            #     dcc.Graph(
                            #         figure=go.Figure(new_weekly.pie_chart(df_clicks, df_duration))
                            #     )
                            # ])
                            html.Div(children=[
                                dcc.Graph(
                                        figure = go.Figure(new_weekly.pie_chart1(df_clicks))
                                    )
                            ],style=pie_chart_style),
                            html.Div(children=[
                                dcc.Graph(
                                        figure = go.Figure(new_weekly.pie_chart2(df_duration))

                                    )
                            ],style=pie_chart_style),
                            html.Div(children=[
                                dcc.Graph(
                                        figure = go.Figure(new_weekly.pie_chart3(df_clicks))
                                    )
                            ],style=pie_chart_style),
                            html.Div(children=[
                                dcc.Graph(
                                        figure = go.Figure(new_weekly.pie_chart4(df_duration))
                                    )
                            ],style=pie_chart_style)

                        ],style={'width':'50%','display':'inline-block'}),

                        html.Div(children=[
                                dcc.Graph(id="clicks",
                                        figure=go.Figure(new_weekly.clicks_weekly(df_clicks,device1))
                                    ),
                                dcc.Graph(id="duration",
                                        figure=go.Figure(new_weekly.duration_weekly(df_duration,device1))
                                    ),
                        ],style={'width':'50%','display':'inline-block'}),

                    ],style={'width':'90%','margin':'auto'}),


            html.Div(children=[
                html.Div(children=[
                    html.Br(),html.Br(),
                    html.H2(children='30 Day Changes',
                            style={
                            'textAlign': 'center',
                            'color': colors['text']
                        }),

                    html.Div(children=str(one_month_ago)+' - '+str(today),
                            style={
                            'textAlign': 'center',
                            'color': colors['text'],
                            'margin-bottom': '0.5cm'
                            }),
                    html.Div(children=[
                        html.Label(children='Please Select Device:',
                                   style={'color': colors['text']}
                        ),
                            dcc.Dropdown(
                                id="select-device",
                                options=[
                                    {'label':i, 'value':i} for i in device
                                ],
                                value='Welcomedesk',
                                style={'width':'300px'}
                            ),

                        dcc.Graph(id="hours_m"),
                        dcc.Graph(id="touches_m"),
                        # per Morgan's suggestion. crashes are now hidden
                        # dcc.Graph(id="crashes_m")
                    ]),

                    ],style={'width':'90%','margin':'auto','padding-bottom':'1cm'}),

                ],style={'backgroundColor': colors['background']})
            ])

],style={'backgroundColor': colors['background']})

# ================================calbacks==============================================

@app.callback(
    Output(component_id='hours_m', component_property='figure'),
    [Input(component_id='select-device', component_property='value')]
    )
def update_figure(value):
    df_monthly_d=df_monthly_hours[df_monthly_hours.index==value]
    return go.Figure(monthly_chart.duration(df_monthly_d))

# callback function for monthly crashes
# @app.callback(
#     Output(component_id='crashes_m', component_property='figure'),
#     [Input(component_id='select-device', component_property='value')]
#     )
# def update_figure(value):
#     df_monthly_c =df_monthly_crashes[df_monthly_crashes.index==value]
#     return go.Figure(monthly_chart.crashes(df_monthly_c))

@app.callback(
    Output(component_id='touches_m', component_property='figure'),
    [Input(component_id='select-device', component_property='value')]
    )
def update_figure(value):
    df_monthly_t =df_monthly_touches[(df_monthly_touches.index)==value]
    return go.Figure(monthly_chart.touches(df_monthly_t))

if __name__ == '__main__':
    app.run_server(debug=True)
