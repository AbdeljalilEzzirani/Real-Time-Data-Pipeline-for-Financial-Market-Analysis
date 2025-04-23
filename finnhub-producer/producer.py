import websocket
import json
import os
from kafka import KafkaProducer
import time

# Get environment variables
FINNHUB_API_TOKEN = os.getenv("FINNHUB_API_TOKEN")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_TOPIC = "financial_data"

# Initialize Kafka Producer
def init_producer():
    try:
        return KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
    except Exception as e:
        print(f"Failed to initialize Kafka producer: {e}")
        return None

producer = init_producer()

def on_message(ws, message):
    if not producer:
        print("Kafka producer not initialized")
        return
    try:
        data = json.loads(message)
        if data['type'] == 'trade':
            producer.send(KAFKA_TOPIC, data)
            producer.flush()
            print(f"Sent to Kafka: {data}")
            time.sleep(0.1)  # Delay 100ms
    except Exception as e:
        print(f"Error processing message: {e}")

def on_error(ws, error):
    print(f"WebSocket error: {error}")

def on_close(ws, frame=None, reason=None):
    print("### WebSocket connection closed ###")

def on_open(ws):
    symbols = ["AAPL", "AMZN", "BINANCE:BTCUSDT", "MSFT", "GOOGL", "OANDA:EUR_USD"]
    for symbol in symbols:
        ws.send(json.dumps({"type": "subscribe", "symbol": symbol}))
        print(f"Subscribed to {symbol}")

def connect_websocket():
    while True:
        try:
            if not FINNHUB_API_TOKEN:
                raise ValueError("FINNHUB_API_TOKEN environment variable is not set")
            
            global producer
            if not producer:
                producer = init_producer()
            
            websocket.enableTrace(True)
            ws_url = f"wss://ws.finnhub.io?token={FINNHUB_API_TOKEN}"
            ws = websocket.WebSocketApp(
                ws_url,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close
            )
            ws.on_open = on_open
            ws.run_forever()
        except Exception as e:
            print(f"WebSocket failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    connect_websocket()

















# import websocket
# import json
# import os
# from kafka import KafkaProducer
# import time

# # Get environment variables
# FINNHUB_API_TOKEN = os.getenv("FINNHUB_API_TOKEN")
# KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
# KAFKA_TOPIC = "financial_data"

# # Initialize Kafka Producer
# def init_producer():
#     try:
#         return KafkaProducer(
#             bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
#             value_serializer=lambda v: json.dumps(v).encode('utf-8')
#         )
#     except Exception as e:
#         print(f"Failed to initialize Kafka producer: {e}")
#         return None

# producer = init_producer()

# def on_message(ws, message):
#     if not producer:
#         print("Kafka producer not initialized")
#         return
#     try:
#         data = json.loads(message)
#         if data['type'] == 'trade':
#             producer.send(KAFKA_TOPIC, data)
#             producer.flush()
#             print(f"Sent to Kafka: {data}")
#             time.sleep(0.1)  # Delay 100ms
#     except Exception as e:
#         print(f"Error processing message: {e}")

# def on_error(ws, error):
#     print(f"WebSocket error: {error}")

# def on_close(ws, frame=None, reason=None):
#     print("### WebSocket connection closed ###")

# def on_open(ws):
#     symbols = ["AAPL", "AMZN", "BINANCE:BTCUSDT", "MSFT", "GOOGL", "EURUSD"]
#     for symbol in symbols:
#         ws.send(json.dumps({"type": "subscribe", "symbol": symbol}))
#         print(f"Subscribed to {symbol}")

# def connect_websocket():
#     while True:
#         try:
#             if not FINNHUB_API_TOKEN:
#                 raise ValueError("FINNHUB_API_TOKEN environment variable is not set")
            
#             global producer
#             if not producer:
#                 producer = init_producer()
            
#             websocket.enableTrace(True)
#             ws_url = f"wss://ws.finnhub.io?token={FINNHUB_API_TOKEN}"
#             ws = websocket.WebSocketApp(
#                 ws_url,
#                 on_message=on_message,
#                 on_error=on_error,
#                 on_close=on_close
#             )
#             ws.on_open = on_open
#             ws.run_forever()
#         except Exception as e:
#             print(f"WebSocket failed: {e}. Retrying in 5 seconds...")
#             time.sleep(5)

# if __name__ == "__main__":
#     connect_websocket()