# predict.py
from DataHandiling import get_pre_process_data
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
import joblib

# Load the model and scaler
model = load_model("lstm_model.h5")
scaler = joblib.load("scaler.save")

# Load your latest data
df = get_pre_process_data()

# Scale it
scaled_data = scaler.transform(df)

# Prepare the last sequence for prediction
sequence_length = 42
input_to_predict = scaled_data[-sequence_length:]

# Predict the next time step
prediction = model.predict(input_to_predict.reshape(1, sequence_length, -1))
new_prediction = scaler.inverse_transform(prediction)

# Prepare new row as DataFrame
predicted_df = pd.DataFrame(new_prediction, columns=df.columns)

# Set the index as next timestamp
last_time_stamp = df.index[-1]
new_time_stamp = last_time_stamp + pd.Timedelta(hours=4)
predicted_df.index = [new_time_stamp]

# Combine original and prediction
new_df = pd.concat([df, predicted_df])
print("Predicted next step:")
print(predicted_df)
print("Updated DataFrame:")
print(new_df.tail(10))
