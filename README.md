# Gold Rates Fetcher

This Python script fetches the **XAU/USD** spot gold price from MetalpriceAPI and the **MCX Gold Futures** price from an MCX Bhavcopy file, then stores both in a CSV file.

## Features

- Fetches **XAU/USD** spot gold price using [MetalpriceAPI](https://metalpriceapi.com).
- Reads **MCX Gold Futures** closing price from an MCX daily Bhavcopy CSV file.
- Appends data into a CSV (`gold_rates.csv`) with timestamp.
- Handles missing files and API errors gracefully.

## Requirements

- Python 3.8+
- Requests
- Pandas
- python-dotenv

## Install dependencies:

pip install -r requirements.txt


## Environment Variables

Create a `.env` file in the project folder with:


## METALPRICEAPI=your_api_key_here

You can get your API key from [metalpriceapi.com](https://metalpriceapi.com).

## Usage

1. Place the MCX Bhavcopy CSV in the project folder.  
   Example file name: BhavCopyDateWise_11082025.csv


## Notes

- If MCX Bhavcopy file is missing, the script will skip MCX data.
- MetalpriceAPI provides rates with limitations on free plans.
