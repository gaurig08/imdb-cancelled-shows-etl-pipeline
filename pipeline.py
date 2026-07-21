"""
pipeline.py
-----------
Extract (ingest.py) -> Transform (transform.py) -> Export for Power BI
(export_powerbi.py)

The PostgreSQL warehouse (load.py) is optional - run `python load.py`
separately if you want the "live database connection" version of the
Power BI demo.
"""

from transform import transform
from export_powerbi import export

print("=" * 50)
print("CANCELLED SHOWS ANALYTICS PIPELINE")
print("=" * 50)

print("\n[1/2] Extracting + transforming IMDb datasets...")
df = transform()

print("\n[2/2] Exporting star-schema CSVs for Power BI...")
export()

print("\n" + "=" * 50)
print("PIPELINE COMPLETE")
print(f" Total shows processed : {len(df)}")
print(f" Cancelled (good shows) : {df['is_cancelled'].sum()}")
print(f" Survived               : {(df['is_cancelled'] == 0).sum()}")
print(" Output: powerbi/dim_genre.csv + powerbi/fact_shows.csv")
print(" Next step: open Power BI Desktop and follow POWERBI_GUIDE.md")
print("=" * 50)
