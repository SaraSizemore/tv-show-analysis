from flask import Flask, render_template, request
import pandas as pd
from pandas import read_csv
import os

app = Flask(__name__)

df = pd.read_csv('./static/shows.csv')
df1 = df[:-1]

show_names = df1['show'].tolist()
show_names = sorted(show_names)
show_provider = ['Amazon Prime', 'Netflix', 'All']


def get_table(cp):
    df2 = df1
    if cp == 'Amazon Prime' or cp == 'Netflix':
        df2 = df2.loc[df2['provider'] == cp]
        df2.drop(columns=['rank'])
        df2['rank'] = df2['provider rank']
    df2 = df2.astype({'rank': 'int'})
    df2 = df2.sort_values(by=['rank'])
    D = df2.to_dict('index')
    dictlist = [{'index': y} for x, y in D.items()]
    return dictlist


def get_page(show):
    df3 = df.loc[df['show'] == show]
    provider = df3.iloc[0]['provider']
    name = df3.iloc[0]['show']
    wpm = round(df3.iloc[0]['wpm'], 1)
    runtime = round(df3.iloc[0]['avg runtime'], 1)
    avg_wpm = round(df3.iloc[0]['avg WPM'], 1)
    avg_reps = round(df3.iloc[0]['avg reps'], 1)
    df4 = df.loc[df['show'] == 'Average']
    wpm_avg = round(df4.iloc[0]['wpm'], 1)
    runtime_avg = round(df4.iloc[0]['avg runtime'], 1)
    avg_wpm_avg = round(df4.iloc[0]['avg WPM'], 1)
    avg_reps_avg = round(df4.iloc[0]['avg reps'], 1)
    return provider, name, wpm, runtime, avg_wpm, avg_reps, wpm_avg, runtime_avg, avg_wpm_avg, avg_reps_avg


@app.route('/')
@app.route('/home')
def home():
    selected_provider = request.args.get("Select Provider")

    if selected_provider == None:
        selected_provider = "All"

    DT = get_table(selected_provider)

    return render_template('home.html', shows=DT, selected_provider=selected_provider, show_provider=show_provider, show_names=show_names)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/showdata')
def show():

    selected_show = request.args.get("Select Show")

    if selected_show == None:
        selected_show = "Sesame Street"

    provider, name, wpm, runtime, avg_wpm, avg_reps, wpm_avg, runtime_avg, avg_wpm_avg, avg_reps_avg = get_page(
        selected_show)

    #selected_show = selected_show, show_names = show_names,

    # return render_template('dinodana.html', selected_show=selected_show, show_names=show_names)
    return render_template('showdata.html', show_names=show_names, provider=provider, name=name, wpm=wpm, runtime=runtime, avg_wpm=avg_wpm, avg_reps=avg_reps, wpm_avg=wpm_avg, runtime_avg=runtime_avg, avg_wpm_avg=avg_wpm_avg, avg_reps_avg=avg_reps_avg)


if __name__ == '__main__':
    app.run()
