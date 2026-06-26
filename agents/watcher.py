# agents/watcher.py
import os
import random
import clickhouse_connect
from config import config

class TelemetryTariffAgent:
    """Agent 1: Queries ClickHouse OLAP with an automatic simulation fallback if offline."""
    
    def __init__(self):
        self.name = "Telemetry & Tariff Agent"
        self.client = None
        # Start with the default configuration setting
        self.fallback_to_simulation = config.USE_SIMULATION

        # If simulation is disabled, attempt a live connection
        if not self.fallback_to_simulation:
            try:
                host = os.getenv("CLICKHOUSE_HOST", "localhost")
                port = int(os.getenv("CLICKHOUSE_PORT", 8123))
                user = os.getenv("CLICKHOUSE_USER", "default")
                password = os.getenv("CLICKHOUSE_PASSWORD", "")
                
                # Initialize the live network connection
                self.client = clickhouse_connect.get_client(
                    host=host,
                    port=port,
                    username=user,
                    password=password,
                    connect_timeout=3  # Timeout quickly if server is unreachable
                )
                # Verify connection viability
                self.client.ping()
                print(f"[{self.name}] Successfully connected to ClickHouse at {host}:{port}")
            except Exception as e:
                print(f"[{self.name} - Network Warning] Could not reach ClickHouse: {e}")
                print(f"[{self.name}] Safely reverting to Simulation Mode for this execution cycle.")
                self.fallback_to_simulation = True

    def fetch_live_metrics(self) -> dict:
        # Safe simulated fallback prevents GitHub Actions pipeline crashes
        if self.fallback_to_simulation:
            return {
                "current_tariff": round(random.uniform(0.15, 0.55), 2),
                "warehouse_load_kw": random.randint(40, 120),
                "docking_status": random.choice(["IDLE", "LOADING"])
            }
        
        try:
            query = """
                SELECT tariff_rate_per_kwh, power_load_kw, docking_bay_status 
                FROM default.sme_energy_telemetry 
                ORDER BY timestamp DESC 
                LIMIT 1
            """
            result = self.client.query(query)
            
            if result.row_count > 0:
                latest_row = result.result_rows[0]
                return {
                    "current_tariff": float(latest_row[0]),
                    "warehouse_load_kw": float(latest_row[1]),
                    "docking_status": str(latest_row[2])
                }
        except Exception as e:
            print(f"[{self.name} - Read Error] Failed to extract ClickHouse rows: {e}.")
            
        return {"current_tariff": 0.28, "warehouse_load_kw": 60, "docking_status": "IDLE"}
