import pandas as pd
import os
from datetime import datetime
import requests
from io import BytesIO

def artist_title_to_csv(input_url):
    try:
        # Download Excel with relaxed SSL verification (to avoid CERTIFICATE_VERIFY_FAILED)
        response = requests.get(input_url, timeout=30, verify=False)
        response.raise_for_status()

        # Read Excel from memory buffer
        df = pd.read_excel(BytesIO(response.content))

        # Select only ARTIST and TITLE columns
        df_selected = df[["ARTIST", "TITLE"]]

        # Combine into one column with "ARTIST - TITLE"
        df_selected["ARTIST_TITLE"] = df_selected["ARTIST"].astype(str) + " - " + df_selected["TITLE"].astype(str)

        # Drop duplicates so only unique "ARTIST - TITLE" remain
        df_selected = df_selected.drop_duplicates(subset=["ARTIST_TITLE"])

        # Create upload folder if not exists
        os.makedirs("upload", exist_ok=True)

        # Build filename with today’s date (ddmmyy format)
        today_str = datetime.now().strftime("%d%m%y")   # e.g. 121225
        output_file = os.path.join("upload", f"Xls{today_str}.csv")

        # Save only the new column to CSV
        df_selected[["ARTIST_TITLE"]].to_csv(output_file, index=False)

        return output_file
    
    except Exception as e:
        return {
            "Status": 500,
            "Error": str(e)
        }

# # Example usage:
# artist_title_to_csv("https://www.cobraside.com/catalog/instock/STK_With_QTY.xlsx")
