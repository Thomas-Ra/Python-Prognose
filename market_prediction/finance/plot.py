import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def make_plot(stock, data, showResult= False, saveResult= True, includeCandles = False, removeWeekends = False, includeVolume= False, useRollingAverage = False):
    # Graph mit zweiter y-Achse anlegen
    if includeVolume:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Bar(x=data.index, y=data["volume"], name="Volume"),
            secondary_y=True,
        )
        fig.update_yaxes(title_text="Volume", secondary_y=True, range=[0,32000000])
    else:
        fig = make_subplots()

    # Add traces
    if includeCandles:
        fig.add_trace(
            go.Candlestick(x=data["date"], open=data['open'], high=data['high'], low=data['low'], close=data['close'], name='market data'),
            secondary_y=False,
        )

    # #remove weekends and time between 4pm and 9:30am (market closed)
    if removeWeekends:
        fig.update_xaxes(
            rangebreaks=[
                { 'pattern': 'day of week', 'bounds': [6, 1]},
                { 'pattern': 'hour', 'bounds':[16,9.5]}
            ]
        )
    
    if useRollingAverage:
        avg_30 = data['adjclose_15'].rolling(window=30, min_periods=1).mean()
        avg_30_true = data['true_adjclose_15'].rolling(window=30, min_periods=1).mean()
        fig.add_trace(
            go.Scatter(x=data["date"], y=avg_30, name='Moving Average of 30 periods', mode="lines"),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(x=data["date"], y=avg_30_true, name='Moving Average of 30 periods predicted', mode="lines"),
            secondary_y=False,
        )
    else: 
        fig.add_trace(
            go.Scatter(x=data["date"], y=data['true_adjclose_15'], name='Close', mode="lines"),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(x=data["date"], y=data['adjclose_15'], name='Close predicted', mode="lines"),
            secondary_y=False,
        )

    # Überschrift
    fig.update_layout(
        title_text=stock + " Stock Info"
    )

    # x-achse Titel
    fig.update_xaxes(title_text="time")

    # y-achsen Titel
    fig.update_yaxes(title_text="Stock Price in USD", secondary_y=False)

    if showResult:
        fig.show()
    fig.write_html("./html/"+stock+".html")


aapl = pd.read_csv("./csv-results/2022-01-08_AAPL-sh-1-sc-1-sbd-0-huber_loss-adam-LSTM-seq-50-step-15-layers-2-units-256-b.csv")
amzn = pd.read_csv("./csv-results/2022-01-07_AMZN-sh-1-sc-1-sbd-0-huber_loss-adam-LSTM-seq-50-step-15-layers-2-units-256-b.csv")
gme = pd.read_csv("./csv-results/2022-01-07_GME-sh-1-sc-1-sbd-0-huber_loss-adam-LSTM-seq-50-step-15-layers-2-units-256-b.csv")
goog = pd.read_csv("./csv-results/2022-01-08_GOOG-sh-1-sc-1-sbd-0-huber_loss-adam-LSTM-seq-50-step-15-layers-2-units-256-b.csv")
msft = pd.read_csv("./csv-results/2022-01-08_MSFT-sh-1-sc-1-sbd-0-huber_loss-adam-LSTM-seq-50-step-15-layers-2-units-256-b.csv")
tsla = pd.read_csv("./csv-results/2022-01-08_TSLA-sh-1-sc-1-sbd-0-huber_loss-adam-LSTM-seq-50-step-15-layers-2-units-256-b.csv")

#fix the unnamed column
aapl.rename( columns={'Unnamed: 0':'date'}, inplace=True )
amzn.rename( columns={'Unnamed: 0':'date'}, inplace=True )
gme.rename( columns={'Unnamed: 0':'date'}, inplace=True )
goog.rename( columns={'Unnamed: 0':'date'}, inplace=True )
msft.rename( columns={'Unnamed: 0':'date'}, inplace=True )
tsla.rename( columns={'Unnamed: 0':'date'}, inplace=True )

make_plot("Amazon", amzn)
make_plot("Apple", aapl)
make_plot("GameStop", gme)
make_plot("Google", goog)
make_plot("Microsoft", msft)
make_plot("Tesla", tsla)