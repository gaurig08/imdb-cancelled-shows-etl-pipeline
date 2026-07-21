"""
export_powerbi.py
------------------
Replaces dashboard.py as the presentation layer. Exports a clean
star-schema pair of CSVs for Power BI:

    powerbi/dim_genre.csv   -> one row per genre
    powerbi/fact_shows.csv  -> one row per show, keyed to dim_genre

Open both in Power BI Desktop (Get Data -> Text/CSV) and build the
relationship on genre_id. Full steps in POWERBI_GUIDE.md.
"""

import os
import pandas as pd
from transform import transform

OUT_DIR = "powerbi"


def export():
    os.makedirs(OUT_DIR, exist_ok=True)
    df = transform()

    dim_genre = (
        df[["primary_genre"]]
        .drop_duplicates()
        .rename(columns={"primary_genre": "genre_name"})
        .sort_values("genre_name")
        .reset_index(drop=True)
    )
    dim_genre.insert(0, "genre_id", dim_genre.index + 1)

    fact = df.merge(
        dim_genre, left_on="primary_genre", right_on="genre_name", how="left"
    )

    fact_cols = [
        "tconst", "genre_id", "primaryTitle", "startYear", "endYear",
        "averageRating", "numVotes", "total_seasons", "total_episodes",
        "runtimeMinutes", "is_cancelled"
    ]
    fact = fact[fact_cols].rename(columns={
        "primaryTitle": "title",
        "startYear": "start_year",
        "endYear": "end_year",
        "averageRating": "average_rating",
        "numVotes": "num_votes",
        "runtimeMinutes": "runtime_minutes",
    })

    dim_genre.to_csv(os.path.join(OUT_DIR, "dim_genre.csv"), index=False)
    fact.to_csv(os.path.join(OUT_DIR, "fact_shows.csv"), index=False)

    print(f"Exported {len(dim_genre)} genres to {OUT_DIR}/dim_genre.csv")
    print(f"Exported {len(fact)} shows to {OUT_DIR}/fact_shows.csv")
    print("\nOpen Power BI Desktop and load both CSVs - see POWERBI_GUIDE.md")


if __name__ == "__main__":
    export()
