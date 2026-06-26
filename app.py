# app.py
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from main import run_orchestration_cycle
import clickhouse_connect

app = FastAPI(
    title="SME Energy Multi-Agent Optimizer API",
    version="1.0.0",
    description="Exposes live telemetry data and Prometheux ontology logic via clean API endpoints."
)

# Enable CORS so your React/Next.js/Vue frontend can make fetch requests without getting blocked
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, change this to your specific frontend URL (e.g., http://localhost:3000)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", summary="Check system health and database connections")
def health_check():
    """Verifies backend operational flags and connections."""
    use_sim = os.getenv("USE_SIMULATION", "True").lower() in ("true", "1")
    
    db_status = "Connected"
    if not use_sim:
        try:
            client = clickhouse_connect.get_client(
                host=os.getenv("CLICKHOUSE_HOST", "localhost"),
                port=int(os.getenv("CLICKHOUSE_PORT", 8123)),
                username=os.getenv("CLICKHOUSE_USER", "default"),
                password=os.getenv("CLICKHOUSE_PASSWORD", "")
            )
            client.ping()
        except Exception as e:
            db_status = f"Disconnected Error: {str(e)}"
            
    return {
        "api_layer": "healthy",
        "simulation_mode": use_sim,
        "clickhouse_connection": db_status
    }

@app.post("/api/v1/optimize", summary="Trigger real-time multi-agent energy check")
def optimize_energy(facility_id: str = "SME_WAREHOUSE_01"):
    """
    Executes the 3-agent orchestration cycle:
    1. Read real-time telemetry out of ClickHouse.
    2. Compute pricing and load thresholds.
    3. Run decision-making verification via Prometheux SaaS logic rules.
    """
    try:
        payload = run_orchestration_cycle(facility_id=facility_id)
        return payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent loop collapsed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Start server on local port 8000
    uvicorn.run("app.py:app", host="0.0.0.0", port=8000, reload=True)
