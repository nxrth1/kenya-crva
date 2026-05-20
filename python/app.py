"""
Kenya Climate Risk & Vulnerability Assessment (CRVA) — Python dashboard.

Run:  streamlit run app.py
"""

from __future__ import annotations

import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

from crva_data import (
    BASEMAPS,
    RISK_CLASSES,
    RISK_COLOR,
    RISK_TEXT,
    load_counties,
    load_geojson,
    rank_counties,
)

st.set_page_config(
    page_title="Kenya CRVA",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Styling (matches original palette) ─────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
h1, h2, h3 { font-family: 'DM Serif Display', serif !important; }
.block-container { padding-top: 1rem; max-width: 100%; }
div[data-testid="stSidebar"] {
  background: #ffffff;
  border-right: 1px solid #e0dbd0;
}
.crva-header {
  background: #1a1a18;
  color: #fff;
  padding: 12px 20px;
  margin: -1rem -1rem 1rem -1rem;
  border-bottom: 3px solid #c84b11;
}
.crva-header h1 { color: #fff !important; font-size: 1.1rem !important; margin: 0; }
.crva-badge {
  display: inline-block;
  font-size: 10px;
  letter-spacing: 0.8px;
  text-transform: uppercase;
  padding: 3px 8px;
  border: 1px solid rgba(255,255,255,0.2);
  color: #ccc;
  margin-left: 8px;
  border-radius: 2px;
}
.crva-badge.live { border-color: #78c679; color: #78c679; }
.score-big { font-family: 'DM Mono', monospace; font-size: 2.5rem; font-weight: 500; line-height: 1; }
.metric-box {
  background: #f5f2ec;
  border: 1px solid #e0dbd0;
  border-radius: 6px;
  padding: 9px 11px;
}
.metric-label {
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.8px;
  text-transform: uppercase;
  color: #6b6860;
}
.metric-val { font-family: 'DM Mono', monospace; font-size: 15px; font-weight: 500; }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="crva-header">
  <span style="font-family:DM Mono,monospace;background:#c84b11;padding:6px 8px;border-radius:4px;font-size:10px;">CRVA</span>
  <span style="font-family:DM Serif Display,serif;font-size:17px;margin-left:12px;">
    Kenya Climate Risk &amp; Vulnerability Assessment
  </span>
  <span style="font-size:11px;color:#999;margin-left:12px;">· WiSK Mentorship · 2026</span>
  <span class="crva-badge">47 Counties</span>
  <span class="crva-badge live">Real CRVA Data</span>
</div>
""",
    unsafe_allow_html=True,
)


@st.cache_data
def get_data():
    counties = load_counties()
    geojson = load_geojson()
    ranked = rank_counties(counties)
    return counties, geojson, ranked


counties_df, geojson, ranked_df = get_data()

if "selected_name" not in st.session_state:
    st.session_state.selected_name = None


def select_county(name: str) -> None:
    st.session_state.selected_name = name


def selected_row() -> pd.Series | None:
    name = st.session_state.selected_name
    if not name:
        return None
    row = counties_df[counties_df["name"] == name]
    return row.iloc[0] if not row.empty else None


def make_map(
    show_crva: bool,
    basemap_key: str,
    opacity: float,
    highlight: str | None,
) -> folium.Map:
    tiles = {
        "carto": (
            "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
            "© OpenStreetMap © CARTO",
        ),
        "osm": (
            "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
            "© OpenStreetMap contributors",
        ),
        "sat": (
            "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            "© Esri",
        ),
    }
    url, attr = tiles.get(basemap_key, tiles["carto"])
    m = folium.Map(location=[0.5, 37.9], zoom_start=6, tiles=None, control=True)
    folium.TileLayer(url, attr=attr, name="basemap").add_to(m)

    if show_crva:

        def style_fn(feature):
            risk = feature["properties"].get("risk", "Moderate")
            name = feature["properties"].get("name", "")
            weight = 2.5 if name == highlight else 1.5
            color = "#333333" if name == highlight else "#ffffff"
            return {
                "fillColor": RISK_COLOR.get(risk, "#cccccc"),
                "fillOpacity": opacity,
                "color": color,
                "weight": weight,
            }

        folium.GeoJson(
            geojson,
            style_function=style_fn,
            highlight_function=lambda f: {
                "fillOpacity": min(opacity + 0.2, 1.0),
                "weight": 2.5,
                "color": "#333333",
            },
            tooltip=folium.GeoJsonTooltip(
                fields=["name", "crva", "risk"],
                aliases=["County", "CRVA", "Risk"],
                localize=True,
                labels=True,
                style=(
                    "font-family: DM Sans, sans-serif; font-size: 12px;"
                    "background: rgba(255,255,255,0.95); border: 1px solid #e0dbd0;"
                ),
            ),
        ).add_to(m)

    folium.LayerControl().add_to(m)
    return m


def render_county_details(row: pd.Series) -> None:
    col = RISK_COLOR[row["risk"]]
    tcol = RISK_TEXT[row["risk"]]
    rank = int(ranked_df[ranked_df["name"] == row["name"]]["rank"].iloc[0])

    st.markdown(f"### {row['name']}")
    st.caption(f"Rank #{rank} of 47 counties")
    st.markdown(
        f'<p class="score-big" style="color:{col}">{row["crva"]:.4f}</p>',
        unsafe_allow_html=True,
    )
    st.caption("Normalised CRVA score (0–1)")
    st.progress(float(row["crva"]))
    st.markdown(
        f'<span style="background:{col};color:{tcol};padding:4px 10px;'
        f'border-radius:2px;font-size:11px;font-weight:600;letter-spacing:0.5px;'
        f'text-transform:uppercase;">{row["risk"]} Risk</span>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            f'<div class="metric-box"><div class="metric-label">Raw Score</div>'
            f'<div class="metric-val">{row["raw"]:.4f}</div></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="metric-box"><div class="metric-label">Area (km²)</div>'
            f'<div class="metric-val">{int(row["area"]):,}</div></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div class="metric-box"><div class="metric-label">Grid Cells</div>'
            f'<div class="metric-val" style="color:#059669">{int(row["count"]):,}</div></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="metric-box"><div class="metric-label">Risk Class</div>'
            f'<div class="metric-val" style="color:{col}">{row["risk"]}</div></div>',
            unsafe_allow_html=True,
        )

    if row["count"] < 50:
        st.warning(
            f"Small sample size ({int(row['count'])} cells) — interpret with caution."
        )


# ── Layout: sidebar panels + map ─────────────────────────────────────────
sidebar = st.sidebar
tab_counties, tab_details, tab_charts, tab_layers = sidebar.tabs(
    ["Counties", "Details", "Charts", "Layers"]
)

with tab_layers:
    show_crva = st.checkbox("CRVA composite risk", value=True)
    basemap_label = st.radio(
        "Basemap",
        list(BASEMAPS.keys()),
        index=0,
    )
    opacity_pct = st.slider("Opacity", 0, 100, 75)
    st.caption(f"Opacity: {opacity_pct}%")

with tab_counties:
    search = st.text_input("Search county", placeholder="Search county…")
    filtered = ranked_df
    if search.strip():
        q = search.strip().lower()
        filtered = ranked_df[ranked_df["name"].str.lower().str.contains(q)]

    for _, row in filtered.iterrows():
        risk = row["risk"]
        dot = RISK_COLOR[risk]
        label = f"{row['name']} — {row['crva']:.3f}"
        if st.button(
            label,
            key=f"btn_{row['name']}",
            use_container_width=True,
            type="primary" if row["name"] == st.session_state.selected_name else "secondary",
        ):
            select_county(row["name"])

with tab_details:
    row = selected_row()
    if row is None:
        st.info(
            "Click any county on the map or select from the Counties list "
            "to see detailed vulnerability data."
        )
    else:
        render_county_details(row)

with tab_charts:
    st.markdown("**Top 10 highest CRVA score**")
    top10 = ranked_df.head(10)
    max_v = top10["crva"].max()
    for _, row in top10.iterrows():
        pct = (row["crva"] / max_v) if max_v else 0
        st.markdown(f"**{row['name']}** — {row['crva']:.2f}")
        st.progress(pct)

    st.divider()
    st.markdown("**Risk class distribution**")
    dist = counties_df["risk"].value_counts().reindex(RISK_CLASSES, fill_value=0)
    chart_df = pd.DataFrame({"risk": dist.index, "count": dist.values})
    st.bar_chart(chart_df.set_index("risk"), color="#c84b11")
    for risk in RISK_CLASSES:
        n = int(dist.get(risk, 0))
        st.markdown(
            f'<span style="display:inline-block;width:10px;height:10px;'
            f'background:{RISK_COLOR[risk]};border-radius:50%;margin-right:6px;"></span>'
            f"{risk}: **{n}**",
            unsafe_allow_html=True,
        )

# ── Main map column ────────────────────────────────────────────────────────
map_col, legend_col = st.columns([5, 1])
with legend_col:
    st.markdown("**CRVA Risk Level**")
    for risk in RISK_CLASSES:
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:5px;">'
            f'<div style="width:20px;height:12px;background:{RISK_COLOR[risk]};border-radius:2px;"></div>'
            f'<span style="font-size:11px;">{risk}</span></div>',
            unsafe_allow_html=True,
        )
    st.caption("Click any county to view full vulnerability details")

with map_col:
    basemap_key = BASEMAPS[basemap_label]
    opacity = opacity_pct / 100.0
    highlight = st.session_state.selected_name
    fmap = make_map(show_crva, basemap_key, opacity, highlight)

    if highlight:
        sel = counties_df[counties_df["name"] == highlight].iloc[0]
        fmap.location = [sel["lat"], sel["lng"]]
        fmap.zoom_start = 9

    map_state = st_folium(
        fmap,
        width=None,
        height=520,
        returned_objects=["last_object_clicked", "last_active_drawing"],
        key="crva_map",
    )

    clicked = map_state.get("last_object_clicked") if map_state else None
    if clicked and isinstance(clicked, dict):
        props = clicked.get("properties") or {}
        name = props.get("name")
        if name:
            select_county(name)
            st.rerun()
