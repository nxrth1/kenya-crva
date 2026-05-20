# Kenya Climate Risk & Vulnerability Assessment (CRVA)

> **An interactive web dashboard mapping climate risk across all 47 counties of Kenya**
> Commissioned by UNEP Kenya Country Office · WiSK Mentorship Programme · 2026

---

## 🌍 Live Dashboard

**[View the interactive map →](https://yourusername.github.io/kenya-crva)**

> Replace `yourusername` with your actual GitHub username after publishing.

---

## 📌 Project Overview

This project produces a **Climate Risk and Vulnerability Assessment (CRVA)** for Kenya, generating evidence-based climate vulnerability maps and a county-level risk index to guide adaptation interventions and national policy.

The assessment follows the **IPCC AR6 vulnerability framework**:

```
Risk = f(Hazard, Exposure, Vulnerability)
Vulnerability = f(Sensitivity, Adaptive Capacity)
```

All 47 Kenyan counties are ranked by a composite CRVA score (0–1 scale) derived from multi-criteria spatial analysis in ArcGIS Pro using satellite data, census statistics, and climate datasets.

---

## 🗺️ Dashboard Features

| Feature | Description |
|---|---|
| **Interactive choropleth map** | All 47 counties coloured by CRVA risk class |
| **County details panel** | CRVA score, raw score, grid cell count, risk rank |
| **Ranked county list** | Searchable, sorted by CRVA score |
| **Top 10 chart** | Bar chart of highest-risk counties |
| **Risk distribution donut** | Breakdown of counties by risk class |
| **Layer controls** | Toggle CRVA layer, switch basemaps, adjust opacity |
| **Hover tooltips** | Instant county name and score on hover |
| **Click to fly** | Click any county to zoom in and view details |

---

## 🏆 Key Findings

### Risk Class Distribution

| Risk Class | Counties | Notable Counties |
|---|---|---|
| 🔴 Very High | 2 | Vihiga, Wajir |
| 🟠 High | 5 | Tana River, Nyamira, Nandi, Turkana, Mandera |
| 🟡 Moderate | 16 | Kakamega, Siaya, Marsabit, Kisii, Bungoma, Kilifi |
| 🟢 Low | 16 | Nakuru, Nairobi, Garissa, Samburu, Narok |
| 🌿 Very Low | 8 | Baringo, Elgeyo/Marakwet, Kajiado, Kirinyaga |

### Highest Risk Counties (Top 5)
1. **Vihiga** — CRVA: 1.000 *(note: small sample size — 23 grid cells)*
2. **Wajir** — CRVA: 0.827
3. **Tana River** — CRVA: 0.715
4. **Nyamira** — CRVA: 0.684
5. **Nandi** — CRVA: 0.654

---

## 🔬 Methodology

### Data Sources

| Dataset | Category | Source |
|---|---|---|
| CHIRPS Pentad Rainfall (2014–2023) | Hazard | UCSB via Google Earth Engine |
| MODIS Land Surface Temperature (2014–2023) | Hazard | NASA via Google Earth Engine |
| Drought Frequency Index (2014–2023) | Hazard | Derived from CHIRPS |
| Flood Plains 2020 | Hazard | Shared project data |
| Kenya Land Use 2017 | Sensitivity | Shared project data |
| MPI & Partial Indices (2022) | Sensitivity | OPHI / Shared project data |
| HDI per County | Adaptive Capacity | UNDP / HDX |
| 2019 Population Census | Exposure | KNBS |
| Major Roads | Adaptive Capacity | OpenStreetMap |
| Health Facilities 2022 | Adaptive Capacity | Shared project data |
| Education Facilities 2020 | Adaptive Capacity | Shared project data |
| Kenya County Boundaries | Base layer | HDX |

### CRVA Formula

```
CRVA = (0.40 × Hazard) + (0.30 × Vulnerability) + (0.30 × Exposure)

Vulnerability = (0.60 × Sensitivity) − (0.40 × Adaptive Capacity)
```

Weights were assigned using **equal weighting within each component**, following standard practice in multi-criteria vulnerability assessments where no single indicator has empirically demonstrated dominance. Top-level component weights were derived from the project Terms of Reference and IPCC AR6 framework.

### GIS Workflow

```
Phase 1 → Project setup & CRS (EPSG:32737 — WGS 1984 UTM Zone 37S)
Phase 2 → Data loading (shapefiles, GeoTIFFs, CSV tables)
Phase 3 → Data preparation (reproject, clip to Kenya, join census data)
Phase 4 → Raster conversion & normalisation (100m fishnet grid, 0–1 scale)
Phase 5 → CRVA calculation (Raster Calculator — Hazard × Exposure × Vulnerability)
Phase 6 → Map production (classification, layout, export)
```

All analysis was performed in **ArcGIS Pro** with supplementary data processing in **Google Earth Engine**.

---

## 📂 Repository Structure

```
kenya-crva/
├── index.html                        ← Interactive CRVA dashboard (main file)
├── README.md                         ← This file
├── data/
│   └── county_vulnerability_ranking.csv   ← Zonal statistics output from ArcGIS Pro
├── docs/
│   ├── methodology.md                ← Detailed methodology notes
│   └── data_sources.md               ← Full data source documentation
└── maps/
    └── kenya_crva_final.png          ← Static export of the CRVA map
```

---

## 🛠️ Technology Stack

| Tool | Purpose |
|---|---|
| ArcGIS Pro | GIS analysis, raster processing, CRVA calculation |
| Google Earth Engine | Climate data extraction (CHIRPS, MODIS) |
| Leaflet.js 1.9.4 | Interactive web mapping |
| HTML / CSS / JavaScript | Dashboard interface |
| GitHub Pages | Free web hosting |

---

## ⚠️ Important Notes & Limitations

1. **Relative assessment only** — CRVA scores are relative within Kenya. A score of 0.8 does not mean 80% risk in absolute terms; it means that county is more at risk than most other Kenyan counties.

2. **Vihiga small sample flag** — Vihiga county has only 23 grid cells in the analysis due to its small geographic area (575 km²). The Very High score should be interpreted alongside this context.

3. **Mombasa small sample** — Mombasa has only 8 grid cells. Score reflects high urban exposure but limited spatial coverage.

4. **Data vintage** — Some datasets used are from different years (land use 2017, census 2019, MPI 2022). This temporal mismatch is common in vulnerability assessments and is noted in the methodology.

5. **Equal weighting assumption** — Sub-indicator weights are equal within each component. A PCA-based weighting approach would produce more statistically derived weights and is recommended for future iterations.

---

## 📋 Project Details

| Item | Detail |
|---|---|
| **Commissioned by** | UNEP Kenya Country Office |
| **Programme** | WiSK Mentorship Programme |
| **Date** | May 2026 |
| **Geographic scope** | Kenya — all 47 counties |
| **Grid resolution** | 100m × 100m fishnet |
| **Coordinate system** | WGS 1984 UTM Zone 37S (EPSG:32737) |
| **Classification method** | Equal interval (0.2 breaks) on normalised 0–1 scale |

---

## 📄 License

This project was produced for UNEP Kenya under the WiSK Mentorship Programme. Data and outputs are intended for research, policy, and educational use.

---

## 🙏 Acknowledgements

- **UNEP Kenya Country Office** — project commissioning and oversight
- **WiSK Mentorship Programme** — technical guidance and supervision
- **KNBS** — 2019 Kenya Population and Housing Census data
- **UCSB Climate Hazards Group** — CHIRPS rainfall dataset
- **NASA** — MODIS Land Surface Temperature products
- **OPHI** — Kenya Multidimensional Poverty Index data
- **HDX / OCHA** — Kenya humanitarian data layers
- **OpenStreetMap contributors** — roads and infrastructure data
