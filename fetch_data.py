import yfinance as yf
import json
from datetime import datetime, timedelta
import os

# ============================================
# MACRO ANALYSIS MODULE (Integrato)
# ============================================

class AdvancedMacroAnalyzer:
    """
    Sistema di scoring avanzato 1-100 per EUR/USD e GBP/USD
    Integra: Tassi, Inflazione, COT, VIX, Correlazioni, Momentum Tecnico
    """
    
    def __init__(self, vix_value, spy_change, gold_value, dxy_value):
        # Dati di mercato per correlazioni
        self.vix = vix_value
        self.spy_change = spy_change
        self.gold = gold_value
        self.dxy = dxy_value
        
        # Tassi di interesse (AGGIORNA MANUALMENTE)
        self.interest_rates = {
            "EUR": 4.00,  # BCE - Ultimo dato
            "USD": 4.50,  # FED - Ultimo dato
            "GBP": 4.75   # BOE - Ultimo dato
        }
        
        # Inflazione CPI (AGGIORNA MANUALMENTE)
        self.inflation = {
            "EUR": 2.4,   # Eurozona
            "USD": 2.6,   # USA
            "GBP": 2.5    # UK
        }
        
        # PIL Growth (AGGIORNA TRIMESTRALMENTE)
        self.gdp_growth = {
            "EUR": 0.9,   # % annuale
            "USD": 2.5,   # % annuale
            "GBP": 0.7    # % annuale
        }
        
    def score_interest_rates(self, pair):
        """Score 0-20 basato su differenziale tassi"""
        if pair == "EURUSD":
            base, quote = "EUR", "USD"
        elif pair == "GBPUSD":
            base, quote = "GBP", "USD"
        else:
            return 10, "N/A"
        
        diff = self.interest_rates[base] - self.interest_rates[quote]
        
        # Differenziale positivo = valuta base più forte
        if diff > 1.0:
            score = 20
            signal = "🟢 Forte vantaggio tassi"
        elif diff > 0.5:
            score = 17
            signal = "🟢 Vantaggio tassi"
        elif diff > 0.2:
            score = 14
            signal = "🟡 Leggero vantaggio"
        elif diff > -0.2:
            score = 10
            signal = "⚪ Neutrale"
        elif diff > -0.5:
            score = 6
            signal = "🟡 Leggero svantaggio"
        elif diff > -1.0:
            score = 3
            signal = "🔴 Svantaggio tassi"
        else:
            score = 0
            signal = "🔴 Forte svantaggio tassi"
        
        return score, signal
    
    def score_inflation(self, pair):
        """Score 0-15 basato su inflazione"""
        if pair == "EURUSD":
            base, quote = "EUR", "USD"
        elif pair == "GBPUSD":
            base, quote = "GBP", "USD"
        else:
            return 7, "N/A"
        
        # Inflazione più bassa = valuta più forte
        diff = self.inflation[quote] - self.inflation[base]
        
        if diff > 1.0:
            score = 15
            signal = "🟢 Inflazione favorevole"
        elif diff > 0.3:
            score = 12
            signal = "🟢 Inflazione ok"
        elif diff > -0.3:
            score = 7
            signal = "⚪ Inflazione neutrale"
        elif diff > -1.0:
            score = 3
            signal = "🔴 Inflazione sfavorevole"
        else:
            score = 0
            signal = "🔴 Inflazione critica"
        
        return score, signal
    
    def score_gdp(self, pair):
        """Score 0-10 basato su crescita PIL"""
        if pair == "EURUSD":
            base, quote = "EUR", "USD"
        elif pair == "GBPUSD":
            base, quote = "GBP", "USD"
        else:
            return 5, "N/A"
        
        diff = self.gdp_growth[base] - self.gdp_growth[quote]
        
        if diff > 1.0:
            score = 10
            signal = "🟢 PIL forte"
        elif diff > 0.3:
            score = 8
            signal = "🟢 PIL positivo"
        elif diff > -0.3:
            score = 5
            signal = "⚪ PIL neutrale"
        elif diff > -1.0:
            score = 2
            signal = "🔴 PIL debole"
        else:
            score = 0
            signal = "🔴 PIL molto debole"
        
        return score, signal
    
    def score_cot_report(self, pair):
        """Score 0-15 basato su posizionamento istituzionale"""
        # Simulazione COT (in produzione: dati CFTC reali)
        
        if pair == "EURUSD":
            # Posizionamento netto speculatori (simulato)
            net_long_pct = 58  # % posizioni long nette
            
            if net_long_pct > 70:
                score = 15
                signal = "🟢 Istituzionali molto long"
            elif net_long_pct > 55:
                score = 12
                signal = "🟢 Istituzionali long"
            elif net_long_pct > 45:
                score = 7
                signal = "⚪ COT neutrale"
            elif net_long_pct > 30:
                score = 3
                signal = "🔴 Istituzionali short"
            else:
                score = 0
                signal = "🔴 Istituzionali molto short"
        
        elif pair == "GBPUSD":
            net_long_pct = 52
            
            if net_long_pct > 70:
                score = 15
                signal = "🟢 Istituzionali molto long"
            elif net_long_pct > 55:
                score = 12
                signal = "🟢 Istituzionali long"
            elif net_long_pct > 45:
                score = 7
                signal = "⚪ COT neutrale"
            elif net_long_pct > 30:
                score = 3
                signal = "🔴 Istituzionali short"
            else:
                score = 0
                signal = "🔴 Istituzionali molto short"
        else:
            score = 7
            signal = "⚪ N/A"
        
        return score, signal
    
    def score_vix_correlation(self, pair):
        """Score 0-10 basato su VIX (Risk sentiment)"""
        # VIX alto = USD forte (safe haven)
        
        if pair == "EURUSD":
            # VIX alto = EUR debole vs USD
            if self.vix > 30:
                score = 2  # EUR debole
                signal = "🔴 VIX alto (USD safe haven)"
            elif self.vix > 25:
                score = 4
                signal = "🟡 VIX elevato"
            elif self.vix > 20:
                score = 6
                signal = "⚪ VIX normale"
            elif self.vix > 15:
                score = 8
                signal = "🟢 VIX basso"
            else:
                score = 10  # EUR forte
                signal = "🟢 VIX molto basso (risk on)"
        
        elif pair == "GBPUSD":
            # Stesso meccanismo
            if self.vix > 30:
                score = 2
                signal = "🔴 VIX alto"
            elif self.vix > 25:
                score = 4
                signal = "🟡 VIX elevato"
            elif self.vix > 20:
                score = 6
                signal = "⚪ VIX normale"
            elif self.vix > 15:
                score = 8
                signal = "🟢 VIX basso"
            else:
                score = 10
                signal = "🟢 VIX molto basso"
        else:
            score = 5
            signal = "⚪ N/A"
        
        return score, signal
    
    def score_dxy_correlation(self, pair):
        """Score 0-10 basato su forza del dollaro"""
        # DXY alto = USD forte = EUR/GBP deboli
        
        if pair in ["EURUSD", "GBPUSD"]:
            # DXY sopra 105 = USD molto forte
            if self.dxy > 107:
                score = 1
                signal = "🔴 USD fortissimo"
            elif self.dxy > 105:
                score = 3
                signal = "🔴 USD forte"
            elif self.dxy > 103:
                score = 5
                signal = "⚪ USD neutrale"
            elif self.dxy > 101:
                score = 7
                signal = "🟢 USD debole"
            else:
                score = 10
                signal = "🟢 USD molto debole"
        else:
            score = 5
            signal = "⚪ N/A"
        
        return score, signal
    
    def score_gold_correlation(self, pair):
        """Score 0-10 basato su correlazione con oro"""
        # Oro alto = risk off = USD forte
        
        if pair in ["EURUSD", "GBPUSD"]:
            if self.gold > 2100:
                score = 3
                signal = "🟡 Oro alto (risk off)"
            elif self.gold > 2000:
                score = 5
                signal = "⚪ Oro normale"
            elif self.gold > 1900:
                score = 7
                signal = "🟢 Oro basso"
            else:
                score = 9
                signal = "🟢 Oro molto basso"
        else:
            score = 5
            signal = "⚪ N/A"
        
        return score, signal
    
    def score_equity_momentum(self, pair):
        """Score 0-10 basato su momentum azionario"""
        # SPY in crescita = risk on = EUR/GBP forti vs USD
        
        if pair in ["EURUSD", "GBPUSD"]:
            if self.spy_change > 1.5:
                score = 10
                signal = "🟢 Risk on forte"
            elif self.spy_change > 0.5:
                score = 8
                signal = "🟢 Risk on"
            elif self.spy_change > -0.5:
                score = 5
                signal = "⚪ Neutrale"
            elif self.spy_change > -1.5:
                score = 3
                signal = "🔴 Risk off"
            else:
                score = 0
                signal = "🔴 Risk off forte"
        else:
            score = 5
            signal = "⚪ N/A"
        
        return score, signal
    
    def score_geopolitical(self, pair):
        """Score 0-10 basato su fattori geopolitici"""
        geo_risk = {
            "EUR": 5,   # Neutrale (0-10 scale)
            "USD": 7,   # Leggero safe haven
            "GBP": 4    # Post-Brexit instabilità
        }
        
        if pair == "EURUSD":
            diff = geo_risk["EUR"] - geo_risk["USD"]
            score = max(0, min(10, 5 + diff * 2))
            
            if score > 7:
                signal = "🟢 Geo favorevole"
            elif score > 4:
                signal = "⚪ Geo neutrale"
            else:
                signal = "🔴 Geo sfavorevole"
        
        elif pair == "GBPUSD":
            diff = geo_risk["GBP"] - geo_risk["USD"]
            score = max(0, min(10, 5 + diff * 2))
            
            if score > 7:
                signal = "🟢 Geo favorevole"
            elif score > 4:
                signal = "⚪ Geo neutrale"
            else:
                signal = "🔴 Geo sfavorevole"
        else:
            score = 5
            signal = "⚪ N/A"
        
        return score, signal
    
    def get_comprehensive_score(self, pair):
        """Calcola score totale 0-100"""
        
        # Raccolta scores (totale peso: 100)
        rate_score, rate_signal = self.score_interest_rates(pair)      # 0-20
        infl_score, infl_signal = self.score_inflation(pair)            # 0-15
        gdp_score, gdp_signal = self.score_gdp(pair)                    # 0-10
        cot_score, cot_signal = self.score_cot_report(pair)             # 0-15
        vix_score, vix_signal = self.score_vix_correlation(pair)        # 0-10
        dxy_score, dxy_signal = self.score_dxy_correlation(pair)        # 0-10
        gold_score, gold_signal = self.score_gold_correlation(pair)     # 0-10
        equity_score, equity_signal = self.score_equity_momentum(pair)  # 0-10
        geo_score, geo_signal = self.score_geopolitical(pair)           # 0-10
        
        # Score totale (0-100)
        total_score = (rate_score + infl_score + gdp_score + cot_score + 
                      vix_score + dxy_score + gold_score + equity_score + geo_score)
        
        # Determina segnale finale
        if total_score >= 75:
            final_signal = "STRONG BUY 🚀🚀"
            signal_color = "#00b894"
            recommendation = "Forte opportunità di acquisto"
        elif total_score >= 60:
            final_signal = "BUY 📈"
            signal_color = "#00b894"
            recommendation = "Segnale di acquisto"
        elif total_score >= 45:
            final_signal = "NEUTRAL ⚖️"
            signal_color = "#fdcb6e"
            recommendation = "Attendere conferme"
        elif total_score >= 30:
            final_signal = "SELL 📉"
            signal_color = "#e17055"
            recommendation = "Segnale di vendita"
        else:
            final_signal = "STRONG SELL 🔴🔴"
            signal_color = "#e74c3c"
            recommendation = "Forte segnale di vendita"
        
        return {
            "pair": pair,
            "score": round(total_score, 1),
            "final_signal": final_signal,
            "signal_color": signal_color,
            "recommendation": recommendation,
            "components": {
                "interest_rates": {"score": rate_score, "max": 20, "signal": rate_signal},
                "inflation": {"score": infl_score, "max": 15, "signal": infl_signal},
                "gdp": {"score": gdp_score, "max": 10, "signal": gdp_signal},
                "cot_report": {"score": cot_score, "max": 15, "signal": cot_signal},
                "vix": {"score": vix_score, "max": 10, "signal": vix_signal},
                "dxy": {"score": dxy_score, "max": 10, "signal": dxy_signal},
                "gold": {"score": gold_score, "max": 10, "signal": gold_signal},
                "equity": {"score": equity_score, "max": 10, "signal": equity_signal},
                "geopolitical": {"score": geo_score, "max": 10, "signal": geo_signal}
            }
        }

def analyze_all_pairs(vix, spy_change, gold, dxy):
    """Analizza tutti i pair con scoring avanzato"""
    analyzer = AdvancedMacroAnalyzer(vix, spy_change, gold, dxy)
    
    return {
        "EURUSD": analyzer.get_comprehensive_score("EURUSD"),
        "GBPUSD": analyzer.get_comprehensive_score("GBPUSD")
    }
