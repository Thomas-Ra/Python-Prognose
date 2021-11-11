import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def make_plot(stock, period = "10d", interval = "15m"):
    data = yf.download(tickers=stock, period=period, interval=interval, rounding=bool)

    avg_30 = data.Close.rolling(window=30, min_periods=1).mean()

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name='market data'),
        secondary_y=False,
    )

    #remove weekends and time between 4pm and 9:30am (market closed)
    fig.update_xaxes(
        rangebreaks=[
            { 'pattern': 'day of week', 'bounds': [6, 1]},
            { 'pattern': 'hour', 'bounds':[16,9.5]}
        ]
    )

    fig.add_trace(
        go.Scatter(x=data.index, y=avg_30, name='Moving Average of 30 periods', mode="lines"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Bar(x=data.index, y=data.Volume, name="Volume"),
        secondary_y=True,
    )


    # Add figure title
    fig.update_layout(
        title_text="TSLA Stock Info"
    )

    # Set x-axis title
    fig.update_xaxes(title_text="time")

    # Set y-axes titles
    fig.update_yaxes(title_text="Stock Price in USD", secondary_y=False)
    fig.update_yaxes(title_text="Volume", secondary_y=True, range=[0,32000000])

    fig.show()
    fig.write_html("./fig.html")