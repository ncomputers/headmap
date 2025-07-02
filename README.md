# Crypto Heatmap Example

This project shows a simple FastAPI application that displays a color-coded
heatmap of crypto prices. If `ccxt.pro` is installed it streams real-time
ticker data from Binance via websockets. Without it the app falls back to
polling the REST API using the free `ccxt` package.

## Requirements

- Python 3.10+
- `fastapi`, `uvicorn`
- `ccxt` (install `ccxt.pro` if you have a subscription for websocket support)

Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
# optional: pip install ccxtpro
```

## Running the app

Run the server with:

```bash
python main.py
```

Then open `http://localhost:5679/` in your browser to see the heatmap.

## Notes

The example uses a background task to keep ticker information updated. When
`ccxt.pro` is available the data comes from Binance websockets. Otherwise the
task polls the REST API every second, so updates appear slightly slower.
