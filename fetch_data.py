import yfinance as yf
import json
from datetime import datetime
import os

def safe_download(ticker_symbol, default_value):
    """Download sicuro con fallback"""
    try:
        ticker = yf.Ticker(ticker_symbol)
        hist = ticker.history(period="5d")
        if len(hist) > 0:
            return float(hist['Close'].iloc[-1])
        return default_value
    except Exception as e:
        print(f"⚠️ Errore scaricando {ticker_symbol}: {e}")
        return default_value

def safe_download_with_change(ticker_symbol, default_value, default_change):
    """Download con calcolo variazione"""
    try:
        ticker = yf.Ticker(ticker_symbol)
        hist = ticker.history(period="5d")
        if len(hist) >= 2:
            current = float(hist['Close'].iloc[-1])
            previous = float(hist['Close'].iloc[-2])
            change = ((current - previous) / previous * 100)
            return current, change
        return default_value, default_change
    except Exception as e:
        print(f"⚠️ Errore scaricando {ticker_symbol}: {e}")
        return default_value, default_change

def fetch_market_data():
    """Scarica dati di mercato"""
    print("🔄 Inizio download dati...")
    
    try:
        # Scarica VIX con variazione
        print("📊 Downloading VIX...")
        vix, vix_change = safe_download_with_change("^VIX", 20.0, 0.0)
        
        # Scarica SPY con variazione
        print("📊 Downloading SPY...")
        spy, spy_change = safe_download_with_change("SPY", 500.0, 0.0)
        
        # Scarica altri ticker
        print("📊 Downloading Gold...")
        gold = safe_download("GC=F", 2000.0)
        
        print("📊 Downloading DXY...")
        dxy = safe_download("DX-Y.NYB", 104.5)
        
        print("📊 Downloading EURUSD...")
        eurusd = safe_download("EURUSD=X", 1.08)
        
        print("📊 Downloading Bitcoin...")
        btc = safe_download("BTC-USD", 50000.0)
        
        # Determina sentiment
        if vix > 25:
            sentiment = "RISK OFF 🛡️"
            sentiment_color = "#e74c3c"
        elif vix < 15:
            sentiment = "RISK ON 🚀"
            sentiment_color = "#00b894"
        else:
            sentiment = "NEUTRALE ⚖️"
            sentiment_color = "#fdcb6e"
        
        # Crea dati
        data = {
            "last_update": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "sentiment": sentiment,
            "sentiment_color": sentiment_color,
            "indicators": {
                "vix": {
                    "value": round(vix, 2),
                    "change": round(vix_change, 2)
                },
                "spy": {
                    "value": round(spy, 2),
                    "change": round(spy_change, 2)
                },
                "gold": {
                    "value": round(gold, 2)
                },
                "dxy": {
                    "value": round(dxy, 2)
                },
                "eurusd": {
                    "value": round(eurusd, 5)
                },
                "bitcoin": {
                    "value": round(btc, 2)
                }
            }
        }
        
        # Salva
        os.makedirs('data', exist_ok=True)
        with open('data/market_data.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        print("✅ Dati salvati con successo!")
        print(f"   VIX: {vix:.2f} ({vix_change:+.2f}%)")
        print(f"   SPY: ${spy:.2f} ({spy_change:+.2f}%)")
        print(f"   Sentiment: {sentiment}")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = fetch_market_data()
    exit(0 if success else 1)
