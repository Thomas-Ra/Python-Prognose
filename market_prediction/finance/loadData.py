from sklearn import preprocessing
from sklearn.model_selection import train_test_split
# python scraper für yahoo finance
from yahoo_fin import stock_info as si
from collections import deque

import numpy as np
import pandas as pd

def shuffle_in_unison(a, b):
        # mischen der beiden arrays auf die gleiche Art und Weise
        state = np.random.get_state()
        np.random.shuffle(a)
        np.random.set_state(state)
        np.random.shuffle(b)

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