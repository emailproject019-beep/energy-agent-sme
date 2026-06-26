# agents/thinker.py
from config import config

class PredictiveAnalyticsAgent:
    """Agent 2: Analyzes current cost metrics and forecasts threshold violations."""
    
    def __init__(self):
        self.name = "Predictive Analytics Agent"

    def evaluate_risk(self, metrics: dict) -> dict:
        tariff = metrics.get("current_tariff", 0.0)
        load = metrics.get("warehouse_load_kw", 0)
        docking_status = metrics.get("docking_status", "IDLE")
        
        # Determine if current pricing exceeds our operational threshold
        is_peak_surge = tariff > config.PRICE_THRESHOLD
        potential_hourly_cost = round(load * tariff, 2)
        
        recommendation = "CONTINUE_NORMAL_OPERATIONS"
        if is_peak_surge:
            recommendation = "PAUSE_NON_ESSENTIAL_HEAVY_MACHINERY"

        return {
            "tariff": tariff,
            "load_kw": load,
            "docking_status": docking_status,
            "is_peak_surge": is_peak_surge,
            "potential_hourly_cost": potential_hourly_cost,
            "recommended_strategy": recommendation
        }
