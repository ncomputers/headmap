# Crypto Heatmap Example

This project shows a simple FastAPI application that uses `ccxt.pro` to stream
real-time ticker data from Binance via websockets. The data is served to a small
web page which displays a color-coded heatmap of the latest prices.

## Requirements

- Python 3.10+
- `ccxt.pro` (paid subscription) or `ccxt` for limited functionality
- `fastapi`, `uvicorn`

Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Running the app

Run the server with:

```bash
python main.py
```

Then open `http://localhost:8000/` in your browser to see the heatmap.

## Notes

The example uses a background task that keeps ticker information updated via the
Binance websocket API. Without an active `ccxt.pro` subscription the websocket
features will not work and the heatmap will remain empty.
