import os
import requests
from config import config

class OperationalStrategyAgent:
    """Agent 3: Evaluates actions via the Prometheux Standalone Cloud SaaS API."""
    
    def __init__(self):
        self.name = "Prometheux SaaS Agent"
        self.api_url = os.getenv("PROMETHEUX_SAAS_URL", "https://api.prometheux.ai")
        self.token = os.getenv("PROMETHEUX_TOKEN", "")
        self.username = os.getenv("PROMETHEUX_USERNAME", "Anupghimire1")
        self.org = os.getenv("PROMETHEUX_ORGANIZATION", "")

    def execute_action(self, analysis: dict) -> bool:
        print(f"[{self.name}] Transmitting live state facts to Prometheux SaaS model...")

        # Construct facts array matching your Vadalog schema predicates
        payload = {
            "username": self.username,
            "organization": self.org,
            "project_id": "SME_Energy_Optimization",
            "facts": [
                {"concept": "LiveTariff", "values": ["SME_WAREHOUSE_01", str(analysis["tariff"])]},
                {"concept": "LogisticsStatus", "values": ["SME_WAREHOUSE_01", str(analysis.get("docking_status", "IDLE"))]}
            ]
        }

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        try:
            # Query the cloud reasoning engine endpoint
            response = requests.post(f"{self.api_url}/v1/projects/reason", json=payload, headers=headers, timeout=12)
            
            if response.status_code == 200:
                result = response.json()
                directives = result.get("derived_knowledge", {}).get("DispatchAction", [])
                
                if not directives:
                    print(f"[{self.name}] Logic verification clear: No changes to operation schedules.")
                    return True
                
                for directive in directives:
                    print(f"──► [ACTION EXECUTED] Prometheux Rule Triggered: {directive['values'][1]} on node {directive['values'][0]}")
                return True
            else:
                print(f"[{self.name} - Network Warning] SaaS returned status code: {response.status_code}")
                return False
        except Exception as e:
            print(f"[{self.name} - Connection Failure] Could not verify logic through Prometheux cloud node: {e}")
            return False
