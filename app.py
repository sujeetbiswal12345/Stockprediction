from flask import Flask, render_template, jsonify, request
import os
from model import load_models, predict_stock_price
from utils import generate_plot, fetch_stock_data

app = Flask(__name__)

# Load models once when the app starts
load_models()


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        symbol = request.form['symbol'].upper()
        
        # Fetch stock data
        data = fetch_stock_data(symbol)
        if data is None:
            raise ValueError(f"No data fetched for {symbol}")
        
        # Perform LSTM Prediction
        lstm_value, today_price, error = predict_stock_price(data)
        
        
        # Generate plot
        plot_url = generate_plot(symbol, data['Close'], lstm_value)
        if plot_url is None:
            raise ValueError("Failed to generate plot.")
        
        return jsonify({
            'symbol': symbol,
            'actual_price': round(today_price, 2),
            'lstm': round(lstm_value, 2),
            'plot_url': plot_url,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

if __name__ == '__main__':
    os.makedirs("backend", exist_ok=True)  # Ensure backend folder exists
    app.run(host='0.0.0.0', port=5000, debug=True)
