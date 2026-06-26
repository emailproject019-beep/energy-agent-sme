# SME Energy Multi-Agent Optimizer ⚡🤖

An autonomous, multi-agent AI system designed to help Small and Medium Enterprises (SMEs)—such as warehouses and light manufacturing units—reduce electricity overhead. The platform cross-references real-time time-series energy tariffs with active operational constraints to dynamically execute load-shifting strategies (e.g., pausing heavy equipment during volatile peak pricing surges).

This project relies on **ClickHouse** for high-speed telemetry storage, **Gensyn** for decentralized forecasting models, and the **Prometheux SaaS Platform** for deterministic, ontology-driven business rule validation.

┌────────────────────────┐      ┌────────────────────────┐      ┌────────────────────────┐
│   1. WATCHER AGENT     │ ───► │   2. THINKER AGENT     │ ───► │    3. DOER AGENT       │
│  Queries ClickHouse to │      │ Evaluates tariff thresholds│      │ Connects to Prometheux │
│  stream live telemetry │      │ and calculates cost risks. │      │ SaaS to verify rules   │
│  and grid market price.│      │                        │      │ and dispatch actions.  │
└────────────────────────┘      └────────────────────────┘      └────────────────────────┘

## 🏗️ Architecture & Agent Breakdown

The system breaks down operational complexity into a highly resilient three-agent loop:
1. **Telemetry & Tariff Agent (The Watcher):** Connects to ClickHouse to pull the latest 15-minute smart meter readings, machinery power load ($kW$), and logistics statuses.
2. **Predictive Analytics Agent (The Thinker):** Analyzes incoming tariff patterns against set critical thresholds and calculates projected hourly operational costs.
3. **Operational Strategy Agent (The Doer):** Acts as the web executor. It uploads live state parameters into the **Prometheux SaaS Cloud** to check against hard-coded business rules (written in Vadalog) before confirming automated equipment adjustments.

---

## 📂 Repository File Structure

```text
energy-agent-sme/
├── .github/
│   └── workflows/
│       └── run-agents.yml      # GitHub Actions automation pipeline (Runs every 30 mins)
├── agents/
│   ├── __init__.py
│   ├── watcher.py              # Agent 1: ClickHouse Ingestion interface
│   ├── thinker.py              # Agent 2: Cost-Risk Analytics evaluator
│   └── doer.py                 # Agent 3: Prometheux SaaS Gateway client
├── ontology/
│   └── energy_rules.vdl        # Vadalog declarative business logic rules
├── .env.example                # Sample environment variables profile
├── app.py                      # FastAPI Web Server deployment file with CORS
├── config.py                   # Secure configuration manager & fallback safety layer
├── main.py                     # Execution orchestrator connecting the 3 agents
└── requirements.txt            # Production dependencies
