import time
from agents.watcher import TelemetryTariffAgent
from agents.thinker import PredictiveAnalyticsAgent
from agents.doer import OperationalStrategyAgent

def run_orchestration_cycle():
    print("\n--- Starting Multi-Agent Energy Optimization Loop ---")
    
    # Initialize your resilient agents
    watcher = TelemetryTariffAgent()
    thinker = PredictiveAnalyticsAgent()
    doer = OperationalStrategyAgent()

    # Step 1: Telemetry & Ingestion Ingest
    live_metrics = watcher.fetch_live_metrics()
    print(f"[1. Watcher] Active Telemetry -> Tariff: ${live_metrics['current_tariff']}/kWh, Load: {live_metrics['warehouse_load_kw']}kW")

    # Step 2: Analysis & Context Processing
    analysis = thinker.evaluate_risk(live_metrics)
    print(f"[2. Thinker] Operational Profile -> Risk Detected: {analysis['is_peak_surge']} | Recommendation: {analysis['recommended_strategy']}")

    # Step 3: Open-Web Action & Automated Transaction
    success = doer.execute_action(analysis)
    print(f"[3. Doer] Execution Loop Concluded. Status Success Flag: {success}")

if __name__ == "__main__":
    # Runs an initial test cycle immediately upon startup
    run_orchestration_cycle()
