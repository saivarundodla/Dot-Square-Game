from tensorflow import keras
from sklearn.model_selection import train_test_split
import numpy as np


def model_traning():
    filepath = "playerMovesData.txt"
    data = np.genfromtxt(filepath, delimiter='\t')
    data = data.astype("int32")

    X_train, X_test, y_train, y_test = train_test_split(data[:, :-1], data[:, -1], test_size=0.3)
    X_train = np.where(X_train == -1, 2, X_train)
    X_test = np.where(X_test == -1, 2, X_test)

    model = keras.Sequential()

    model.add(keras.layers.Dense(40, input_shape=(X_train.shape[1],), activation='relu'))

    model.add(keras.layers.Dense(20, activation='relu'))

    keras.layers.Dropout(1)

    model.add(keras.layers.Dense(1, activation='linear'))

    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mean_squared_error'])

    model.fit(X_train, y_train, epochs=10, batch_size=10, validation_split=0.2, shuffle=True, verbose=1)

    model.evaluate(X_test, y_test)

    return model


model = None


def predict_model(arr):
    global model
    if model is None:
        model = model_traning()
    return model.predict(arr)
