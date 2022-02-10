# prediction is based on Tutorial found on: https://www.thepythoncode.com/article/stock-price-prediction-in-python-using-tensorflow-2-and-keras
# for this parameters have been optimized and code restructed + extended
import tensorflow as tf
from tensorflow.keras.callbacks import ModelCheckpoint, TensorBoard

import os
import logging 
import time
import numpy as np
import random
import pandas as pd

from .loadData import load_data
from .model import create_model, predict
from .saveData import save_df, get_final_df
from .plot import make_plot

def predictTicker(ticker, N_STEPS=50,LOOKUP_STEP = 15, TEST_SIZE = 0.2, N_LAYERS = 2, BIDIRECTIONAL = True, BATCH_SIZE = 64, EPOCHS = 1000):
    """
        Params:
            ticker (str/pd.DataFrame): Aktiensymbol, das zu untersuchen ist
            n_steps (int): die Länge der historischen Sequenz (d. h. die Größe des Fensters), die für die Vorhersage verwendet wird, default: 50
            lookup_step (int): der vorauszusagende zukünftige Suchschritt, default: 1 (z. B. nächster Tag)
            test_size (float): Anteil der Testdaten
            n_layers (int): Anzahl RNN layers die wir nutzen
            bidirectional (bool): bidirectional RNNs nutzen
            batch_size (int): Anzahl der in jeder Trainingsiteration verwendeten Datenproben
            epochs (int): Anzahl der Durchläufe des Algorithmus durch die gesamte Trainingsmenge; eine hohe Zahl wird empfohlen
        """

    logging.info('Prediction gestartet')
    # seed speichern um die gleichen Ergebnisse zu erhalten
    np.random.seed(314)
    tf.random.set_seed(314)
    random.seed(314)

    # Skalierung der Merkmalsspalten und des Ausgabepreises
    SCALE = True
    scale_str = f"sc-{int(SCALE)}"

    # soll der Datensatz gemischt werden
    SHUFFLE = True
    shuffle_str = f"sh-{int(SHUFFLE)}"

    # ob der Trainings-/Testsatz nach Datum aufgeteilt werden soll
    SPLIT_BY_DATE = False
    split_by_date_str = f"sbd-{int(SPLIT_BY_DATE)}"

    # Merkmale, die wir zur Vorhersage des nächsten Kurswerts verwenden
    FEATURE_COLUMNS = ["adjclose", "volume", "open", "high", "low"]

    # date now
    date_now = time.strftime("%Y-%m-%d")

    ### model parameter

    # 256 LSTM neuronen
    UNITS = 256

    # 40% dropout
    DROPOUT = 0.4

    ### Training-Parameter
    LOSS = "huber_loss" # loss Funktion für regression
    OPTIMIZER = "adam" # optimizer algorithmus

    # Aktiensymbol
    ticker_data_filename = os.path.join("data", f"{ticker}_{date_now}.csv")

    # model Name zum speichern
    model_name = f"{date_now}_{ticker}-{shuffle_str}-{scale_str}-{split_by_date_str}-\
    {LOSS}-{OPTIMIZER}-LSTM-seq-{N_STEPS}-step-{LOOKUP_STEP}-layers-{N_LAYERS}-units-{UNITS}"
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
    logging.info('Aktiendaten vom Server geladen')
    # dataframe speichern
    data["df"].to_csv(ticker_data_filename)
    # model aufbauen
    model = create_model(N_STEPS, len(FEATURE_COLUMNS), loss=LOSS, units=UNITS, n_layers=N_LAYERS,
                        dropout=DROPOUT, optimizer=OPTIMIZER, bidirectional=BIDIRECTIONAL)
    # tensorflow callbacks
    checkpointer = ModelCheckpoint(os.path.join("results", model_name + ".h5"), save_weights_only=True, save_best_only=True, verbose=1)
    tensorboard = TensorBoard(log_dir=os.path.join("logs", model_name))
    # trainiere das Modell und speichere die Wichtungen, wenn wir ein neues optimales Modell mit ModelCheckpoint
    logging.info('Model Training wird gestartet')
    history = model.fit(data["X_train"], data["y_train"],
                        batch_size=BATCH_SIZE,
                        epochs=EPOCHS,
                        validation_data=(data["X_test"], data["y_test"]),
                        callbacks=[checkpointer, tensorboard],
                        verbose=1)

    # optimale Modellgewichte aus dem Ergebnisordner laden
    model_path = os.path.join("results", model_name) + ".h5"
    model.load_weights(model_path)

    # Evaluierung des Models
    logging.info('Model wird evaluiert')
    loss, mae = model.evaluate(data["X_test"], data["y_test"], verbose=0)
    # Berechnung des mittleren absoluten Fehlers (inverse Skalierung)
    if SCALE:
        mean_absolute_error = data["column_scaler"]["adjclose"].inverse_transform([[mae]])[0][0]
    else:
        mean_absolute_error = mae

    # den endgültigen Datenrahmen für den Testsatz abrufen
    final_df = get_final_df(model, data, SCALE, LOOKUP_STEP)

    # zukünftigen Preis vorhersagen
    future_price = predict(model, data, SCALE, N_STEPS)

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
    data = [
        ['Loss:', loss],  
        ['Mean Absolute Error:', mean_absolute_error],
        ['Accuracy score:', accuracy_score], 
        ['Total buy profit:', total_buy_profit], 
        ['Total sell profit:', total_sell_profit], 
        ['Total profit:', total_profit], 
        ['Profit per trade:', profit_per_trade]
    ]
    for item in data:
        print('{} {}'.format(item[0],item[1]))
     # Create the pandas DataFrame
    df = pd.DataFrame(data, columns = ['Label', 'Value'])
    df.to_csv("./market_prediction/finance/displayResults/"+ticker+".csv")
    logging.info('Ergebnisse wurden lokal gespeichert')

    save_df(final_df, model_name)
    plot_df = final_df
    make_plot(ticker, plot_df)
    
    logging.info('Prediction abgeschlossen')
