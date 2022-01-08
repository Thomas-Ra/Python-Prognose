import matplotlib.pyplot as plt #needed for model testing
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Bidirectional
from tensorflow.keras.callbacks import ModelCheckpoint, TensorBoard
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
# python scraper für yahoo finance
from yahoo_fin import stock_info as si
from collections import deque

import os
import time
import numpy as np
import pandas as pd
import random

from plot import make_plot

# seed speichern um die gleichen Ergebnisse zu erhalten
np.random.seed(314)
tf.random.set_seed(314)
random.seed(314)

#Vorbereitung des Datasets

def shuffle_in_unison(a, b):
    # mischen der beiden arrays auf die gleiche Art und Weise
    state = np.random.get_state()
    np.random.shuffle(a)
    np.random.set_state(state)
    np.random.shuffle(b)

#long function but flexible
def load_data(ticker, n_steps=50, scale=True, shuffle=True, lookup_step=1, split_by_date=True,
                test_size=0.2, feature_columns=['adjclose', 'volume', 'open', 'high', 'low']):
    """
    Lädt und verabreitet Daten von Yahoo Finance
    Params:
        ticker (str/pd.DataFrame): Aktiensymbol, das zu untersuchen ist
        n_steps (int): die Länge der historischen Sequenz (d. h. die Größe des Fensters), die für die Vorhersage verwendet wird, default: 50
        scale (bool): Sollen die PReise normalisiert werden auf [0,1]; default: True
        shuffle (bool): soll das Datenset gemischt werden?; default: True
        lookup_step (int): der vorauszusagende zukünftige Suchschritt, default: 1 (z. B. nächster Tag)
        split_by_date (bool): sollen Testdaten nach Training/Testing Datum gesplitted werden; wenn nicht dann ist der split random
        test_size (float): Anteil der Testdaten
        feature_columns (list): Liste der Merkmale, die in das Modell eingespeist werden sollen; Standard ist alles, was von yahoo_fin übergeben wird
    """
    # wurde Ticker bereits geladen?; es kann ein Dataframe oder ein Aktiensymbol übergeben werden
    if isinstance(ticker, str):
        # von yahoo finance anfragen
        df = si.get_data(ticker)
    elif isinstance(ticker, pd.DataFrame):
        # wenn bereits gealden, einfach verwenden
        df = ticker
    else:
        raise TypeError("ticker muss entweder ein String (Aktiensymbol) oder eine `pd.DataFrame` Instanz sein")
    
    # Rückgabewert der Funktion initialisieren
    result = {}

    # yahoo finance dataframe wird mit zurückgegeben
    result['df'] = df.copy()

    # überprüfen ob die zu betrachtenden Merkamle gültig/im Dataframe enthalten sind
    for col in feature_columns:
        assert col in df.columns, f"'{col}' existiert nicht im dataframe."
    
    # Datum als Spalte hinzufügen
    if "date" not in df.columns:
        df["date"] = df.index
    if scale:
        column_scaler = {}
        # normalisieren der Werte auf 0 bis 1
        for column in feature_columns:
            scaler = preprocessing.MinMaxScaler()
            df[column] = scaler.fit_transform(np.expand_dims(df[column].values, axis=1))
            column_scaler[column] = scaler
        # scaler zum Rückgabewert hinzufügen
        result["column_scaler"] = column_scaler
    
    # Zielspalte (label) durch Verschiebung um `lookup_step` hinzufügen
    df['future'] = df['adjclose'].shift(-lookup_step)
    # letzte `lookup_step` Spalten enthalten NaN in der Spalte für die Zukunft

    # speichern der Spalten bevor die NaN's entfernt werden
    last_sequence = np.array(df[feature_columns].tail(lookup_step))
    
    # NaNs entfernen
    df.dropna(inplace=True)
    sequence_data = []
    sequences = deque(maxlen=n_steps)

    for entry, target in zip(df[feature_columns + ["date"]].values, df['future'].values):
        sequences.append(entry)
        if len(sequences) == n_steps:
            sequence_data.append([np.array(sequences), target])
    # Erhalte die letzte Sequenz durch Anhängen der letzten `n_step`-Sequenz an die `lookup_step`-Sequenz.
    # Wenn zum Beispiel n_steps=50 und lookup_step=10, sollte last_sequence 60 (also 50+10) lang sein.
    # Diese last_sequence wird zur Vorhersage zukünftiger Aktienkurse verwendet, die im Datensatz nicht vorhanden sind.
    last_sequence = list([s[:len(feature_columns)] for s in sequences]) + list(last_sequence)
    last_sequence = np.array(last_sequence).astype(np.float32)

    # zum Ergebnis hinzufügen
    result['last_sequence'] = last_sequence

    # X's and y's aufbauen
    X, y = [], []
    for seq, target in sequence_data:
        X.append(seq)
        y.append(target)
    
    # umwandeln zu numpy arrays
    X = np.array(X)
    y = np.array(y)
    if split_by_date:
        # Aufteilung des Datensatzes in Trainings- und Testsätze nach Datum
        train_samples = int((1 - test_size) * len(X))
        result["X_train"] = X[:train_samples]
        result["y_train"] = y[:train_samples]
        result["X_test"]  = X[train_samples:]
        result["y_test"]  = y[train_samples:]
        if shuffle:
            #die Datensätze für das Training zu mischen (wenn der Parameter shuffle gesetzt ist)
            shuffle_in_unison(result["X_train"], result["y_train"])
            shuffle_in_unison(result["X_test"], result["y_test"])
    else:    
        # Datensatz zufällig aufteilen
        result["X_train"], result["X_test"], result["y_train"], result["y_test"] = train_test_split(X, y, 
                                                                                test_size=test_size, shuffle=shuffle)
    
    # Liste der Daten der Testreihe abrufen
    dates = result["X_test"][:, -1, -1]
   
    # Abrufen von Testmerkmalen aus dem ursprünglichen Datenrahmen
    result["test_df"] = result["df"].loc[dates]
   
    # doppelte Daten im Testdatenrahmen entfernen
    result["test_df"] = result["test_df"][~result["test_df"].index.duplicated(keep='first')]
   
    # Daten aus den Trainings-/Testsätzen entfernen und in float32 konvertieren
    result["X_train"] = result["X_train"][:, :, :len(feature_columns)].astype(np.float32)
    result["X_test"] = result["X_test"][:, :, :len(feature_columns)].astype(np.float32)
    return result

# Modelerstellung

# RNN mit Keras erstellen
# flexibles model
# Anzahl der layer, Abbruchquote, rnn cell, lossund der Optimierer können angepasst werden
def create_model(sequence_length, n_features, units=256, cell=LSTM, n_layers=2, dropout=0.3,
                loss="mean_absolute_error", optimizer="rmsprop", bidirectional=False):
    model = Sequential()
    for i in range(n_layers):
        if i == 0:
            # erstes layer
            if bidirectional:
                model.add(Bidirectional(cell(units, return_sequences=True), batch_input_shape=(None, sequence_length, n_features)))
            else:
                model.add(cell(units, return_sequences=True, batch_input_shape=(None, sequence_length, n_features)))
        elif i == n_layers - 1:
            # letztes layer
            if bidirectional:
                model.add(Bidirectional(cell(units, return_sequences=False)))
            else:
                model.add(cell(units, return_sequences=False))
        else:
            # versteckte layers
            if bidirectional:
                model.add(Bidirectional(cell(units, return_sequences=True)))
            else:
                model.add(cell(units, return_sequences=True))
        # Abbruchquote(dropout) nach jedem layer hinzufügen
        model.add(Dropout(dropout))
    model.add(Dense(1, activation="linear"))
    model.compile(loss=loss, metrics=["mean_absolute_error"], optimizer=optimizer)
    return model

# Model Training

# Länge der historischen Sequenz
N_STEPS = 50

# Lookup step, 1 ist der nächste Tag
LOOKUP_STEP = 15

# ob die Merkmalsspalten und der Ausgabepreis skaliert werden sollen
SCALE = True
scale_str = f"sc-{int(SCALE)}"

# soll der Datensatz gemischt werden
SHUFFLE = True
shuffle_str = f"sh-{int(SHUFFLE)}"

# ob der Trainings-/Testsatz nach Datum aufgeteilt werden soll
SPLIT_BY_DATE = False
split_by_date_str = f"sbd-{int(SPLIT_BY_DATE)}"

# Test-Datensatz-Split, 0.2 is 20%
TEST_SIZE = 0.2

# Merkmale, die wir zur Vorhersage des nächsten Kurswerts verwenden
FEATURE_COLUMNS = ["adjclose", "volume", "open", "high", "low"]

# date now
date_now = time.strftime("%Y-%m-%d")

### model parameter
# Anzahl RNN layers die wir nutzen
N_LAYERS = 2

# RNN cell die genutzt werden soll, default: LSTM cell
CELL = LSTM

# 256 LSTM neuronen
UNITS = 256

# 40% dropout
DROPOUT = 0.4

# bidirectional RNNs nutzen
BIDIRECTIONAL = True

### Training-Parameter
LOSS = "huber_loss" # loss Funktion für regression
OPTIMIZER = "adam" # optimizer algorithmus
BATCH_SIZE = 64 # Anzahl der in jeder Trainingsiteration verwendeten Datenproben
EPOCHS = 1000 # Anzahl der Durchläufe des Algorithmus durch die gesamte Trainingsmenge; eine höhere Zahl wird empfohlen

# Aktiensymbol
ticker = "AAPL"
ticker_data_filename = os.path.join("data", f"{ticker}_{date_now}.csv")

# model Name zum speichern
model_name = f"{date_now}_{ticker}-{shuffle_str}-{scale_str}-{split_by_date_str}-\
{LOSS}-{OPTIMIZER}-{CELL.__name__}-seq-{N_STEPS}-step-{LOOKUP_STEP}-layers-{N_LAYERS}-units-{UNITS}"
if BIDIRECTIONAL:
    model_name += "-b"

# Ordner anlegen, sollten sie noch nicht da sein
if not os.path.isdir("results"):
    os.mkdir("results")
if not os.path.isdir("logs"):
    os.mkdir("logs")
if not os.path.isdir("data"):
    os.mkdir("data")

# Daten laden
data = load_data(ticker, N_STEPS, scale=SCALE, split_by_date=SPLIT_BY_DATE, 
                shuffle=SHUFFLE, lookup_step=LOOKUP_STEP, test_size=TEST_SIZE, 
                feature_columns=FEATURE_COLUMNS)
# dataframe speichern
data["df"].to_csv(ticker_data_filename)
# model aufbauen
model = create_model(N_STEPS, len(FEATURE_COLUMNS), loss=LOSS, units=UNITS, cell=CELL, n_layers=N_LAYERS,
                    dropout=DROPOUT, optimizer=OPTIMIZER, bidirectional=BIDIRECTIONAL)
# tensorflow callbacks
checkpointer = ModelCheckpoint(os.path.join("results", model_name + ".h5"), save_weights_only=True, save_best_only=True, verbose=1)
tensorboard = TensorBoard(log_dir=os.path.join("logs", model_name))
# trainiere das Modell und speichere die Wichtungen, wenn wir ein neues optimales Modell mit ModelCheckpoint
history = model.fit(data["X_train"], data["y_train"],
                    batch_size=BATCH_SIZE,
                    epochs=EPOCHS,
                    validation_data=(data["X_test"], data["y_test"]),
                    callbacks=[checkpointer, tensorboard],
                    verbose=1)

# dataframe aufbauen 
# dataframe beinhaltet den adjclose sowie die Berechnung des Kauf- und Verkaufsgewinns
def get_final_df(model, data):
    """
    Diese Funktion nimmt die dicts "model" und "data", um 
    um einen endgültigen dataframe zu erstellen, der die Merkmale zusammen 
    mit den wahren und vorhergesagten Preisen des Testdatensatzes enthält.
    """
    # wenn der vorhergesagte zukünftige Preis höher ist als der aktuelle, 
    # dann berechne den wahren zukünftigen Preis minus den aktuellen Preis, um den Kaufgewinn zu erhalten
    buy_profit  = lambda current, pred_future, true_future: true_future - current if pred_future > current else 0
    # wenn der vorhergesagte zukünftige Preis niedriger ist als der aktuelle Preis,
    # dann subtrahieren wir den wahren zukünftigen Preis vom aktuellen Preis
    sell_profit = lambda current, pred_future, true_future: current - true_future if pred_future < current else 0
    X_test = data["X_test"]
    y_test = data["y_test"]
    # Prognosen erstellen und Preise ermitteln
    y_pred = model.predict(X_test)
    if SCALE:
        y_test = np.squeeze(data["column_scaler"]["adjclose"].inverse_transform(np.expand_dims(y_test, axis=0)))
        y_pred = np.squeeze(data["column_scaler"]["adjclose"].inverse_transform(y_pred))
    test_df = data["test_df"]
    # Hinzufügen der voraussichtlichen künftigen Preise zum Datenrahmen
    test_df[f"adjclose_{LOOKUP_STEP}"] = y_pred
    # Hinzufügen echter zukünftiger Preise zum Datenrahmen
    test_df[f"true_adjclose_{LOOKUP_STEP}"] = y_test
    # sortieren des dataframe nach Datum
    test_df.sort_index(inplace=True)
    final_df = test_df
    # die Spalte für den Kaufgewinn hinzufügen
    final_df["buy_profit"] = list(map(buy_profit, 
                                    final_df["adjclose"], 
                                    final_df[f"adjclose_{LOOKUP_STEP}"], 
                                    final_df[f"true_adjclose_{LOOKUP_STEP}"])
                                    # da wir keinen Gewinn für die letzte Sequenz haben, fügen wir 0 hinzu
                                    )
    # die Spalte für den Verkaufsgewinn hinzufügen
    final_df["sell_profit"] = list(map(sell_profit, 
                                    final_df["adjclose"], 
                                    final_df[f"adjclose_{LOOKUP_STEP}"], 
                                    final_df[f"true_adjclose_{LOOKUP_STEP}"])
                                    # da wir keinen Gewinn für die letzte Sequenz haben, fügen wir 0 hinzu
                                    )
    return final_df

# Vorhersage des nächsten zukünftigen Preises
def predict(model, data):
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

# optimale Modellgewichte aus dem Ergebnisordner laden
model_path = os.path.join("results", model_name) + ".h5"
model.load_weights(model_path)

# Evaluierung des Models
loss, mae = model.evaluate(data["X_test"], data["y_test"], verbose=0)
# Berechnung des mittleren absoluten Fehlers (inverse Skalierung)
if SCALE:
    mean_absolute_error = data["column_scaler"]["adjclose"].inverse_transform([[mae]])[0][0]
else:
    mean_absolute_error = mae

# den endgültigen Datenrahmen für den Testsatz abrufen
final_df = get_final_df(model, data)

# zukünftigen Preis vorhersagen
future_price = predict(model, data)

# accuracy = Anzahl positiver Profite
accuracy_score = (len(final_df[final_df['sell_profit'] > 0]) + len(final_df[final_df['buy_profit'] > 0])) / len(final_df)
# Berechnung des gesamten Kauf- und Verkaufsgewinns
total_buy_profit  = final_df["buy_profit"].sum()
total_sell_profit = final_df["sell_profit"].sum()
# Gesamtgewinn durch Addition von Verkauf und Kauf
total_profit = total_buy_profit + total_sell_profit
# Dividieren des Gesamtgewinns durch die Anzahl der Testmuster (Anzahl der Abschlüsse)
profit_per_trade = total_profit / len(final_df)

# print Metriken
print(f"Future price after {LOOKUP_STEP} days is {future_price:.2f}$")
print(f"{LOSS} loss:", loss)
print("Mean Absolute Error:", mean_absolute_error)
print("Accuracy score:", accuracy_score)
print("Total buy profit:", total_buy_profit)
print("Total sell profit:", total_sell_profit)
print("Total profit:", total_profit)
print("Profit per trade:", profit_per_trade)

print(final_df.tail(10))

# Speichern des endgültigen dataframes im Ordner csv-results
csv_results_folder = "csv-results"
if not os.path.isdir(csv_results_folder):
    os.mkdir(csv_results_folder)
csv_filename = os.path.join(csv_results_folder, model_name + ".csv")
final_df.to_csv(csv_filename)

# #--------------------------------------------------------------------------------------------------------------------
# # Plotting Predicition and Reality
# #--------------------------------------------------------------------------------------------------------------------
# # function plots the true and predicted values into he same plot
# def plot_graph(test_df):
#     """
#     This function plots true close price along with predicted close price
#     with blue and red colors respectively
#     """
#     plt.plot(test_df[f'true_adjclose_{LOOKUP_STEP}'], c='b')
#     plt.plot(test_df[f'adjclose_{LOOKUP_STEP}'], c='r')
#     plt.xlabel("Days")
#     plt.ylabel("Price")
#     plt.legend(["Actual Price", "Predicted Price"])
#     plt.show()

# # plot true/pred prices graph
# plot_graph(final_df)