import pickle
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

# Global variables for model and scaler
lstm_model = None
scaler = None

def load_models():
    global lstm_model, scaler
    if lstm_model is None or scaler is None:
        try:
            # Load the LSTM model
            lstm_model = load_model('backend/lstm_model.h5')
            lstm_model.compile(optimizer='adam', loss='mse')
            
            # Load the scaler
            with open('backend/scaler.pkl', 'rb') as f:
                scaler = pickle.load(f)
            
            print("Models and scaler loaded successfully.")
        except Exception as e:
            print(f"Error loading models: {e}")

def predict_stock_price(data):
    """Predict the stock price using the LSTM model."""
    today_price = data['Close'].iloc[-1]
    
    # Prepare data for LSTM
    scaled_data = scaler.transform(data.values)
    lstm_input = scaled_data[-60:].reshape(1, 60, 1)
    
    # Make prediction
    lstm_value = float(scaler.inverse_transform(lstm_model.predict(lstm_input))[0][0])
    
    # Calculate error
    error = abs(today_price - lstm_value)
    
    return lstm_value, today_price, error
