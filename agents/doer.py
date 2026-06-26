import json
import requests
from config import config

class OperationalStrategyAgent:
    """Agent 3: Orchestrates, monitors, and dispatches real-world actions on the open web."""
    
    def __init__(self):
        self.name = "Operational Strategy Agent"

    def execute_action(self, analysis: dict) -> bool:
        if not analysis.get("is_peak_surge"):
            print(f"[{self.name}] System stable. No open-web adjustments required.")
            return True

        # Build the payload representing the transaction/operation to perform
        action_payload = {
            "event": "TARIFF_PEAK_MITIGATION",
            "target_facility": "SME_WAREHOUSE_01",
            "action_directive": analysis["recommended_strategy"],
            "financials": {
                "triggered_at_tariff": analysis["tariff"],
                "projected_cost_hourly": analysis["potential_hourly_cost"]
            }
        }

        print(f"[{self.name} - PUBLISHING TASK] Dispatching payload to {config.WEBHOOK_ACTION_URL}...")

        try:
            # Real web transaction/action execution point
            response = requests.post(
                config.WEBHOOK_ACTION_URL, 
                json=action_payload,
                headers={"Content-Type": "application/json"},
                timeout=8
            )
            
            # MONITORING: Logging trace context for verification
            if response.status_code in (200, 201):
                print(f"[{self.name} - TRANSACTED SUCCESSFULLY] Remote server acknowledged action state change.")
                return True
            else:
                print(f"[{self.name} - MONITOR ALERT] Server rejected action with code: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            # FAIL-SAFE: Graceful interceptor prevents application crash if internet/endpoint drops
            print(f"[{self.name} - EXECUTION CRITICAL FAILURE] Web action connection failed: {e}")
            return False
