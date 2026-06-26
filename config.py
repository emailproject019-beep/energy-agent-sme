import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    CLICKHOUSE_URL = os.getenv("CLICKHOUSE_URL", "http://localhost:8123")
    # Endpoint where the open-web action or transaction is executed
    WEBHOOK_ACTION_URL = os.getenv("WEBHOOK_ACTION_URL", "https://httpbin.org/post")
    # Cost per kWh threshold to trigger operational changes ($ or £)
    PRICE_THRESHOLD = float(os.getenv("ENERGY_PRICE_THRESHOLD", 0.35))
    # Forces simulation mode to guarantee zero failures in GitHub/local dev environments
    USE_SIMULATION = os.getenv("USE_SIMULATION", "True").lower() in ("true", "1", "yes")

config = Config()
