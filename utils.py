import yfinance as yf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def fetch_stock_data(symbol, days=66):
    """Fetch historical stock data."""
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(period=f"{days}d")
        if df.empty or 'Close' not in df.columns:
            raise ValueError(f"No data available for {symbol}")
        return df[['Close']]
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return None

def generate_plot(symbol, actual, lstm_pred):
    """Generate a plot for stock prediction."""
    try:
        plt.figure(figsize=(10, 5))
        plt.plot(actual.index, actual.values, label='Actual Price', color='blue')
        plt.plot(actual.index[-1], lstm_pred, 'ro', markersize=8, label='LSTM Prediction')
        
        # Add today's price annotation
        plt.annotate(f'Today: Rs {actual.values[-1]:.2f}', 
                    xy=(actual.index[-1], actual.values[-1]),
                    xytext=(10, 10), textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                    arrowprops=dict(arrowstyle='->'))
        
        plt.title(f'{symbol} Price Prediction')
        plt.xlabel('Date')
        plt.ylabel('Price (Rs)')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        img = BytesIO()
        plt.savefig(img, format='png', dpi=100)
        img.seek(0)
        plt.close()
        return base64.b64encode(img.getvalue()).decode('utf-8')
    except Exception as e:
        print(f"Error generating plot: {e}")
        return None
