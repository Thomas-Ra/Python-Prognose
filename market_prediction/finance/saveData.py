import os
import numpy as np

# dataframe aufbauen 
# dataframe beinhaltet den adjclose sowie die Berechnung des Kauf- und Verkaufsgewinns
def get_final_df(model, data, SCALE, LOOKUP_STEP):
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

def save_df(df, model_name):
    # Speichern des endgültigen dataframes im Ordner csv-results
    csv_results_folder = "csv-results"
    if not os.path.isdir(csv_results_folder):
        os.mkdir(csv_results_folder)
    csv_filename = os.path.join(csv_results_folder, model_name + ".csv")
    df.to_csv(csv_filename)