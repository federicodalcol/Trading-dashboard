import requests
from datetime import datetime, timedelta
import json

class MacroAnalyzer:
    """
    Analizza EUR/USD e GBP/USD basandosi su:
    - COT Report (Commitment of Traders)
    - Inflazione (CPI)
    - Tassi di interesse
    - Sentiment geopolitico
    """
    
    def __init__(self):
        # Tassi di interesse correnti (aggiornali manualmente ogni mese)
        self.interest_rates = {
            "EUR": 4.00,  # BCE - aggiorna manualmente
            "USD": 4.50,  # FED - aggiorna manualmente
            "GBP": 4.75   # BOE - aggiorna manualmente
        }
        
        # Inflazione CPI (aggiorna manualmente ogni mese)
        self.inflation = {
            "EUR": 2.4,   # Eurozona CPI
            "USD": 2.6,   # US CPI
            "GBP": 2.5    # UK CPI
        }
        
    def analyze_interest_rate_differential(self, pair):
        """Analizza il differenziale tassi di interesse"""
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
        """Analizza il differenziale inflazione"""
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
        """
        Simula analisi COT Report
        In produzione: scarica da CFTC.gov
        Per ora: logica simulata basata su sentiment retail
        """
        # Logica semplificata (in produzione useresti API CFTC)
        # Qui simuliamo che istituzionali fanno l'opposto dei retail
        
        # Esempio: se retail è 70% long, istituzionali sono probabilmente short
        # Quindi segnale contrarian
        
        if pair == "EURUSD":
            # Simulazione: retail sentiment
            retail_long_pct = 65  # 65% retail sono long
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
        """
        Valuta rischio geopolitico
        In produzione: analisi news API
        """
        # Fattori geopolitici base (aggiornali manualmente)
        geopolitical_factors = {
            "EUR": 0,   # 0 = stabile, -1 = rischio, 1 = safe haven
            "USD": 1,   # USD tipicamente safe haven
            "GBP": -1   # Brexit aftermath, instabilità
        }
        
        if pair == "EURUSD":
            risk_diff = geopolitical_factors["EUR"] - geopolitical_factors["USD"]
            if risk_diff < 0:
                return -1, "Geo Risk: USD Safe Haven"
            elif risk_diff > 0:
                return 1, "Geo Risk: EUR Preferred"
            else:
                return 0, "Geo Risk: NEUTRAL"
        
        elif pair == "GBPUSD":
            risk_diff = geopolitical_factors["GBP"] - geopolitical_factors["USD"]
            if risk_diff < 0:
                return -1, "Geo Risk: USD Safe Haven"
            elif risk_diff > 0:
                return 1, "Geo Risk: GBP Preferred"
            else:
                return 0, "Geo Risk: NEUTRAL"
        
        return 0, "Geo Risk: N/A"
    
    def get_comprehensive_analysis(self, pair):
        """Analisi completa del pair"""
        
        # Raccolta segnali
        rate_score, rate_signal = self.analyze_interest_rate_differential(pair)
        infl_score, infl_signal = self.analyze_inflation_differential(pair)
        cot_score, cot_signal = self.get_cot_sentiment(pair)
        geo_score, geo_signal = self.get_geopolitical_risk(pair)
        
        # Score totale
        total_score = rate_score + infl_score + cot_score + geo_score
        
        # Determina segnale finale
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
                    "signal": rate_signal,
                    "eur_rate": self.interest_rates.get("EUR", 0),
                    "usd_rate": self.interest_rates.get("USD", 0),
                    "gbp_rate": self.interest_rates.get("GBP", 0)
                },
                "inflation": {
                    "score": infl_score,
                    "signal": infl_signal,
                    "eur_cpi": self.inflation.get("EUR", 0),
                    "usd_cpi": self.inflation.get("USD", 0),
                    "gbp_cpi": self.inflation.get("GBP", 0)
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
    
    results = {
        "EURUSD": analyzer.get_comprehensive_analysis("EURUSD"),
        "GBPUSD": analyzer.get_comprehensive_analysis("GBPUSD"),
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    }
    
    return results

if __name__ == "__main__":
    results = analyze_all_pairs()
    print(json.dumps(results, indent=2))
