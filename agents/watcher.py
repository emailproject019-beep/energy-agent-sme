import os
import clickhouse_connect
from config import config

class TelemetryTariffAgent:
    """Agent 1: Directly queries ClickHouse OLAP for live telemetry updates."""
    
    def __init__(self):
        self.name = "Telemetry & Tariff Agent"
        if not config.USE_SIMULATION:
            # Establish native connection to ClickHouse instance
            self.client = clickhouse_connect.get_client(
                host=os.getenv("CLICKHOUSE_HOST", "localhost"),
                port=int(os.getenv("CLICKHOUSE_PORT", 8123)),
                username=os.getenv("CLICKHOUSE_USER", "default"),
                password=os.getenv("CLICKHOUSE_PASSWORD", "")
            )

    def fetch_live_metrics(self) -> dict:
        if config.USE_SIMULATION:
            return {"current_tariff": 0.42, "warehouse_load_kw": 85, "docking_status": "IDLE"}
        
        try:
            # Query the exact latest 15-minute matrix row from the database
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
            print(f"[{self.name} - Error] Failed to read ClickHouse: {e}. Dropping to baseline backup.")
            
        return {"current_tariff": 0.28, "warehouse_load_kw": 60, "docking_status": "IDLE"}
