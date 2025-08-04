# predict.py
from DataHandiling import get_pre_process_data
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
import joblib

# Load the model and scaler
from tensorflow.keras.losses import MeanSquaredError

model = load_model("lstm_model.h5", compile=False)
model.compile(optimizer='adam', loss=MeanSquaredError())

scaler = joblib.load("scaler.save")

# Load your latest data
df = get_pre_process_data()
new_df=df.copy()

# Prepare the last sequence for prediction
sequence_length = 42

for i in range(10):
    scaled_data = scaler.transform(new_df)
    input_to_predict = scaled_data[-sequence_length:]

# Predict the next time step
    prediction = model.predict(input_to_predict.reshape(1, sequence_length, -1))
    new_prediction = scaler.inverse_transform(prediction)

# Prepare new row as DataFrame
    predicted_df = pd.DataFrame(new_prediction, columns=df.columns)

# Set the index as next timestamp
    last_time_stamp = new_df.index[-1]
    new_time_stamp = last_time_stamp + pd.Timedelta(hours=1)
    predicted_df.index = [new_time_stamp]

# Combine original and prediction
    new_df = pd.concat([new_df, predicted_df])
    print("Predicted next step:")
    print(predicted_df)

print("PREVIOUS DataFrame:")
print(df.tail(5))

print("Updated DataFrame:")
print(new_df.tail(15))



import matplotlib.pyplot as plt
import seaborn as sns

# Slice last 40 rows
original_last40 = df.tail(40)
predicted_last40 = new_df.tail(40)

# Separate real and predicted parts in new_df
real_part = predicted_last40.iloc[:30]  # first 30 known values
predicted_part = predicted_last40.iloc[30:]  # last 10 predicted values

# Set figure size
plt.figure(figsize=(14, 8))

# Plot 1: Original data (Top)
plt.subplot(2, 1, 1)
sns.lineplot(x=original_last40.index, y=original_last40["close"], label="Original Close", linewidth=2)
plt.title("Original Close Prices (Last 40 Points)")
plt.ylabel("Close Price")
plt.xticks(rotation=45)
plt.grid(True)

# Plot 2: Predicted data (Bottom)
plt.subplot(2, 1, 2)

# Plot real part of predicted data
sns.lineplot(x=real_part.index, y=real_part["close"], label="Real (from model input)", color="blue", linewidth=2)

# Plot predicted part
sns.lineplot(x=predicted_part.index, y=predicted_part["close"], label="Predicted (model output)", color="red", linewidth=2, linestyle="--")

plt.title("Predicted Close Prices (Last 40 Points)")
plt.xlabel("Time")
plt.ylabel("Close Price")
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()

# Adjust layout
plt.tight_layout()
plt.show()
