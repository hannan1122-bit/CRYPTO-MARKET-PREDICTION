from DataHandiling import get_pre_process_data
# from xgboost import XGBRegressor
import numpy as np


# model.py

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import joblib  # for saving scaler

# Load your dataset

df=get_pre_process_data()

# Scaling
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(df)

# Save the scaler
joblib.dump(scaler, "scaler.save")

# Prepare data
X, Y = [], []
sequence_length = 60
for i in range(sequence_length, len(scaled_data)):
    X.append(scaled_data[i-sequence_length:i])
    Y.append(scaled_data[i])
X = np.array(X)
Y = np.array(Y)

# Model
model = Sequential([
    LSTM(256, input_shape=(X.shape[1], X.shape[2]), activation='tanh', return_sequences=True),
    LSTM(128, activation='tanh'),
    Dense(scaled_data.shape[1])
])
model.compile(optimizer='adam', loss='mse')

# Train model
model.fit(X, Y, epochs=100, batch_size=10)

# Save the trained model
model.save("lstm_model.h5")
print("Model and scaler saved successfully!")















# --------------  USING MACHINE LEARNING MODEL BUT NOT EFFICIENT BEACUSE IT DOESNT SEE THE SEQUNECE --------------



# from sklearn.model_selection import train_test_split
# from sklearn.metrics import mean_squared_error
# X=df.drop("target",axis=1)
# y=df["target"]

# x_train,x_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)
# model=XGBRegressor()
# model.fit(x_train,y_train)
# pred=model.predict(x_test)

# mse=mean_squared_error(y_test, pred)
# rmse=np.sqrt(mse)
# print("MSE : ",mse)
# print("Target mean:", y.mean())
# print("Target std:", y.std())

# print("RMSE : ",rmse)














#                 MY PRACTICE

# import numpy as np
# from sklearn.preprocessing import MinMaxScaler

# scaler=MinMaxScaler()
# scaled_data=scaler.fit_transform(df)

# X,Y=[],[]

# sequence_length=42
# for i in range(sequence_length,len(scaled_data)):
#     X.append(scaled_data[i-sequence_length:i])
#     Y.append(scaled_data[i])

# X=np.array(X)
# Y=np.array(Y)

# import tensorflow as tf
# from tensorflow.keras.layers import Dense,LSTM
# from tensorflow.keras.models import Sequential

# model=Sequential([
#     LSTM(64,input_shape=(X.shape[1],X.shape[2]),activation='tanh',return_sequences=True),
#     LSTM(32,activation='tanh'),
#     Dense(scaled_data.shape[1])
# ])

# model.compile(optimizer='adam',loss='mse')
# model.fit(X,Y,epochs=100,batch_size=10)

# input_to_predict=scaled_data[-sequence_length:]
# prediction=model.predict(input_to_predict.reshape(1, sequence_length, -1))
# print("ORIGINAL DATA:-")
# print(df.tail())
# new_df=df.copy()

# import pandas as pd
# last_time_stamp=new_df.index[-1]

# new_time_stamp=last_time_stamp +pd.Timedelta(hours=4)

# new_prediction=scaler.inverse_transform(prediction)
# predicted_df = pd.DataFrame(new_prediction, columns=df.columns)

# predicted_df.index=[new_time_stamp]
# predicted_df = predicted_df.astype(df.dtypes)


# print("OUR PREDICTION IS: ")
# print(predicted_df)

# new_df=pd.concat([new_df,predicted_df])

# print("NEW DATAFRAME: ",new_df.tail())