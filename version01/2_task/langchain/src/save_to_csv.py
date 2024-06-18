import pandas as pd
import os
from datetime import datetime

def save_to_csv(directory, descriptions):
    now = datetime.now()
    # print(now)
    df = pd.DataFrame(descriptions)
    df.columns = ["CAM Name", "Beschreibung"]
    csv_path = os.path.join(directory, f"CAM_Beschreibung_{now}.csv")
    df.to_csv(csv_path, index=False, sep=';', encoding='utf-8')