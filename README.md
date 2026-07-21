# IMDb Cancelled Shows ETL Pipeline

An end-to-end pipeline that analyzes 8,000+ IMDb TV shows to answer a
specific question: **which genuinely good shows got cancelled too
soon?** — and visualizes the pattern in Power BI.

## The question this answers

Not "which shows ended" (most shows end eventually), but "which shows
were rated 7.0+ on IMDb and still got cut within 3 seasons or fewer."
That's the `is_cancelled` flag this pipeline builds — a proxy for
shows that were cancelled despite being good, not because they were
bad.

## Data

- **Source:** [IMDb non-commercial datasets](https://datasets.imdbws.com/)
  — `title.basics.tsv`, `title.ratings.tsv`, `title.episode.tsv`
  (not included in this repo due to size/license — download and
  place in `data/` to run the pipeline yourself).
- **Filters applied:** TV series only, 1,000+ votes, started in 2000
  or later, has a rating.
- **Scale:** 8,293 shows after filtering, 3,130 flagged as
  cancelled-too-soon.

## Pipeline architecture

```
IMDb .tsv files (data/)
      │
      ▼
 ingest.py           →  loads title basics, ratings, episodes
      │
      ▼
 transform.py        →  merges, filters, computes total_seasons/episodes,
                          flags is_cancelled
      │
      ├───────────────► load.py            → optional: PostgreSQL star schema
      │                                        (dim_genre + fact_shows)
      │
      └───────────────► export_powerbi.py  → writes powerbi/dim_genre.csv
                                                and powerbi/fact_shows.csv
                                                      │
                                                      ▼
                                              Power BI Desktop dashboard
```

## Tech stack

| Layer | Tool |
|---|---|
| Extract / Transform | Python, Pandas |
| Data warehouse (optional) | PostgreSQL |
| Visualization | **Power BI** |
| Orchestration | Plain Python (`pipeline.py`) |
| SQL analysis (optional) | `analyze.sql` |

## How to run

1. Download the three datasets from datasets.imdbws.com, unzip them,
   and place them in `data/`.
2. `pip install -r requirements.txt`
3. `python pipeline.py`

This produces:
- `powerbi/dim_genre.csv` — one row per genre (dimension table)
- `powerbi/fact_shows.csv` — one row per show (fact table)

Optional PostgreSQL path (for a live-connection Power BI demo):
```bash
python load.py
psql shows_db < analyze.sql
```

## Power BI dashboard

See **[POWERBI_GUIDE.md](POWERBI_GUIDE.md)** for exact steps.

Dashboard includes:
- Cancellation rate by genre (bar chart)
- Rating distribution: cancelled vs. survived (histogram)
- Cancellation trend by decade
- Average episode count: cancelled vs. survived
- Genre and decade slicers

## Project structure

```
├── data/                     # IMDb .tsv files (you provide these)
├── powerbi/
│   ├── dim_genre.csv          # generated
│   └── fact_shows.csv         # generated
├── ingest.py                    # extract
├── transform.py                   # transform + is_cancelled logic
├── load.py                          # optional PostgreSQL warehouse loader
├── export_powerbi.py                  # Power BI CSV export
├── pipeline.py                          # orchestrator
├── analyze.sql                            # optional SQL analysis
├── requirements.txt
├── POWERBI_GUIDE.md
├── INTERVIEW_QA.md
└── README.md
```

## Skills demonstrated

- ETL pipeline design (extract / transform / load, separated by concern)
- Feature engineering (deriving a binary label from multiple raw fields)
- Star-schema data modeling (fact + dimension tables)
- SQL analytics (optional PostgreSQL path)
- Power BI (data modeling, DAX, interactive dashboards)

## Future improvements

- Airflow orchestration for scheduled re-runs as IMDb updates its datasets
- Incremental loading instead of full reload each run
- An ML classifier predicting cancellation risk from early-season
  ratings, instead of the current rule-based flag
- Cloud deployment (e.g., the warehouse on RDS, Power BI Service for
  scheduled refresh)
