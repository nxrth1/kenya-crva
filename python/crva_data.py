"""Data loading and shared constants for the Kenya CRVA dashboard."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

RISK_COLOR = {
    "Very High": "#c00000",
    "High": "#f07d32",
    "Moderate": "#c2e699",
    "Low": "#78c679",
    "Very Low": "#1a9641",
}

RISK_TEXT = {
    "Very High": "#ffffff",
    "High": "#ffffff",
    "Moderate": "#2d5a0e",
    "Low": "#1a3a0a",
    "Very Low": "#ffffff",
}

RISK_CLASSES = ["Very High", "High", "Moderate", "Low", "Very Low"]

BASEMAPS = {
    "Light (CartoDB)": "carto",
    "OpenStreetMap": "osm",
    "Satellite (ESRI)": "sat",
}


def load_counties() -> pd.DataFrame:
    """Load pre-computed county CRVA records (from ArcGIS zonal stats + normalisation)."""
    with open(DATA_DIR / "counties.json", encoding="utf-8") as f:
        rows = json.load(f)
    return pd.DataFrame(rows)


def load_geojson() -> dict:
    with open(DATA_DIR / "kenya_counties.geojson", encoding="utf-8") as f:
        return json.load(f)


def rank_counties(df: pd.DataFrame) -> pd.DataFrame:
    out = df.sort_values("crva", ascending=False).reset_index(drop=True)
    out["rank"] = range(1, len(out) + 1)
    return out


def county_by_name(df: pd.DataFrame, name: str) -> pd.Series | None:
    match = df[df["name"] == name]
    if match.empty:
        return None
    return match.iloc[0]
