import streamlit as st
import google.generativeai as genai
import os
import datetime

# ==============================================================================
# 1. UI CONFIGURATION & BRANDING
# ==============================================================================
st.set_page_config(page_title="Raza Enterprises Inc", page_icon="🏭", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0b0f19; font-family: 'Segoe UI', sans-serif; }
    
    /* Brand Header */
    .brand-header {
        background: linear-gradient(90deg, #020024 0%, #090979 35%, #00d4ff 100%);
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 25px;
        border: 1px solid #00d4ff;
        box-shadow: 0 0 25px rgba(0, 212, 255, 0.3);
    }
    .brand-text {
        font-size: 2.8rem;
        font-weight: 800;
        color: #fff;
        text-transform: uppercase;
        letter-spacing: 4px;
        text-shadow: 2px 2px 4px #000;
    }
    .sub-brand { color: #e0f7fa; font-size: 1.1rem; letter-spacing: 2px; font-weight: 300;}

    /* Cards */
    .tech-card {
        background-color: #161b22;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid;
        margin-bottom: 20px;
        color: #e6edf3;
        height: 100%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .card-title { font-size: 1.2rem; font-weight: bold; margin-bottom: 15px; display: block; color: white; border-bottom: 1px solid #333; padding-bottom: 5px;}
    
    /* Status Colors */
    .analysis { border-color: #d2a8ff; }
    .gauges { border-color: #ff7b72; }
    .yield { border-color: #79c0ff; }
    .comm { border-color: #7ee787; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. SIDEBAR (SMART MODEL DETECTION)
# ==============================================================================
with st.sidebar:
    st.markdown("<h3 style='color: #00d4ff; text-align: center;'>SYSTEM CONTROL</h3>", unsafe_allow_html=True)
    
    api_key = st.text_input("🔑 Google API Key", type="password")
    
    # 🚨 AUTO-DETECT LOGIC (Fixes the 404 Error)
    valid_models = []
    if api_key:
        try:
            genai.configure(api_key=api_key)
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    # Clean up the name (remove "models/")
                    valid_models.append(m.name.replace("models/", ""))
        except:
            pass
    
    # Fallback if detection fails
    if not valid_models:
        valid_models = ["gemini-1.5-flash", "gemini-pro"]
        
    model_name = st.selectbox("🤖 AI Core Engine", valid_models)
    
    st.success(f"System Online: {model_name}")
    st.divider()
    st.caption("© 2025 Raza Enterprises Inc.")

# ==============================================================================
# 3. HEADER
# ==============================================================================
st.markdown("""
<div class="brand-header">
    <div class="brand-text">RAZA ENTERPRISES INC</div>
    <div class="sub-brand">ADVANCED SPINNING SIMULATION SUITE V6.0</div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 4. DETAILED INPUTS
# ==============================================================================
tab1, tab2, tab3 = st.tabs(["🧶 RAW MATERIAL", "⚙️ MACHINERY SETUP", "🎯 TARGETS"])

with tab1:
    fiber_input = st.text_area("Fiber Specifications", height=150, 
        placeholder="e.g. 100% US Cotton, Staple 1-1/8, Mic 4.2...")

with tab2:
    st.markdown("#### 🏭 Plant Configuration Details")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("**1. Preparation**")
        blow_cap = st.number_input("Blowroom Cap (kg/hr)", value=800)
        blow_eff = st.number_input("Blowroom Eff %", value=85)
        card_prod = st.number_input("Card Prod (kg/hr)", value=60)
        
    with c2:
        st.markdown("**2. Spinning Frame**")
        spindles = st.number_input("Total Ring Spindles", value=25000)
        ring_speed = st.number_input("Spindle Speed (RPM)", value=18500)
        ring_eff = st.number_input("Ring Eff %", value=95)
        
    with c3:
        st.markdown("**3. Winding / Post-Spin**")
        wind_drums = st.number_input("Auto-Coner Drums", value=600)
        wind_speed = st.number_input("Winding Speed (m/min)", value=1300)
        wind_eff = st.number_input("Winding Eff %", value=88)

with tab3:
    t1, t2 = st.columns(2)
    with t1:
        target_count = st.number_input("Target Count (Ne)", value=30)
    with t2:
        yarn_twist = st.number_input("Twist Multiplier (TM)", value=4.0)

# ==============================================================================
# 5. UNIFIED AGENT LOGIC
# ==============================================================================
def run_raza_simulation(fiber, count, tm, machinery_data):
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)

    # UNIFIED PROMPT (All inputs included)
    prompt = f"""
    Act as the Technical Board of Raza Enterprises.
    Generate a full Spinning Project Report based on these inputs:
    
    RAW MATERIAL: {fiber}
    TARGET: Ne {count}, TM {tm}
    
    MACHINERY DATA:
    - Blowroom: {machinery_data['blow_cap']} kg/hr @ {machinery_data['blow_eff']}% eff
    - Carding: {machinery_data['card_prod']} kg/hr/machine
    - Ring Frame: {machinery_data['spindles']} Spindles @ {machinery_data['ring_speed']} RPM @ {machinery_data['ring_eff']}% eff
    - Winding: {machinery_data['wind_drums']} Drums @ {machinery_data['wind_speed']} m/min @ {machinery_data['wind_eff']}% eff

    ------------------------------------------------------------------
    GENERATE 4 SECTIONS. SEPARATE EACH SECTION WITH "|||".
    ------------------------------------------------------------------
    
    SECTION 1: FIBER ANALYSIS
    - Assess quality.
    - Identify spinning risks (neps, trash, moisture).
    
    |||
    
    SECTION 2: MACHINE GAUGE SETTINGS (Technical)
    - Blowroom Beater Settings.
    - Carding Settings (Cylinder-Flat gauge).
    - Drawframe Roller Distances.
    - Ring Frame Spacer Size & Break Draft.
    
    |||
    
    SECTION 3: PRODUCTION & YIELD (Calculations)
    - Calculate TPI = {tm} * sqrt({count}).
    - Calculate Grams/Spindle/Shift (8hrs) = (RPM * 0.024 * 60 * 8 * RingEff) / (TPI * Count).
    - Calculate Total Ring Production (Tons/Day).
    - Check if Blowroom ({machinery_data['blow_cap']} kg/hr) can feed this production.
    - Check if Winding capacity balances with Ring Production.
    
    |||
    
    SECTION 4: COMMERCIAL STRATEGY
    - Best end-use application.
    - Market positioning (Low/Med/High).
    """

    response = model.generate_content(prompt)
    
    try:
        parts = response.text.split("|||")
        if len(parts) < 4: return response.text, "Processing...", "Processing...", "Processing..."
        return parts[0].strip(), parts[1].strip(), parts[2].strip(), parts[3].strip()
    except:
        return response.text, "Error", "Error", "Error"

# ==============================================================================
# 6. EXECUTION
# ==============================================================================
if st.button("🚀 START PRODUCTION SIMULATION", type="primary", use_container_width=True):
    if not api_key:
        st.error("⚠️ SYSTEM LOCKED: ENTER GOOGLE API KEY")
    elif not fiber_input:
        st.warning("⚠️ DATA MISSING: ENTER FIBER SPECS")
    else:
        with st.spinner("🔄 RAZA AI AGENTS ARE CALCULATING..."):
            try:
                # Pack machinery data
                machinery = {
                    'blow_cap': blow_cap, 'blow_eff': blow_eff,
                    'card_prod': card_prod,
                    'spindles': spindles, 'ring_speed': ring_speed, 'ring_eff': ring_eff,
                    'wind_drums': wind_drums, 'wind_speed': wind_speed, 'wind_eff': wind_eff
                }
                
                r1, r2, r3, r4 = run_raza_simulation(fiber_input, target_count, yarn_twist, machinery)
                
                # Display Dashboard
                st.markdown("---")
                c1, c2 = st.columns(2)
                with c1: st.markdown(f'<div class="tech-card analysis"><span class="card-title">🔬 Fiber Physics</span>{r1}</div>', unsafe_allow_html=True)
                with c2: st.markdown(f'<div class="tech-card gauges"><span class="card-title">🔧 Gauge Settings</span>{r2}</div>', unsafe_allow_html=True)
                
                c3, c4 = st.columns(2)
                with c3: st.markdown(f'<div class="tech-card yield"><span class="card-title">📊 Production Balance</span>{r3}</div>', unsafe_allow_html=True)
                with c4: st.markdown(f'<div class="tech-card comm"><span class="card-title">📈 Market Strategy</span>{r4}</div>', unsafe_allow_html=True)

                # Export
                ts = datetime.datetime.now().strftime("%Y-%m-%d")
                report = f"RAZA ENTERPRISES - SPINNING REPORT\nDATE: {ts}\n\n=== FIBER ===\n{r1}\n\n=== SETTINGS ===\n{r2}\n\n=== YIELD ===\n{r3}\n\n=== STRATEGY ===\n{r4}"
                st.download_button("💾 DOWNLOAD OFFICIAL REPORT", report, file_name=f"Raza_Report_{ts}.txt")

            except Exception as e:
                st.error(f"SYSTEM FAILURE: {e}")
