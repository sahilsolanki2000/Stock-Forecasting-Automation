# Stock Forecasting Automation

This is a Streamlit application that allows users to perform stock price forecasting using various models such as ARIMA, Prophet, and Exponential Smoothing. The application fetches historical stock price data from Yahoo Finance and generates forecasts for the next 30 days.

## Features

- Fetch historical stock price data using Yahoo Finance.
- Choose between different forecasting models: ARIMA, Prophet, and Exponential Smoothing.
- Display the actual stock prices and forecasted prices on an interactive Plotly chart.
- Option to show the forecasted DataFrame.
- Include a range slider and various date range selection options for better visualization.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/stock-forecasting-automation.git
    cd stock-forecasting-automation
    ```

2. Create and activate a virtual environment:
    - On Windows:
        ```sh
        python -m venv env
        .\env\Scripts\activate
        ```
    - On macOS and Linux:
        ```sh
        python3 -m venv env
        source env/bin/activate
        ```

3. Install the required libraries:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the Streamlit application:
    ```sh
    streamlit run app.py
    ```

2. Open your web browser and navigate to `http://localhost:8501`.

3. Enter the stock ticker (e.g., AAPL, MSFT) and select the date range for the historical data.

4. Choose the forecasting model and click the "Run Forecast" button.

5. View the actual and forecasted stock prices on the interactive Plotly chart.

6. (Optional) Check the "Show Forecasted DataFrame" checkbox to display the forecasted data in a DataFrame format.

## Dependencies

- streamlit
- yfinance
- pandas
- pmdarima
- prophet
- statsmodels
- plotly

## Example

![Example](example.png)

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Yahoo Finance](https://www.yahoofinance.com/)
- [Prophet](https://facebook.github.io/prophet/)
- [pmdarima](http://alkaline-ml.com/pmdarima/)
- [Statsmodels](https://www.statsmodels.org/)
- [Plotly](https://plotly.com/)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## Contact

If you have any questions, feel free to reach out to me at [your-email@example.com](mailto:your-email@example.com).
