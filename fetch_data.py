import yfinance as yf
import json
from datetime import datetime
import os
import time

def fetch_market_data():
    """
    Scarica dati di mercato e determina sentiment Risk On/Off
    """
    print("🔄 Inizio download dati...")
    
    try:
        # Scarica VIX con retry
        print("Downloading VIX...")
        vix_ticker = yf.Ticker("^VIX")
        vix_hist = vix_ticker.history(period="5d")
        if len(vix_hist) < 2:
            raise ValueError("VIX data insufficient")
        vix = vix_hist['Close'].iloc[-1]
        vix_prev = vix_hist['Close'].iloc[-2]
        vix_change = ((vix - vix_prev) / vix_prev * 100)
        
        # Scarica SPY
        print("Downloading SPY...")
        spy_ticker = yf.Ticker("SPY")
        spy_hist = spy_ticker.history(period="5d")
        if len(spy_hist) < 2:
            raise ValueError("SPY data insufficient")
        spy = spy_hist['Close'].iloc[-1]
        spy_prev = spy_hist['Close'].iloc[-2]
        spy_change = ((spy - spy_prev) / spy_prev * 100)
        
        # Scarica Gold
        print("Downloading Gold...")
        gold_ticker = yf.Ticker("GC=F")
        gold_hist = gold_ticker.history(period="2d")
        gold = gold_hist['Close'].iloc[-1] if len(gold_hist) > 0 else 2000.0
        
        # Scarica EUR/USD
        print("Downloading EURUSD...")
        eurusd_ticker = yf.Ticker("EURUSD=X")
        eurusd_hist = eurusd_ticker.history(period="2d")
        eurusd = eurusd_hist['Close'].iloc[-1] if len(eurusd_hist) > 0 else 1.08
        
        # Scarica Bitcoin
        print("Downloading Bitcoin...")
        btc_ticker = yf.Ticker("BTC-USD")
        btc_hist = btc_ticker.history(period="2d")
        btc = btc_hist['Close'].iloc[-1] if len(btc_hist) > 0 else 50000.0
        
        # DXY (fallback se non disponibile)
        print("Downloading DXY...")
        try:
            dxy_ticker = yf.Ticker("DX-Y.NYB")
            dxy_hist = dxy_ticker.history(period="2d")
            dxy = dxy_hist['Close'].iloc[-1] if len(dxy_hist) > 0 else 104.5
        except:
            dxy = 104.5
        
        # Determina sentiment Risk On/Off
        if vix > 25:
            sentiment = "RISK OFF 🛡️"
            sentiment_color = "#e74c3c"
        elif vix < 15:
            sentiment = "RISK ON 🚀"
            sentiment_color = "#00b894"
        else:
            sentiment = "NEUTRALE ⚖️"
            sentiment_color = "#fdcb6e"
        
        # Crea oggetto dati
        data = {
            "last_update": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "sentiment": sentiment,
            "sentiment_color": sentiment_color,
            "indicators": {
                "vix": {
                    "value": round(float(vix), 2),
                    "change": round(float(vix_change), 2)
                },
                "spy": {
                    "value": round(float(spy), 2),
                    "change": round(float(spy_change), 2)
                },
                "gold": {
                    "value": round(float(gold), 2)
                },
                "dxy": {
                    "value": round(float(dxy), 2)
                },
                "eurusd": {
                    "value": round(float(eurusd), 5)
                },
                "bitcoin": {
                    "value": round(float(btc), 2)
                }
            }
        }
        
        # Crea cartella data se non esiste
        os.makedirs('data', exist_ok=True)
        
        # Salva in JSON
        with open('data/market_data.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        print("✅ Dati aggiornati con successo!")
        print(f"   VIX: {vix:.2f} ({vix_change:+.2f}%)")
        print(f"   SPY: ${spy:.2f} ({spy_change:+.2f}%)")
        print(f"   Gold: ${gold:.2f}")
        print(f"   Sentiment: {sentiment}")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore durante download: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = fetch_market_data()
    if not success:
        exit(1)
