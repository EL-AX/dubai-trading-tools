import pandas as pd

class BacktestEngine:
    def __init__(self, data, initial_balance=1000):
        self.data = data
        self.balance = initial_balance
        self.initial_balance = initial_balance
        self.position = 0
        self.trades = []
        self.equity_curve = [initial_balance]
    
    def buy_signal(self, rsi):
        return rsi < 30
    
    def sell_signal(self, rsi):
        return rsi > 70
    
    def run(self, rsi_values):
        results = []
        
        for i, rsi in enumerate(rsi_values):
            if self.balance <= 0:
                break
            
            if self.buy_signal(rsi) and self.position == 0:
                self.position = 1
                entry_price = self.data['close'].iloc[i] if i < len(self.data) else 100
                results.append({"type": "buy", "price": entry_price, "rsi": rsi})
            
            elif self.sell_signal(rsi) and self.position == 1:
                self.position = 0
                exit_price = self.data['close'].iloc[i] if i < len(self.data) else 100
                results.append({"type": "sell", "price": exit_price, "rsi": rsi})
            
            self.equity_curve.append(self.balance)
        
        total_trades = len([t for t in results if t["type"] == "buy"])
        win_rate = 0
        if total_trades > 0:
            win_rate = (len([t for t in results if t["type"] == "sell"]) / total_trades) * 100
        
        return {
            "trades": results,
            "final_balance": self.balance,
            "total_profit": self.balance - self.initial_balance,
            "profit_percent": ((self.balance - self.initial_balance) / self.initial_balance) * 100,
            "total_trades": total_trades,
            "win_rate": win_rate,
            "equity_curve": self.equity_curve
        }
