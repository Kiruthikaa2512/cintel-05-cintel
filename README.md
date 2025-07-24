# Global Climate Monitor by Kiruthikaa

A real-time dashboard built with PyShiny Express that simulates temperature and humidity readings over time, visualized via responsive cards, data grids, and trend charts.

## Features
- Live data updates every second
- Value boxes for temperature, humidity, and timestamp
- Data grid showing last 20 readings
- Trend chart for temperature using linear regression
- **Enhanced Feature**: Additional chart for humidity with its own predictive trend line

## Technologies
- PyShiny Express
- Pandas for data management
- Plotly for interactive charts
- faicons for expressive icons
- scipy for regression analytics

## Run Locally

```bash
python -m venv .venv
source .venv/bin/activate    # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app:app --reload