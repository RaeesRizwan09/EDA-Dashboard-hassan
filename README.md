# 🌬️ WINDGRID — US Wind Turbine Dashboard

A dark aerospace-industrial Streamlit dashboard for exploring the **USGS Wind Turbine Database** —
deployment timelines, state fleet sizes, manufacturer profiles, turbine specs, and capacity analysis
across 58,000+ utility-scale turbines installed between 1981 and 2018.

---

## Folder Structure

```
wind_dashboard/
├── data/
│   └── us_wind_csv.xls     ← dataset goes here (it's actually a CSV)
├── .streamlit/
│   └── config.toml
├── app.py
├── charts.py
├── filters.py
├── requirements.txt
└── README.md
```

---

## Setup & Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Opens at `http://localhost:8501`

---

## Dashboard Sections

| Section | What's Inside |
|---------|--------------|
| **01 · Fleet Command** | State turbine count bar · Total installed capacity by state |
| **02 · Deployment Timeline** | Year-by-year installation histogram · Cumulative build-up line |
| **03 · Manufacturer Profiles** | Manufacturer market share bar · Avg capacity by maker scatter |
| **04 · Turbine Engineering** | Hub height histogram · Rotor diameter distribution · Capacity KDE |
| **05 · Capacity Landscape** | Capacity band breakdown · Hub height vs capacity scatter |
| **06 · Data Terminal** | State summary table · Raw turbine records · CSV export |

## Sidebar Filters
- **State** (multi-select)
- **Manufacturer** (multi-select)
- **Install Year Range** (slider)
- **Turbine Capacity Range kW** (slider)
- **Hub Height Range m** (slider)
- **Top N** for ranked charts

---

## Design

- **Theme**: Dark aerospace / industrial — midnight navy, electric cyan, amber signal, steel blue
- **Fonts**: Space Mono (monospace terminals) · Barlow Condensed (industrial headers) · Barlow (body)
- Completely different from coffee dashboard (warm parchment/espresso) and Big Mac (editorial black/gold)

---

*Data: USGS Wind Turbine Database · data.usgs.gov · Last updated 2018*
