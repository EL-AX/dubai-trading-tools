import json
import os
from datetime import datetime

ALERTS_FILE = "data/alerts_history.json"

def get_default_alerts():
    """Default alert configuration"""
    return {
        "rsi_overbought": 70,
        "rsi_oversold": 30,
        "price_change_percent": 5,  # Alert if price changes >5%
        "enabled": True
    }

def load_alerts_config(email):
    """Load user's alert configuration"""
    from src.auth import get_user_settings
    settings = get_user_settings(email)
    return settings.get("alerts", get_default_alerts())

def save_alert_config(email, config):
    """Save user's alert configuration"""
    from src.auth import get_user_settings, save_user_settings
    settings = get_user_settings(email)
    settings["alerts"] = config
    save_user_settings(email, settings)

def check_alerts(ticker, rsi, price, price_24h_ago=None):
    """Check if any alerts should be triggered"""
    alerts = []
    
    # RSI-based alerts
    if rsi > 70:
        alerts.append({
            "type": "overbought",
            "ticker": ticker,
            "rsi": rsi,
            "message": f"⚠️ {ticker} OVERBOUGHT - RSI at {rsi:.0f}",
            "severity": "warning"
        })
    if rsi < 30:
        alerts.append({
            "type": "oversold",
            "ticker": ticker,
            "rsi": rsi,
            "message": f"✅ {ticker} OVERSOLD - RSI at {rsi:.0f} (potential BUY)",
            "severity": "info"
        })
    
    # Price change alerts
    if price_24h_ago and price > 0 and price_24h_ago > 0:
        change_percent = ((price - price_24h_ago) / price_24h_ago) * 100
        if abs(change_percent) > 5:
            severity = "error" if change_percent < -5 else "success"
            direction = "📉 DOWN" if change_percent < 0 else "📈 UP"
            alerts.append({
                "type": "price_volatility",
                "ticker": ticker,
                "change_percent": change_percent,
                "message": f"{direction} {ticker} changed {abs(change_percent):.2f}% in 24h",
                "severity": severity
            })
    
    return alerts

def save_alert_history(ticker, alert_type, value, message=""):
    """Save alert to history"""
    os.makedirs(os.path.dirname(ALERTS_FILE), exist_ok=True)
    
    history = []
    if os.path.exists(ALERTS_FILE):
        try:
            with open(ALERTS_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except:
            history = []
    
    history.append({
        "timestamp": datetime.now().isoformat(),
        "ticker": ticker,
        "alert_type": alert_type,
        "value": value,
        "message": message
    })
    
    # Keep only last 1000 alerts
    history = history[-1000:]
    
    with open(ALERTS_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

def get_alert_history(limit=50):
    """Get recent alerts"""
    if not os.path.exists(ALERTS_FILE):
        return []
    try:
        with open(ALERTS_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
        return history[-limit:]  # Return last N alerts
    except:
        return []
