import os
import csv
from datetime import datetime, timezone
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

METALPRICE_API_KEY = os.getenv("METALPRICEAPI")
BHAVCOPY_FILE = "BhavCopyDateWise_11082025.csv"
OUTPUT_CSV = "gold_rates.csv"
CSV_HEADER = ["timestamp", "source", "instrument", "price", "currency", "notes"]

def append_row(row):
     write_header = not os.path.exists(OUTPUT_CSV)
     with open(OUTPUT_CSV, "a", newline="", encoding="utf-8") as f:
          writer = csv.writer(f)
          if write_header:
               writer.writerow(CSV_HEADER)
          writer.writerow(row)

def fetch_xauusd_metalprice_api():
     url = "https://api.metalpriceapi.com/v1/latest"
     params = {
          "api_key": METALPRICE_API_KEY,
          "base": "USD",
          "currencies": "XAU",
     }
     resp = requests.get(url, params=params)
     data = resp.json()
     if not data.get("success", False):
          raise Exception(f"MetalpriceAPI Error: {data}")

     xauusd = data["rates"].get("USDXAU")
     if xauusd is None:
          raise Exception(f"Spot Gold USD price not found in API response: {data}")
     return xauusd, "USD", "MetalpriceAPI"

def parse_mcx_bhavcopy(path, commodity_symbol="GOLD"):
     df = pd.read_csv(path)

     gold_rows = df[
          (df["Instrument Name"].str.strip().str.upper() == "FUTCOM") &
          (df["Symbol"].str.strip().str.upper() == commodity_symbol.upper())
          ]

     if gold_rows.empty:
          raise ValueError(f"No {commodity_symbol} rows found in MCX Bhavcopy")

     price = float(gold_rows.iloc[0]["Close"])
     return price, "INR", "MCX_Bhavcopy"

def main():
     timestamp = datetime.now(timezone.utc).isoformat()

     try:
          xauusd_price, xauusd_ccy, xauusd_src = fetch_xauusd_metalprice_api()
          append_row([timestamp, xauusd_src, "XAU/USD", xauusd_price, xauusd_ccy, "Gold Spot (MetalpriceAPI)"])
          print(f"{timestamp} XAU/USD = {xauusd_price} {xauusd_ccy}")
     except Exception as e:
          print("XAU/USD fetch failed:", e)

     if os.path.exists(BHAVCOPY_FILE):
          try:
               mcx_price, mcx_ccy, mcx_src = parse_mcx_bhavcopy(BHAVCOPY_FILE)
               append_row([timestamp, mcx_src, "MCX Gold Futures", mcx_price, mcx_ccy, "Bhavcopy"])
               print(f"{timestamp} MCX Gold = {mcx_price} {mcx_ccy}")
          except Exception as e:
               print("MCX fetch failed:", e)
     else:
          print("Bhavcopy file not found. Download it first.")

if __name__ == "__main__":
     main()
