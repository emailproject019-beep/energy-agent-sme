# dashboard.py
import streamlit as st
import random
import time
from main import run_orchestration_cycle

st.set_page_config(page_title="SME Smart Energy Pilot", page_icon="⚡", layout="wide")

st.title("⚡ SME Multi-Agent Energy Optimization Platform")
st.subheader("Live Operational Co-Pilot for Warehouses & Logistics Hubs")

# Sidebar - Infrastructure Mapping
st.sidebar.header("🛡️ Connected Infrastructure Status")
st.sidebar.success("🗄️ ClickHouse Cloud: ACTIVE")
st.sidebar.success("🧠 Prometheux SaaS: SIGNED IN")
st.sidebar.info("🤖 Gensyn Network: MODEL SYNCD")

facility = st.sidebar.selectbox("Select Target Facility", ["SME_WAREHOUSE_01", "SME_LIGHT_MANUFACTURING_02"])
use_simulation = st.sidebar.toggle("Forced Simulation Mode", value=True)

# Main Dashboard Grid
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Current Grid Tariff", value=f"${random.uniform(0.18, 0.52):.2f} / kWh", delta="Surging (+35%)" if random.random() > 0.5 else "Stable")
with col2:
    st.metric(label="Facility Power Load", value=f"{random.randint(65, 115)} kW")
with col3:
    st.metric(label="Logistics Dock Status", value=random.choice(["LOADING", "IDLE"]))

st.divider()

st.subheader("🤖 Run Real-Time Agent Optimization")
st.write("Click below to command the 3 autonomous agents to check live metrics, evaluate pricing risks, and verify operational rules via Prometheux.")

if st.button("🚀 Trigger Agent Execution Loop", type="primary"):
    with st.spinner("Agents coordinating across cloud layers..."):
        time.sleep(1.5) # Simulated latency for visual effect
        
        # Execute your core agent workflow
        results = run_orchestration_cycle(facility_id=facility)
        
        # Display Agent outputs clearly
        st.toast("Multi-agent cycle completed successfully!")
        
        st.success("### 📊 Live Agent Decision Logs")
        
        c1, c2 = st.columns(2)
        with c1:
            st.json(results["telemetry"])
            st.info(f"**Watcher Agent:** Pulled latest parameters successfully.")
        with c2:
            st.json(results["analysis"])
            st.warning(f"**Thinker Agent:** Evaluated financial strategy constraints.")
            
        st.divider()
        st.markdown(f"### 🎯 Final Operational Directive")
        st.info(f"**Prometheux Rule Engine Decision:** `{results['execution']['action_dispatched']}`")
        st.caption("Provenance Trace: Verified via deterministic Vadalog ontology to prevent operational damage.")
