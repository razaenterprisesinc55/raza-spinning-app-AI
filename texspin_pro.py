import streamlit as st
import google.generativeai as genai
import os
import datetime
import time

# ==============================================================================
# 1. PROFESSIONAL UI CONFIGURATION
# ==============================================================================
st.set_page_config(page_title="Raza Enterprises Inc | Spinning OS", page_icon="🏭", layout="wide")

# Custom CSS for "Raza Enterprises" Branding and Industrial Look
st.markdown("""
<style>
    /* Main Background and Font */
    .stApp { background-color: #0b0f19; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* Branding Header */
    .brand-header {
        background: linear-gradient(90deg, #001f3f 0%, #0074D9 100%);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
        border: 1px solid #0074D9;
        box-shadow: 0 0 15px rgba(0, 116, 217, 0.5);
    }
    .brand-text {
        font-size: 2.5rem;
        font-weight: 800;
        color: #fff;
        text-transform: uppercase;
        letter-spacing: 3px;
        text-shadow: 0 0 10px #00aaff;
    }
    .sub-brand { color: #7FDBFF; font-size: 1rem; letter-spacing: 1px; }

    /* Report Cards */
    .tech-card {
        background-color: #161b22;
        padding: 20px;
        border-radius: 8px;
        border-left: 4px solid;
        margin-bottom: 15px;
        color: #c9d1d9;
    }
    .card-title { font-size: 1.2rem; font-weight: bold; margin-bottom: 10px; display: block; color: white; }
    
    /* Specific Colors */
    .analysis { border-color: #d2a8ff; } /* Purple */
    .gauges { border-color: #ff7b72; }   /* Red */
    .yield { border-color: #79c0ff; }    /* Blue */
    .comm { border-color: #7ee787; }     /* Green */
    
    /* Input Fields */
    .stNumberInput input { color: #79c0ff; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. SIDEBAR & BRANDING
# ==============================================================================
with st.sidebar:
    st.markdown("<h2 style='color: #79c0ff; text-align: center;'>SYSTEM CONTROL</h2>", unsafe_allow_html=True)
    
    api_key = st.text_input("🔑 System Access Key (Google API)", type="password")
    
    # Auto-Detect Models Logic (Kept from previous success)
    valid_models = []
    if api_key:
        try:
            genai.configure(api_key=api_key)
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    valid_models.append(m.name.replace("models/", ""))
        except:
            pass
    if not valid_models: valid_models = ["gemini-1.5-flash", "gemini-pro"]
    
    model_name = st.selectbox("🤖 AI Core Engine", valid_models)
    
    st.divider()
    st.info("System Status: ONLINE")
    st.caption("© 2025 Raza Enterprises Inc.")

# ==============================================================================
# 3. HEADER
# ==============================================================================
st.markdown("""
<div class="brand-header">
    <div class="brand-text">RAZA ENTERPRISES INC</div>
    <div class="sub-brand">ADVANCED TEXTILE MANUFACTURING SIMULATION</div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 4. DATA INPUT TABS
# ==============================================================================
tab1, tab2 = st.tabs(["🧶 RAW MATERIAL", "⚙️ MACHINERY SETUP"])

with tab1:
    col1, col2 = st.columns([2, 1])
    with col1:
        fiber_input = st.text_area("Fiber Specifications", height=150, 
            placeholder="e.g. 100% Cotton Giza 86, Staple 33mm, Mic 4.0 OR 65/35 Poly-Cotton Blend...")
    with col2:
        st.write("### Target Parameters")
        target_count = st.number_input("Target Count (Ne)", value=30, step=1)
        yarn_twist = st.number_input("Target TM", value=4.0, step=0.1)

with tab2:
    st.write("### 🏭 Plant Capacity & Efficiency Configuration")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**1. Preparation**")
        blow_cap = st.number_input("Blowroom Line Capacity (kg/hr)", value=600)
        card_eff = st.slider("Carding Efficiency %", 85, 98, 92)
    with c2:
        st.markdown("**2. Spinning**")
        spindles = st.number_input("Total Ring Spindles", value=25000, step=1000)
        ring_speed = st.number_input("Avg Spindle Speed (RPM)", value=18000, step=500)
    with c3:
        st.markdown("**3. Winding**")
        drums = st.number_input("Auto-Coner Drums", value=600)
        wind_eff = st.slider("Winding Efficiency %", 70, 95, 85)

# ==============================================================================
# 5. AGENT LOGIC
# ==============================================================================
def run_raza_simulation(fiber, count, tm, spindles, speed, card_e, wind_e):
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)

    # --- AGENT 1: FIBER ANALYST ---
    st.toast("🔬 Analyzing Material Physics...")
    prompt_1 = f"""
    ROLE: Senior Fiber Technologist at Raza Enterprises.
    INPUT: "{fiber}" for Ne {count}.
    TASK: Analyze fiber physics.
    OUTPUT:
    1. Nature of Fiber & Classification.
    2. Spin-ability assessment for Count Ne {count}.
    3. Required mix/blend strategy (if applicable).
    4. Preparation risks (Neps, Static, Fusion).
    """
    res_1 = model.generate_content(prompt_1).text

    # --- AGENT 2: GAUGE & SETTING MASTER ---
    st.toast("🔧 Configuring Machine Gauges...")
    prompt_2 = f"""
    ROLE: Chief Technical Engineer.
    TASK: Provide PRECISE GAUGE SETTINGS (in thousands of an inch or mm) for processing "{fiber}".
    
    YOU MUST PROVIDE SETTINGS FOR:
    1. **Blowroom:** Beater speeds/settings.
    2. **Carding:** Cylinder-Doffer setting, Flat-Cylinder setting.
    3. **Drawframe:** Roller gauge settings (Front-Back).
    4. **Simplex/Roving:** Spacer size.
    5. **Ring Frame:** Spacer size, Break Draft zone setting, Ring rail speed.
    """
    res_2 = model.generate_content(prompt_2).text

    # --- AGENT 3: YIELD & PRODUCTION PLANNER ---
    st.toast("📊 Calculating Plant Yield...")
    prompt_3 = f"""
    ROLE: Production Planning Manager.
    TASK: Calculate production yield and balance based on these inputs:
    
    - Target Count: Ne {count}
    - Spindles: {spindles}
    - Speed: {speed} RPM
    - TM: {tm}
    
    CALCULATIONS REQUIRED:
    1. Calculate Twist Per Inch (TPI) = TM * sqrt(Count).
    2. Calculate Grams per Spindle per Shift (8 hours). Formula approx: (Speed * Efficiency 0.95 * 60 * 8) / (TPI * 36 * 840 * Count). *Adjust logic as an expert*.
    3. Total Daily Production (in Tons) for {spindles} spindles.
    4. Does the Blowroom capacity ({blow_cap} kg/hr) match this requirement?
    """
    res_3 = model.generate_content(prompt_3).text

    # --- AGENT 4: COMMERCIAL STRATEGIST ---
    st.toast("📈 Finalizing Commercial Report...")
    prompt_4 = f"""
    ROLE: Commercial Director.
    TASK: Summary for the Board of Directors.
    Based on the technical data, define:
    1. Market Application (e.g. High-end Shirting vs Low-end Weft).
    2. Expected Quality Level (Uster Percentiles).
    3. Sales Pitch for this yarn.
    """
    res_4 = model.generate_content(prompt_4).text

    return res_1, res_2, res_3, res_4

# ==============================================================================
# 6. EXECUTION & REPORTING
# ==============================================================================
if st.button("🚀 INITIATE RAZA PROTOCOL", type="primary"):
    if not api_key:
        st.error("⚠️ SYSTEM LOCKED: API KEY REQUIRED")
    elif not fiber_input:
        st.warning("⚠️ DATA MISSING: ENTER FIBER SPECS")
    else:
        with st.spinner("🔄 ORCHESTRATING AGENTS..."):
            try:
                # Run Logic
                r1, r2, r3, r4 = run_raza_simulation(fiber_input, target_count, yarn_twist, spindles, ring_speed, card_eff, wind_eff)
                
                # --- DISPLAY DASHBOARD ---
                st.markdown("---")
                
                # Report Section 1 & 2
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f'<div class="tech-card analysis"><span class="card-title">🔬 Fiber Physics Report</span>{r1}</div>', unsafe_allow_html=True)
                with c2:
                    st.markdown(f'<div class="tech-card gauges"><span class="card-title">🔧 Precision Gauge Settings</span>{r2}</div>', unsafe_allow_html=True)

                # Report Section 3 & 4
                c3, c4 = st.columns(2)
                with c3:
                    st.markdown(f'<div class="tech-card yield"><span class="card-title">📊 Yield & Capacity Analysis</span>{r3}</div>', unsafe_allow_html=True)
                with c4:
                    st.markdown(f'<div class="tech-card comm"><span class="card-title">📈 Commercial Strategy</span>{r4}</div>', unsafe_allow_html=True)

                # --- EXPORT FEATURE ---
                # We compile a text report
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                report_text = f"""
====================================================================
                  RAZA ENTERPRISES INC.
             OFFICIAL SPINNING SIMULATION REPORT
====================================================================
Date: {timestamp}
Fiber: {fiber_input}
Target: Ne {target_count} | TM {yarn_twist}
Machinery: {spindles} Spindles @ {ring_speed} RPM

--------------------------------------------------------------------
1. FIBER ANALYSIS
--------------------------------------------------------------------
{r1}

--------------------------------------------------------------------
2. MACHINE GAUGE SETTINGS (Technical)
--------------------------------------------------------------------
{r2}

--------------------------------------------------------------------
3. PRODUCTION YIELD CALCULATION
--------------------------------------------------------------------
{r3}

--------------------------------------------------------------------
4. COMMERCIAL STRATEGY
--------------------------------------------------------------------
{r4}

====================================================================
GENERATED BY RAZA ENTERPRISES AI OS
====================================================================
                """
                
                st.download_button(
                    label="💾 DOWNLOAD FULL REPORT (TXT)",
                    data=report_text,
                    file_name=f"Raza_Spinning_Report_{target_count}Ne.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"SYSTEM FAILURE: {e}")
