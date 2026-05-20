# Methodology Notes — Kenya CRVA 2026

## 1. Conceptual Framework

This assessment adopts the IPCC AR6 risk framework where:

**Risk = f(Hazard, Exposure, Vulnerability)**

Vulnerability itself is decomposed as:

**Vulnerability = Sensitivity − Adaptive Capacity**

This means a county is highly vulnerable if it is strongly sensitive to climate stress AND has limited capacity to cope or recover.

---

## 2. Indicator Selection

### Hazard Indicators
Represent the climate stressors present in the landscape.

| Indicator | Rationale | Data |
|---|---|---|
| Mean annual rainfall variability (CHIRPS) | Erratic rainfall is the primary agricultural climate risk in Kenya | CHIRPS Pentad 2014–2023 |
| Drought frequency index | Count of pentads with Z-score < −1 SD over 10 years | Derived from CHIRPS |
| Mean land surface temperature (MODIS) | Heat stress affects crops, livestock and human health | MODIS MOD11A2 2014–2023 |
| Flood plain coverage | Physical flood hazard zone | FloodPlains_2020 shapefile |

### Sensitivity Indicators
Represent how strongly systems respond to climate stress.

| Indicator | Rationale | Data |
|---|---|---|
| Agricultural land use | Rain-fed farming is directly exposed to rainfall variability | Kenya Land Use 2017 |
| MPI poverty score | Poor households have fewer resources to cope with climate impacts | OPHI Kenya MPI 2022 |
| Forest cover | Forest loss increases runoff, drought, and temperature extremes | GForestAreas_2022 |

### Adaptive Capacity Indicators
Represent the ability to cope, adjust, or recover. These are **inverted** — higher capacity = lower vulnerability.

| Indicator | Rationale | Data |
|---|---|---|
| HDI per county | Composite of education, income, life expectancy | UNDP / HDX |
| Road density | Access to markets, services, and emergency response | MajorRoads shapefile |
| Health facility density | Access to healthcare affects recovery from climate impacts | HealthFacilities_2022 |

### Exposure Indicators
Represent people, assets, and systems in harm's way.

| Indicator | Rationale | Data |
|---|---|---|
| Population density | More people in hazard zones = higher exposure | WorldPop / KNBS 2019 |
| Settlement coverage | Built environment in climate-risk zones | Settlement_2022 |
| AgroClimatic zone | Classifies agricultural risk zones | Kenya_AgroClimatic_Zones |

---

## 3. Normalisation

All indicators were normalised to a 0–1 scale using min-max normalisation:

```
X_norm = (X − X_min) / (X_max − X_min)
```

For **Adaptive Capacity** indicators (HDI, roads, health), the scale was inverted after normalisation:

```
X_inverted = 1 − X_norm
```

This ensures that higher adaptive capacity translates to lower vulnerability in the composite score.

---

## 4. Weighting

Equal weights were applied within each component:

**Hazard (40% of final CRVA):**
- CHIRPS rainfall: 25%
- Drought frequency: 25%
- MODIS LST: 25%
- Flood plains: 25%

**Vulnerability (30% of final CRVA):**
- Sensitivity: 60% of vulnerability score
  - Land use: 33.3%
  - MPI score: 33.3%
  - Forest cover: 33.3%
- Adaptive Capacity: 40% of vulnerability score
  - HDI: 33.3%
  - Road density: 33.3%
  - Health facilities: 33.3%

**Exposure (30% of final CRVA):**
- Population density: 33.3%
- Settlement coverage: 33.3%
- AgroClimatic zones: 33.3%

**Justification:** Equal weighting was chosen to avoid arbitrary subjective weighting of indicators. This approach is transparent and replicable. PCA-based weighting is recommended for future iterations.

---

## 5. Spatial Processing

- **Grid resolution:** 100m × 100m fishnet grid
- **Coordinate system:** WGS 1984 UTM Zone 37S (EPSG:32737)
- **Extent:** Full Kenya bounding box clipped to national boundary
- **Raster algebra:** ArcGIS Pro Raster Calculator
- **Zonal statistics:** Mean CRVA score extracted per county using Zonal Statistics as Table

---

## 6. Classification

The raw CRVA scores (ranging from 2.27 to 6.24 on the raster scale) were:

1. Normalised to 0–1 using min-max
2. Classified into 5 equal-interval classes (0.2 breaks):

| Class | Score range | Label |
|---|---|---|
| 1 | 0.00–0.20 | Very Low |
| 2 | 0.20–0.40 | Low |
| 3 | 0.40–0.60 | Moderate |
| 4 | 0.60–0.80 | High |
| 5 | 0.80–1.00 | Very High |

---

## 7. Limitations & Caveats

- The CRVA map is a **relative** assessment within Kenya only
- Results are sensitive to indicator selection and weighting assumptions
- Small counties (Vihiga: 23 cells, Mombasa: 8 cells) have limited spatial representation
- Data from different years were used due to availability constraints
- The assessment captures current conditions — future climate projections (CMIP6) were not incorporated in this iteration
