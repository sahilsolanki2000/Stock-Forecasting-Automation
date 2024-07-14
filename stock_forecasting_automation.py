import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
from pmdarima import auto_arima
from prophet import Prophet
from statsmodels.tsa.api import ExponentialSmoothing
import plotly.graph_objects as go

st.title("Stock Forecasting Automation")

# User inputs
stock_ticker = st.text_input("Enter Stock Ticker (e.g. AAPL, MSFT):")
start_date = st.date_input("Start Date", datetime(2020, 1, 1))
end_date = st.date_input("End Date", datetime.now())

# Model choice with descriptions
model_choice = st.selectbox(
    "Choose Model", 
    ["Prophet (Facebook's time series model, good for seasonality and trends)", 
     "ARIMA (AutoRegressive Integrated Moving Average, good for non-seasonal data)", 
     "Exponential Smoothing (Good for data with trends and seasonality)"]
)

show_forecast_df = st.checkbox("Show Forecasted DataFrame (Next 30 days)")

if st.button("Run Forecast"):
    if stock_ticker:
        # Fetch data
        data = yf.download(stock_ticker, start=start_date, end=end_date)

        if data.empty:
            st.error("No data found for the given stock ticker. Please enter a correct stock ticker.")
        else:
            st.write(data)

            # Prepare data for forecasting
            data.reset_index(inplace=True)
            data['Date'] = pd.to_datetime(data['Date'])
            data.set_index('Date', inplace=True)

            # Ensure the index is recognized as a DatetimeIndex and set frequency
            if not isinstance(data.index, pd.DatetimeIndex):
                data.index = pd.to_datetime(data.index)
            data = data.asfreq('D')

            # Handle missing values
            data['Close'].interpolate(method='time', inplace=True)

            forecast_df = pd.DataFrame()

            try:
                if "ARIMA" in model_choice:
                    st.subheader("ARIMA Forecast")
                    model = auto_arima(data['Close'], start_p=1, start_q=1, max_p=3, max_q=3, seasonal=False)
                    forecast = model.predict(n_periods=30)
                    forecast_dates = pd.date_range(data.index[-1], periods=30, freq='D')
                    forecast_series = pd.Series(forecast, index=forecast_dates)
                    forecast_df['ARIMA'] = forecast_series
            except Exception as e:
                st.error(f"Error in ARIMA model: {e}")

            try:
                if "Prophet" in model_choice:
                    st.subheader("Prophet Forecast")
                    prophet_data = data.reset_index()[['Date', 'Close']].rename(columns={'Date': 'ds', 'Close': 'y'})
                    prophet_model = Prophet()
                    prophet_model.fit(prophet_data)
                    future = prophet_model.make_future_dataframe(periods=30)
                    forecast = prophet_model.predict(future)
                    forecast_df['Prophet'] = forecast.set_index('ds')['yhat'][-30:]
            except Exception as e:
                st.error(f"Error in Prophet model: {e}")

            try:
                if "Exponential Smoothing" in model_choice:
                    st.subheader("Exponential Smoothing Forecast")
                    es_model = ExponentialSmoothing(data['Close'], trend='add', seasonal=None).fit()
                    forecast = es_model.forecast(steps=30)
                    forecast_dates = pd.date_range(data.index[-1], periods=30, freq='D')
                    forecast_series = pd.Series(forecast, index=forecast_dates)
                    forecast_df['Exponential Smoothing'] = forecast_series
            except Exception as e:
                st.error(f"Error in Exponential Smoothing model: {e}")

            # Remove rows with NaN values
            forecast_df.dropna(inplace=True)

            if not forecast_df.empty:
                combined_df = pd.concat([data['Close'], forecast_df], axis=1)
                
                if show_forecast_df:
                    st.write("Forecasted DataFrame (Next 30 days)")
                    st.dataframe(forecast_df)
                
                # Create Plotly figure
                fig = go.Figure()

                # Add actual close price
                fig.add_trace(go.Scatter(
                    x=combined_df.index,
                    y=combined_df['Close'],
                    mode='lines',
                    name='Actual Close Price'
                ))

                # Add ARIMA forecast
                if 'ARIMA' in combined_df.columns:
                    fig.add_trace(go.Scatter(
                        x=combined_df.index,
                        y=combined_df['ARIMA'],
                        mode='lines',
                        name='ARIMA Forecast'
                    ))

                # Add Prophet forecast
                if 'Prophet' in combined_df.columns:
                    fig.add_trace(go.Scatter(
                        x=combined_df.index,
                        y=combined_df['Prophet'],
                        mode='lines',
                        name='Prophet Forecast'
                    ))

                # Add Exponential Smoothing forecast
                if 'Exponential Smoothing' in combined_df.columns:
                    fig.add_trace(go.Scatter(
                        x=combined_df.index,
                        y=combined_df['Exponential Smoothing'],
                        mode='lines',
                        name='Exponential Smoothing Forecast'
                    ))

                # Update layout to include range slider
                fig.update_layout(
                    title='Stock Price and Forecast',
                    xaxis_title='Date',
                    yaxis_title='Price',
                    xaxis=dict(
                        rangeselector=dict(
                            buttons=list([
                                dict(count=1, label='1m', step='month', stepmode='backward'),
                                dict(count=6, label='6m', step='month', stepmode='backward'),
                                dict(count=1, label='YTD', step='year', stepmode='todate'),
                                dict(count=1, label='1y', step='year', stepmode='backward'),
                                dict(step='all')
                            ])
                        ),
                        rangeslider=dict(visible=True),
                        type='date'
                    )
                )

                st.plotly_chart(fig)
    else:
        st.write("Please enter a stock ticker.")