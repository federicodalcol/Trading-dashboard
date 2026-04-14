import yfinance as yf
import json
from datetime import datetime
import os

def fetch_market_data():
    """
    Scarica dati di mercato e determina sentiment Risk On/Off
    """
    print("🔄 Inizio download dati...")
    
    try:
        # Scarica dati principali
        vix = yf.Ticker("^VIX").history(period="1d")['Close'].iloc[-1]
        spy = yf.Ticker("SPY").history(period="1d")['Close'].iloc[-1]
        gold = yf.Ticker("GC=F").history(period="1d")['Close'].iloc[-1]
        
        # USD Index (DXY)
        try:
            dxy = yf.Ticker("DX-Y.NYB").history(period="1d")['Close'].iloc[-1]
        except:
            dxy = 104.5  # Fallback se non disponibile
        
        # EUR/USD
        eurusd = yf.Ticker("EURUSD=X").history(period="1d")['Close'].iloc[-1]
        
        # Bitcoin
        btc = yf.Ticker("BTC-USD").history(period="1d")['Close'].iloc[-1]
        
        # Calcola variazioni percentuali (vs giorno precedente)
        vix_hist = yf.Ticker("^VIX").history(period="5d")
        spy_hist = yf.Ticker("SPY").history(period="5d")
        
        vix_change = ((vix - vix_hist['Close'].iloc[-2]) / vix_hist['Close'].iloc[-2] * 100)
        spy_change = ((spy - spy_hist['Close'].iloc[-2]) / spy_hist['Close'].iloc[-2] * 100)
        
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
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
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
        
        # Crea cartella data se non esiste
        os.makedirs('data', exist_ok=True)
        
        # Salva in JSON
        with open('data/market_data.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        print("✅ Dati aggiornati con successo!")
        print(f"   VIX: {vix:.2f} ({vix_change:+.2f}%)")
        print(f"   SPY: ${spy:.2f} ({spy_change:+.2f}%)")
        print(f"   Sentiment: {sentiment}")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore durante download: {e}")
        return False

if __name__ == "__main__":
    fetch_market_data()
