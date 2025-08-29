import csv
import requests
import os
from datetime import datetime

def save_id_name_to_csv(api_url):
    try:
        # Call the API
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        # Extract only "id" and "name", and replace "&amp;" with "&"
        filtered_data = [
            {"id": item["id"], "name": item["name"].replace("&amp;", "&")}
            for item in data
        ]

        # Create "upload" folder if it doesn't exist
        os.makedirs("upload", exist_ok=True)

        # Generate filename like Woo121225 (DDMMYY)
        today = datetime.today().strftime("%d%m%y")
        output_file = os.path.join("upload", f"Woo{today}.csv")

        # Save to CSV
        with open(output_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["id", "name"])
            writer.writeheader()
            writer.writerows(filtered_data)

        return {
            "Status": 200,
            "message" : output_file
        }

    except Exception as e:
        return {
            "Status": 500,
            "Error": str(e)
        }

# # Example usage:
# # Replace with your API endpoint
# api_url = "https://workflows.poptechstudio.ai/webhook/get-woo-data"
# save_id_name_to_csv(api_url)
