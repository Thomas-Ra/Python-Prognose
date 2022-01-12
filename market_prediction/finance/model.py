from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Bidirectional, Dense, Dropout, LSTM

import numpy as np

# RNN mit Keras erstellen
# flexibles model
# Anzahl der layer, Abbruchquote, rnn cell, lossund der Optimierer können angepasst werden
def create_model(sequence_length, n_features, units=256, n_layers=2, dropout=0.3,
                loss="mean_absolute_error", optimizer="rmsprop", bidirectional=False):
    model = Sequential()
    for i in range(n_layers):
        if i == 0:
            # erstes layer
            if bidirectional:
                model.add(Bidirectional(LSTM(units, return_sequences=True), batch_input_shape=(None, sequence_length, n_features)))
            else:
                model.add(LSTM(units, return_sequences=True, batch_input_shape=(None, sequence_length, n_features)))
        elif i == n_layers - 1:
            # letztes layer
            if bidirectional:
                model.add(Bidirectional(LSTM(units, return_sequences=False)))
            else:
                model.add(LSTM(units, return_sequences=False))
        else:
            # versteckte layers
            if bidirectional:
                model.add(Bidirectional(LSTM(units, return_sequences=True)))
            else:
                model.add(LSTM(units, return_sequences=True))
        # Abbruchquote(dropout) nach jedem layer hinzufügen
        model.add(Dropout(dropout))
    model.add(Dense(1, activation="linear"))
    model.compile(loss=loss, metrics=["mean_absolute_error"], optimizer=optimizer)
    return model

# Vorhersage des nächsten zukünftigen Preises
def predict(model, data, SCALE, N_STEPS):
    # die letzte Sequenz aus den Daten abrufen
    last_sequence = data["last_sequence"][-N_STEPS:]
    # Dimensionen erweitern
    last_sequence = np.expand_dims(last_sequence, axis=0)
    # die Vorhersage erhalten (skaliert von 0 bis 1)
    prediction = model.predict(last_sequence)
    # den Preis ermitteln (durch Umkehrung der Skalierung)
    if SCALE:
        predicted_price = data["column_scaler"]["adjclose"].inverse_transform(prediction)[0][0]
    else:
        predicted_price = prediction[0][0]
    return predicted_price