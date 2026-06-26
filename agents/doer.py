import requests
from config import config

class OperationalStrategyAgent:
    """Agent 3: Evaluates actions using the Prometheux Reasoning Engine via API/MCP."""
    
    def __init__(self):
        self.name = "Prometheux Orchestration Agent"
        # Prometheux endpoint setup (SaaS, local Docker, or Snowflake Native App link)
        self.prometheux_api = f"{config.PROMETHEUX_URL}/v1/reason"

    def execute_action(self, analysis: dict) -> bool:
        print(f"[{self.name}] Initiating ontology cross-examination...")

        # Fact payload sent into the Prometheux execution context
        context_facts = {
            "ontology_profile": "sme_energy_v1",
            "runtime_facts": [
                {"fact": "LiveTariff", "args": ["SME_WAREHOUSE_01", analysis["tariff"]]},
                {"fact": "CriticalThreshold", "args": ["SME_WAREHOUSE_01", config.PRICE_THRESHOLD]}
            ]
        }

        try:
            # Query the Prometheux reasoning platform
            response = requests.post(
                self.prometheux_api,
                json=context_facts,
                headers={"Authorization": f"Bearer {config.PROMETHEUX_API_KEY}"},
                timeout=10
            )
            
            if response.status_code == 200:
                reasoning_result = response.json()
                directives = reasoning_result.get("inferences", {}).get("DispatchAction", [])
                
                if not directives:
                    print(f"[{self.name}] Prometheux safely concluded: No actions allowed under current operational rules.")
                    return True

                for directive in directives:
                    machine_id, action = directive["args"][0], directive["args"][1]
                    print(f"[{self.name} - DETERMINISTIC ACTION APPROVED] Executing {action} on device {machine_id}.")
                    # Here, the agent triggers the open-web webhook safely grounded by data provenance
                return True
            else:
                print(f"[{self.name} - Error] Prometheux engine rejected request: {response.status_code}")
                return False

        except Exception as e:
            print(f"[{self.name} - Error] Connection to Prometheux failed: {e}")
            return False
