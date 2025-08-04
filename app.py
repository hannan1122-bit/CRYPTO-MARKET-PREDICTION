from flask import Flask, jsonify
from flask_cors import CORS
from DataHandiling import get_pre_process_data
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError
import joblib

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load pre-trained LSTM model and scaler
model = load_model("lstm_model.h5", compile=False)
model.compile(optimizer='adam', loss=MeanSquaredError())
scaler = joblib.load("scaler.save")

@app.route('/predict', methods=['GET'])
def predict():
    try:
        # Load and copy preprocessed data
        df = get_pre_process_data()
        new_df = df.copy()
        sequence_length = 42
        predictions = []

        # Predict next 10 future points using recursive approach
        for _ in range(10):
            # Scale latest data
            scaled_data = scaler.transform(new_df)
            input_to_predict = scaled_data[-sequence_length:]
            prediction = model.predict(input_to_predict.reshape(1, sequence_length, -1), verbose=0)
            
            # Inverse scale the prediction
            new_prediction = scaler.inverse_transform(prediction)
            predicted_df = pd.DataFrame(new_prediction, columns=df.columns)
            
            # Add timestamp to prediction
            last_time_stamp = new_df.index[-1]
            new_time_stamp = last_time_stamp + pd.Timedelta(hours=1)
            predicted_df.index = [new_time_stamp]
            
            # Add prediction to the new data
            new_df = pd.concat([new_df, predicted_df])
            predictions.append({
                "timestamp": new_time_stamp.strftime("%Y-%m-%d %H:%M:%S"),
                "close": float(predicted_df["close"].iloc[0])
            })

        # Prepare original last 40 data points
        original = df.tail(40).reset_index()
        original["timestamp"] = original[original.columns[0]].astype(str)
        original = original[["timestamp", "close"]]

        return jsonify({
            "original": original.to_dict(orient="records"),
            "predicted": predictions
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
