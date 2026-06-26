import random
import requests
from config import config

class TelemetryTariffAgent:
    """Agent 1: Monitors real-time grid prices and warehouse consumption."""
    
    def __init__(self):
        self.name = "Telemetry & Tariff Agent"

    def fetch_live_metrics(self) -> dict:
        if config.USE_SIMULATION:
            # Safe, predictable data simulation to prevent API failure crashes
            return {
                "current_tariff": round(random.uniform(0.15, 0.55), 2),
                "warehouse_load_kw": random.randint(40, 120)
            }
        
        try:
            # Real-world integration layer (e.g., querying ClickHouse or external API)
            response = requests.get(f"{config.CLICKHOUSE_URL}/api/live-metrics", timeout=5)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"[{self.name} Warning] Live data fetch failed: {e}. Defaulting to safe metrics.")
            
        # Fallback payload to ensure pipeline continuous execution
        return {"current_tariff": 0.28, "warehouse_load_kw": 75}
