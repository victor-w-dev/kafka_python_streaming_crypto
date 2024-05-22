from pybit.unified_trading import HTTP
from kafka import KafkaProducer
import json
import time

# Initialize Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Initialize trading session
session = HTTP(testnet=False)
timeframe = 1

def klines(symbol):
    try:
        # Fetch the latest kline data
        resp = session.get_kline(
            category='linear',
            symbol=symbol,
            interval=timeframe,
            limit=1
        )['result']['list']
        
        # Reverse the response to maintain chronological order
        resp = resp[::-1]
        return resp[0]
    except Exception as err:
        print(f"Error fetching klines: {err}")
        return None

if __name__ == "__main__":
    while True:
        kline_data = klines('BTCUSDT')
        if kline_data:
            data_dict = {
                "Time": int(kline_data[0]),                  
                "Open": float(kline_data[1]),                 
                "High": float(kline_data[2]),                 
                "Low": float(kline_data[3]),                  
                "Close": float(kline_data[4]),                
                "Volume": float(kline_data[5]),               
                "Turnover": float(kline_data[6])              
            }
            try:
                # Send data to Kafka topic
                producer.send('BTCUSDT-1min', json.dumps(data_dict).encode('utf-8'))
                print(f"Sent data: {data_dict}")

                # Periodically flush the producer
                producer.flush()
            except Exception as e:
                print(f"Error sending data to Kafka: {e}")
        # Delay to control the rate of data fetching and sending
        time.sleep(1)