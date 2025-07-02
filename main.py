from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import asyncio

# ccxt.pro provides the real-time websocket interface
try:
    import ccxt.pro as ccxt
except ImportError:  # fallback for environments without the pro version
    import ccxt

app = FastAPI()

# create exchange instance
exchange = ccxt.binance()

# shared dictionary for latest ticker info
latest_tickers = {}

async def watch_markets(markets):
    """Background task to keep ticker information updated via websocket."""
    while True:
        try:
            data = await exchange.watch_tickers(markets)
            for symbol, ticker in data.items():
                latest_tickers[symbol] = ticker
        except Exception as exc:  # pragma: no cover - runtime logging only
            print("watch_markets error", exc)
            await asyncio.sleep(5)

@app.on_event("startup")
async def startup_event():
    markets = ["BTC/USDT", "ETH/USDT", "BNB/USDT"]
    asyncio.create_task(watch_markets(markets))

@app.get("/", response_class=HTMLResponse)
async def get_index():
    return """
    <html>
        <head>
            <title>Crypto Heatmap</title>
            <style>
                body { font-family: Arial, sans-serif; }
                .grid { display: flex; gap: 1rem; }
                .cell { width: 100px; height: 100px; display: flex; justify-content: center; align-items: center; color: white; }
            </style>
        </head>
        <body>
            <h1>Real Time Crypto Heatmap</h1>
            <div id="heatmap" class="grid"></div>
            <script>
                const ws = new WebSocket(`ws://${location.host}/ws`);
                ws.onmessage = (event) => {
                    const data = JSON.parse(event.data);
                    const container = document.getElementById('heatmap');
                    container.innerHTML = '';
                    Object.keys(data).forEach((symbol) => {
                        const price = data[symbol]['last'];
                        const percent = data[symbol]['percentage'];
                        const cell = document.createElement('div');
                        cell.className = 'cell';
                        const hue = percent > 0 ? 120 : 0;  // green/red
                        const intensity = Math.min(Math.abs(percent), 10) * 10;
                        cell.style.backgroundColor = `hsl(${hue}, 70%, ${50 - intensity / 5}%)`;
                        cell.innerText = `${symbol}\n${price}`;
                        container.appendChild(cell);
                    });
                }
            </script>
        </body>
    </html>
    """

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            await ws.send_json({s: {
                'last': t['last'],
                'percentage': t.get('percentage', 0)
            } for s, t in latest_tickers.items()})
            await asyncio.sleep(1)
    except Exception:
        pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
