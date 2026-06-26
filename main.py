# main.py
from agents.watcher import TelemetryTariffAgent
from agents.thinker import PredictiveAnalyticsAgent
from agents.doer import OperationalStrategyAgent

def run_orchestration_cycle(facility_id: str = "SME_WAREHOUSE_01") -> dict:
    """Orchestrates the multi-agent pipeline and gathers results for the API layer."""
    
    # Initialize agents
    watcher = TelemetryTariffAgent()
    thinker = PredictiveAnalyticsAgent()
    doer = OperationalStrategyAgent()

    # 1. Gather Telemetry (ClickHouse)
    # Note: If your fetch_live_metrics method doesn't take facility_id yet, 
    # it will default to the latest globally or can be expanded later.
    live_metrics = watcher.fetch_live_metrics()

    # 2. Process Risk Matrix
    analysis = thinker.evaluate_risk(live_metrics)

    # 3. Deterministic Validation & Action (Prometheux SaaS)
    action_executed = doer.execute_action(analysis)

    # Consolidate complete execution footprint for the UI dashboard
    return {
        "facility_id": facility_id,
        "status": "success",
        "telemetry": {
            "current_tariff_kwh": live_metrics.get("current_tariff"),
            "current_load_kw": live_metrics.get("warehouse_load_kw"),
            "docking_status": live_metrics.get("docking_status")
        },
        "analysis": {
            "is_peak_surge": analysis.get("is_peak_surge"),
            "potential_hourly_cost": analysis.get("potential_hourly_cost"),
            "recommended_strategy": analysis.get("recommended_strategy")
        },
        "execution": {
            "prometheux_verified": action_executed,
            "action_dispatched": analysis.get("recommended_strategy") if analysis.get("is_peak_surge") else "NONE"
        }
    }

if __name__ == "__main__":
    # Fallback to standard terminal testing if executed directly
    print(run_orchestration_cycle())
