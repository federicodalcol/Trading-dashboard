import yfinance as yf
import json
from datetime import datetime, timedelta
import os

# ============================================
# MACRO ANALYSIS MODULE (Integrato)
# ============================================

class MacroAnalyzer:
    """
    Analizza EUR/USD e GBP/USD basandosi su:
    - Tassi di interesse
    - Inflazione (CPI)
    - COT Report sentiment
    - Rischio geopolitico
    """
    
    def __init__(self):
        # Tassi di interesse correnti (aggiorna manualmente ogni mese)
        self.interest_rates = {
            "EUR": 4.00,  # BCE
            "USD": 4.50,  # FED
            "GBP": 4.75   # BOE
        }
        
        # Inflazione CPI (aggiorna manualmente ogni mese)
        self.inflation = {
            "EUR": 2.4,   # Eurozona
            "USD": 2.6,   # USA
            "GBP": 2.5    # UK
        }
        
    def analyze_interest_rate_differential(self, pair):
        """Analizza differenziale tassi di interesse"""
        if pair == "EURUSD":
            base, quote = "EUR", "USD"
        elif pair == "GBPUSD":
            base, quote = "GBP", "USD"
        else:
            return 0, "N/A"
        
        differential = self.interest_rates[base] - self.interest_rates[quote]
        
        if differential > 0.5:
            signal = "STRONG BUY"
            score = 2
        elif differential > 0:
            signal = "BUY"
            score = 1
        elif differential < -0.5:
            signal = "STRONG SELL"
            score = -2
        elif differential < 0:
            signal = "SELL"
            score = -1
        else:
            signal = "NEUTRAL"
            score = 0
            
        return score, f"{signal} (Diff: {differential:+.2f}%)"
    
    def analyze_inflation_differential(self, pair):
        """Analizza differenziale inflazione"""
        if pair == "EURUSD":
            base, quote = "EUR", "USD"
        elif pair == "GBPUSD":
            base, quote = "GBP", "USD"
        else:
            return 0, "N/A"
        
        # Inflazione più alta = valuta più debole
        differential = self.inflation[quote] - self.inflation[base]
        
        if differential > 0.5:
            signal = "BUY"
            score = 1
        elif differential < -0.5:
            signal = "SELL"
            score = -1
        else:
            signal = "NEUTRAL"
            score = 0
            
        return score, f"{signal} (CPI Diff: {differential:+.1f}%)"
    
    def get_cot_sentiment(self, pair):
        """Analisi COT Report (semplificata)"""
        if pair == "EURUSD":
            retail_long_pct = 65
            if retail_long_pct > 70:
                return -1, "COT: Smart Money SHORT"
            elif retail_long_pct < 30:
                return 1, "COT: Smart Money LONG"
            else:
                return 0, "COT: NEUTRAL"
        
        elif pair == "GBPUSD":
            retail_long_pct = 55
            if retail_long_pct > 70:
                return -1, "COT: Smart Money SHORT"
            elif retail_long_pct < 30:
                return 1, "COT: Smart Money LONG"
            else:
                return 0, "COT: NEUTRAL"
        
        return 0, "COT: N/A"
    
    def get_geopolitical_risk(self, pair):
        """Valuta rischio geopolitico"""
        geopolitical_factors = {
            "EUR": 0,   # Stabile
            "USD": 1,   # Safe haven
            "GBP": -1   # Post-Brexit instabilità
        }
        
        if pair == "EURUSD":
            risk_diff = geopolitical_factors["EUR"] - geopolitical_factors["USD"]
            if risk_diff < 0:
                return -1, "Geo: USD Safe Haven"
            elif risk_diff > 0:
                return 1, "Geo: EUR Preferred"
            else:
                return 0, "Geo: NEUTRAL"
        
        elif pair == "GBPUSD":
            risk_diff = geopolitical_factors["GBP"] - geopolitical_factors["USD"]
            if risk_diff < 0:
                return -1, "Geo: USD Safe Haven"
            elif risk_diff > 0:
                return 1, "Geo: GBP Preferred"
            else:
                return 0, "Geo: NEUTRAL"
        
        return 0, "Geo: N/A"
    
    def get_comprehensive_analysis(self, pair):
        """Analisi completa del pair"""
        
        rate_score, rate_signal = self.analyze_interest_rate_differential(pair)
        infl_score, infl_signal = self.analyze_inflation_differential(pair)
        cot_score, cot_signal = self.get_cot_sentiment(pair)
        geo_score, geo_signal = self.get_geopolitical_risk(pair)
        
        total_score = rate_score + infl_score + cot_score + geo_score
        
        if total_score >= 3:
            final_signal = "STRONG BUY 🚀"
            signal_color = "#00b894"
        elif total_score >= 1:
            final_signal = "BUY 📈"
            signal_color = "#00b894"
        elif total_score <= -3:
            final_signal = "STRONG SELL 📉"
            signal_color = "#e74c3c"
        elif total_score <= -1:
            final_signal = "SELL 📉"
            signal_color = "#e74c3c"
        else:
            final_signal = "NEUTRAL ⚖️"
            signal_color = "#fdcb6e"
        
        return {
            "pair": pair,
            "final_signal": final_signal,
            "signal_color": signal_color,
            "total_score": total_score,
            "components": {
                "interest_rates": {
                    "score": rate_score,
                    "signal": rate_signal
                },
                "inflation": {
                    "score": infl_score,
                    "signal": infl_signal
                },
                "cot": {
                    "score": cot_score,
                    "signal": cot_signal
                },
                "geopolitical": {
                    "score": geo_score,
                    "signal": geo_signal
                }
            }
        }

def analyze_all_pairs():
    """Analizza tutti i pair"""
    analyzer = MacroAnalyzer()
    
    return {
        "EURUSD": analyzer.get_comprehensive_analysis("EURUSD"),
        "GBPUSD": analyzer.get_comprehensive_analysis("GBPUSD")
    }

# ============================================
# MARKET DATA FETCHER
# ============================================

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
    """Scarica dati di mercato e analisi macro"""
    print("🔄 Inizio download dati...")
    
    try:
        # Scarica dati di mercato
        print("📊 Downloading market data...")
        vix, vix_change = safe_download_with_change("^VIX", 20.0, 0.0)
        spy, spy_change = safe_download_with_change("SPY", 500.0, 0.0)
        gold = safe_download("GC=F", 2000.0)
        dxy = safe_download("DX-Y.NYB", 104.5)
        eurusd = safe_download("EURUSD=X", 1.08)
        btc = safe_download("BTC-USD", 50000.0)
        
        # Sentiment
        if vix > 25:
            sentiment = "RISK OFF 🛡️"
            sentiment_color = "#e74c3c"
        elif vix < 15:
            sentiment = "RISK ON 🚀"
            sentiment_color = "#00b894"
        else:
            sentiment = "NEUTRALE ⚖️"
            sentiment_color = "#fdcb6e"
        
        # Timestamp UTC+2
        now_utc_plus_2 = datetime.utcnow() + timedelta(hours=2)
        timestamp = now_utc_plus_2.strftime("%Y-%m-%d %H:%M:%S UTC+2")
        
        # Analisi macro
        print("📊 Running macro analysis...")
        macro_results = analyze_all_pairs()
        
        # Crea dati completi
        data = {
            "last_update": timestamp,
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
            },
            "macro_analysis": macro_results
        }
        
        # Salva
        os.makedirs('data', exist_ok=True)
        with open('data/market_data.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        print("✅ Dati salvati con successo!")
        print(f"   VIX: {vix:.2f} ({vix_change:+.2f}%)")
        print(f"   SPY: ${spy:.2f} ({spy_change:+.2f}%)")
        print(f"   Timestamp: {timestamp}")
        print(f"   EUR/USD: {macro_results['EURUSD']['final_signal']}")
        print(f"   GBP/USD: {macro_results['GBPUSD']['final_signal']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = fetch_market_data()
    exit(0 if success else 1)
