import streamlit as st
import requests
from datetime import datetime
import google.generativeai as genai

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="KAIROS — Weather",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------------------------------------------------------
# WEATHER DATA RETRIEVAL (Open-Meteo API)
# -----------------------------------------------------------------------------
LATITUDE = -1.2667
LONGITUDE = 36.8000
LOCATION_NAME = "Westlands, Nairobi"

WMO_CODE_MAP = {
    0: ("Clear Sky", "☀️"),
    1: ("Mainly Clear", "🌤️"),
    2: ("Partly Cloudy", "⛅"),
    3: ("Overcast", "☁️"),
    45: ("Foggy", "🌫️"),
    48: ("Depositing Rime Fog", "🌫️"),
    51: ("Light Drizzle", "🌦️"),
    53: ("Moderate Drizzle", "🌧️"),
    55: ("Dense Drizzle", "🌧️"),
    61: ("Slight Rain", "🌦️"),
    63: ("Moderate Rain", "🌧️"),
    65: ("Heavy Rain", "🌧️"),
    71: ("Slight Snow", "🌨️"),
    73: ("Moderate Snow", "🌨️"),
    75: ("Heavy Snow", "❄️"),
    80: ("Brief Showers", "🌦️"),
    81: ("Moderate Showers", "🌧️"),
    82: ("Violent Showers", "⛈️"),
    95: ("Thunderstorm", "⛈️"),
    96: ("Thunderstorm w/ Hail", "⛈️"),
    99: ("Severe Thunderstorm", "⛈️"),
}


@st.cache_data(ttl=600)
def fetch_weather_data():
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={LATITUDE}&longitude={LONGITUDE}"
        f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m"
        f"&hourly=temperature_2m,precipitation_probability,weather_code"
        f"&timezone=Africa%2FNairobi&forecast_days=2"
    )
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception:
        return None


data = fetch_weather_data()

# -----------------------------------------------------------------------------
# CUSTOM CLAUDE-STYLE STYLING (MERRIWEATHER & MONTSERRAT)
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,300;0,400;0,700;1,300&family=Montserrat:wght@300;400;500;600;700&display=swap');

    /* Global Reset & Claude Warm Beige Tone with Montserrat */
    [data-testid="stAppViewContainer"] {
        background-color: #FAF7F2;
        color: #22201D;
        font-family: 'Montserrat', sans-serif;
    }
    
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }
    
    #MainMenu, footer {
        visibility: hidden;
    }

    .main .block-container {
        padding-top: 2.2rem;
        padding-bottom: 3.5rem;
        max-width: 980px;
    }

    /* Header Container */
    .brand-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 24px;
        margin-bottom: 24px;
        border-bottom: 1px solid #ECE6DB;
    }

    .brand-title-wrap {
        display: flex;
        align-items: center;
        gap: 16px;
    }

    /* Merriweather Font for Brand Title */
    .brand-title {
        font-family: 'Merriweather', serif;
        font-size: 26px;
        font-weight: 700;
        letter-spacing: 0.12em;
        color: #1A1918;
        margin: 0;
    }

    .location-tag {
        font-family: 'Montserrat', sans-serif;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.04em;
        color: #79746D;
        text-transform: uppercase;
    }

    /* Hero Weather Card */
    .hero-card {
        background: #FFFFFF;
        border: 1px solid #EAE4D9;
        border-radius: 20px;
        padding: 36px 40px;
        margin-bottom: 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
    }

    .hero-temp-block {
        display: flex;
        flex-direction: column;
    }

    /* Merriweather Font for Main Temperature */
    .hero-temp {
        font-family: 'Merriweather', serif;
        font-size: 72px;
        font-weight: 300;
        line-height: 1;
        color: #191817;
        letter-spacing: -0.04em;
    }

    .hero-desc {
        font-family: 'Montserrat', sans-serif;
        font-size: 19px;
        font-weight: 500;
        color: #55524E;
        margin-top: 10px;
    }

    .hero-meta {
        font-family: 'Montserrat', sans-serif;
        font-size: 14px;
        color: #8C867E;
        margin-top: 4px;
    }

    .hero-icon {
        font-size: 64px;
        user-select: none;
    }

    /* Metric Grid Cards */
    .metrics-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 18px;
        margin-bottom: 30px;
    }

    .metric-card {
        background: #FFFFFF;
        border: 1px solid #EAE4D9;
        border-radius: 16px;
        padding: 22px 24px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.015);
    }

    .metric-label {
        font-family: 'Montserrat', sans-serif;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #8E877E;
        margin-bottom: 8px;
    }

    /* Merriweather Font for Metric Values */
    .metric-value {
        font-family: 'Merriweather', serif;
        font-size: 26px;
        font-weight: 700;
        color: #1F1E1D;
        letter-spacing: -0.02em;
    }

    .metric-sub {
        font-family: 'Montserrat', sans-serif;
        font-size: 13px;
        color: #8C867E;
        margin-top: 4px;
    }

    /* Section Subhead */
    .section-label {
        font-family: 'Montserrat', sans-serif;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #79746D;
        margin-bottom: 14px;
    }

    /* Hourly Forecast Scroller */
    .forecast-container {
        display: flex;
        gap: 14px;
        overflow-x: auto;
        padding-bottom: 12px;
        scrollbar-width: thin;
        scrollbar-color: #DDD6C9 transparent;
    }

    .forecast-pill {
        background: #FFFFFF;
        border: 1px solid #EAE4D9;
        border-radius: 14px;
        min-width: 104px;
        padding: 16px 14px;
        text-align: center;
        flex-shrink: 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.01);
    }

    .pill-time {
        font-family: 'Montserrat', sans-serif;
        font-size: 13px;
        font-weight: 500;
        color: #79746D;
        margin-bottom: 8px;
    }

    .pill-icon {
        font-size: 22px;
        margin-bottom: 6px;
    }

    .pill-temp {
        font-family: 'Merriweather', serif;
        font-size: 18px;
        font-weight: 700;
        color: #1E1D1C;
    }

    .pill-rain {
        font-family: 'Montserrat', sans-serif;
        font-size: 12px;
        font-weight: 500;
        color: #64748B;
        margin-top: 4px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# HAND-DRAWN SKETCH SVG LOGO
# -----------------------------------------------------------------------------
SKETCH_LOGO_SVG = """
<svg width="48" height="48" viewBox="0 0 72 72" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- Hand-drawn style cloud -->
  <path d="M 22 36 
           C 16 36, 12 30, 14 24 
           C 16 18, 24 17, 27 20 
           C 30 13, 44 12, 48 18 
           C 54 14, 62 20, 60 27 
           C 65 31, 62 38, 55 38 
           L 22 38" 
        stroke="#1E1D1A" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round" />
  
  <!-- Sketchy rain lines -->
  <line x1="24" y1="42" x2="21" y2="47" stroke="#1E1D1A" stroke-width="1.8" stroke-linecap="round" />
  <line x1="33" y1="43" x2="30" y2="49" stroke="#1E1D1A" stroke-width="1.8" stroke-linecap="round" />
  <line x1="43" y1="42" x2="40" y2="48" stroke="#1E1D1A" stroke-width="1.8" stroke-linecap="round" />
  <line x1="52" y1="43" x2="49" y2="49" stroke="#1E1D1A" stroke-width="1.8" stroke-linecap="round" />

  <!-- Ground Line -->
  <path d="M 12 62 Q 36 60, 60 62" stroke="#1E1D1A" stroke-width="1.6" stroke-linecap="round" />

  <!-- Small Minimal Trees -->
  <line x1="22" y1="56" x2="22" y2="61" stroke="#1E1D1A" stroke-width="1.6" stroke-linecap="round" />
  <path d="M 22 49 L 17 56 L 27 56 Z" stroke="#1E1D1A" stroke-width="1.5" stroke-linejoin="round" fill="none" />

  <line x1="34" y1="57" x2="34" y2="61" stroke="#1E1D1A" stroke-width="1.4" stroke-linecap="round" />
  <path d="M 34 52 L 30 57 L 38 57 Z" stroke="#1E1D1A" stroke-width="1.4" stroke-linejoin="round" fill="none" />

  <line x1="48" y1="55" x2="48" y2="61" stroke="#1E1D1A" stroke-width="1.6" stroke-linecap="round" />
  <path d="M 48 48 L 43 55 L 53 55 Z" stroke="#1E1D1A" stroke-width="1.5" stroke-linejoin="round" fill="none" />
</svg>
"""

# -----------------------------------------------------------------------------
# APPLICATION HEADER
# -----------------------------------------------------------------------------
header_html = f"""
<div class="brand-header">
    <div class="brand-title-wrap">
        {SKETCH_LOGO_SVG}
        <div>
            <h1 class="brand-title">KAIROS</h1>
            <div class="location-tag">{LOCATION_NAME}</div>
        </div>
    </div>
    <div class="location-tag" style="font-size: 12px; color: #9A958E;">
        {datetime.now().strftime("%A, %b %d")}
    </div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# CONTENT RENDERING
# -----------------------------------------------------------------------------
if not data:
    st.error("Unable to load weather data at this moment. Please refresh shortly.")
else:
    current = data.get("current", {})
    hourly = data.get("hourly", {})

    temp = round(current.get("temperature_2m", 0))
    apparent_temp = round(current.get("apparent_temperature", 0))
    humidity = current.get("relative_humidity_2m", 0)
    wind_speed = current.get("wind_speed_10m", 0)
    weather_code = current.get("weather_code", 0)

    weather_desc, weather_icon = WMO_CODE_MAP.get(
        weather_code, ("Clear", "☀️")
    )

    # Calculate current rain chance from current hour's hourly forecast
    hourly_times = hourly.get("time", [])
    hourly_precip = hourly.get("precipitation_probability", [])
    hourly_temps = hourly.get("temperature_2m", [])
    hourly_codes = hourly.get("weather_code", [])

    current_iso_hour = datetime.now().strftime("%Y-%m-%dT%H:00")
    rain_chance = 0
    start_idx = 0

    if current_iso_hour in hourly_times:
        start_idx = hourly_times.index(current_iso_hour)
        rain_chance = hourly_precip[start_idx] if start_idx < len(hourly_precip) else 0
    elif len(hourly_precip) > 0:
        rain_chance = hourly_precip[0]

    # --- Hero Temperature Display ---
    hero_card_html = f"""
    <div class="hero-card">
        <div class="hero-temp-block">
            <div class="hero-temp">{temp}°C</div>
            <div class="hero-desc">{weather_desc}</div>
            <div class="hero-meta">Feels like {apparent_temp}°C in {LOCATION_NAME}</div>
        </div>
        <div class="hero-icon">{weather_icon}</div>
    </div>
    """
    st.markdown(hero_card_html, unsafe_allow_html=True)

    # --- 3-Metric Cards Grid ---
    metrics_html = f"""
    <div class="metrics-container">
        <div class="metric-card">
            <div class="metric-label">Humidity</div>
            <div class="metric-value">{humidity}%</div>
            <div class="metric-sub">Relative moisture</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Wind Speed</div>
            <div class="metric-value">{wind_speed} <span style="font-size: 16px; font-weight: 400; color: #6F6A63; font-family: 'Montserrat';">km/h</span></div>
            <div class="metric-sub">Surface level (10m)</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Rain Chance</div>
            <div class="metric-value">{rain_chance}%</div>
            <div class="metric-sub">Precipitation probability</div>
        </div>
    </div>
    """
    st.markdown(metrics_html, unsafe_allow_html=True)

    # --- Horizontal Hourly Forecast Timeline ---
    st.markdown('<div class="section-label">Hourly Timeline</div>', unsafe_allow_html=True)

    forecast_pills_html = '<div class="forecast-container">'
    end_idx = min(start_idx + 8, len(hourly_times))

    for i in range(
