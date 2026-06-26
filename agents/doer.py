import os
import requests
from config import config

class OperationalStrategyAgent:
    """Agent 3: Evaluates actions via the Prometheux Standalone Cloud SaaS API."""
    
    def __init__(self):
        self.name = "Prometheux SaaS Agent"
        # Pull environment configurations dynamically
        self.api_url = os.getenv("PROMETHEUX_SAAS_URL", "https://api.prometheux.ai")
        self.token = os.getenv("PROMETHEUX_TOKEN", "mock_token")
        self.username = os.getenv("PROMETHEUX_USERNAME", "demo_user")
        self.org = os.getenv("PROMETHEUX_ORGANIZATION", "demo_org")

    def execute_action(self, analysis: dict) -> bool:
        print(f"[{self.name}] Connecting to Prometheux SaaS Engine...")

        # If in simulation mode and credentials aren't set, gracefully succeed 
        if config.USE_SIMULATION and self.token == "mock_token":
            print(f"[{self.name} - SIMULATION] Bypassing cloud call. Logic evaluated: {analysis['recommended_strategy']}.")
            return True

        # Formulate runtime factual assertions based on ClickHouse telemetry data
        payload = {
            "username": self.username,
            "organization": self.org,
            "ontology_id": "warehouse_energy_rules",
            "facts": [
                {"concept": "LiveTariff", "values": ["SME_WAREHOUSE_01", analysis["tariff"]]},
                {"concept": "CurrentLoad", "values": ["SME_WAREHOUSE_01", analysis["load_kw"]]}
            ]
        }

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        try:
            # Query the cloud reasoning gate
            response = requests.post(f"{self.api_url}/v1/projects/reason", json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                # Extract actions safely derived by Vadalog rules
                directives = result.get("derived_knowledge", {}).get("DispatchAction", [])
                
                if not directives:
                    print(f"[{self.name}] SaaS Evaluation complete: No operational adjustments needed.")
                    return True
                
                for item in directives:
                    print(f"[{self.name} - EXECUTION RULE] Triggering state change: {item['action']} on device {item['device_id']}")
                return True
            else:
                print(f"[{self.name} - Warning] SaaS gateway returned status code {response.status_code}. Using safe fallback.")
                return False

        except requests.exceptions.RequestException as e:
            print(f"[{self.name} - Error] Cloud connectivity failed: {e}. Gracefully handling fallback.")
            return False
