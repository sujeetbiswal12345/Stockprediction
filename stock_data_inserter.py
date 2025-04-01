import sqlite3

# Function to insert stock data
def insert_stock_data(symbol, date, open_price, high, low, close, volume):
    try:
        conn = sqlite3.connect('stock_predictions.db')
        c = conn.cursor()
        c.execute('''INSERT INTO stock_data (symbol, date, open, high, low, close, volume)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                     (symbol, date, open_price, high, low, close, volume))
        conn.commit()
        conn.close()
        print("Stock data inserted successfully.")
    except Exception as e:
        print(f"Error inserting stock data: {e}")

if __name__ == "__main__":
    # Example usage
    insert_stock_data('AAPL', '2025-04-01', 150.50, 152.00, 148.00, 150.20, 500000)
