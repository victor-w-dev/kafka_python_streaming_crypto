from kafka import KafkaConsumer
import pandas as pd
import json
from datetime import datetime

kafka_server_ip = '' #input kafka server ip here or use logging dotenv

consumer = KafkaConsumer(
    'BTCUSDT-1min', #subscribe the topic
    bootstrap_servers=f'{kafka_server_ip}:9092',
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='consumer-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Function to process and group the data
def process_and_group_data(data_list):
    df = pd.DataFrame(data_list)
    
    # Count occurrences for each (Time, Open) pair
    counted = df.groupby(['Time']).size().reset_index(name='kafka_record_count')
    
    grouped = df.groupby(['Time']).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Volume': 'last',
        'Turnover': 'last'
    }).reset_index()
    
    # Merge the count with the grouped DataFrame
    result = pd.merge(grouped, counted, on=['Time'])

    result['Datetime'] = pd.to_datetime(result['Time'], unit='ms').dt.strftime('%Y-%m-%d %H:%M:%S')
    result.set_index('Datetime', inplace=True)
    #print(result)
    
    return result

data_list = []
grouped_df = pd.DataFrame()  # Initialize an empty DataFrame to store the grouped data
previous_time = None  # Initialize the previous time as None

for message in consumer:
    try:
        message = message.value
        print(f"Received data: {message}")
        data_list.append(message)
    
        # Get the time from the current message
        current_time = message['Time']
    
        # Check if the current time is greater than the previous time
        if previous_time is not None and current_time > previous_time:
            grouped_data = process_and_group_data(data_list)
            
            if grouped_df.empty:
                grouped_df = grouped_data
            else:
               # Concatenate the DataFrames
                grouped_df = pd.concat([grouped_df, grouped_data])
                
                # Drop duplicates based on the index
                grouped_df = grouped_df[~grouped_df.index.duplicated(keep='last')]
            
            data_list = []  # Reset the list for the new minute
            previous_time = current_time
            
            print(grouped_df)  # Print the updated DataFrame (optional)
        else:
            # Update the previous time to the current time if previous_time was None
            previous_time = current_time
    
    except Exception as e:
        # Print any errors encountered while processing messages
        print(f"Error processing message: {e}")