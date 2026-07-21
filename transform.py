"""
transform.py
------------
Builds the feature this whole project is centered on: is_cancelled -
a flag for shows that were, by the numbers, GOOD (average rating >=
7.0) but still ended within 3 seasons or fewer. That's the
"cancelled too soon" definition, distinct from shows that simply
ran their natural course or ended because they were unpopular.
"""

import pandas as pd
from ingest import load_basics, load_ratings, load_episodes


def transform():
    basics = load_basics()
    ratings = load_ratings()
    episodes = load_episodes()

    print("\nMerging series with ratings...")
    df = basics.merge(ratings, on="tconst", how="inner")

    # Only keep series with meaningful data
    df = df[
        (df["numVotes"] >= 1000) &      # at least 1000 votes - filters noise
        (df["startYear"] >= 2000) &     # modern era only
        (df["averageRating"].notna())
    ].copy()
    print(f"Series after filtering: {len(df)}")

    print("Calculating seasons per show...")
    seasons = episodes.groupby("parentTconst")["seasonNumber"].nunique().reset_index()
    seasons.columns = ["tconst", "total_seasons"]

    ep_count = episodes.groupby("parentTconst")["episodeNumber"].count().reset_index()
    ep_count.columns = ["tconst", "total_episodes"]

    df = df.merge(seasons, on="tconst", how="left")
    df = df.merge(ep_count, on="tconst", how="left")

    # Flag cancelled shows: has an end year, ran <=3 seasons, and was
    # rated 7.0+ (i.e. "good but still cancelled")
    df["is_cancelled"] = (
        (df["endYear"].notna()) &
        (df["total_seasons"] <= 3) &
        (df["averageRating"] >= 7.0)
    ).astype(int)

    # Keep only the first listed genre for simpler genre-level analysis
    df["primary_genre"] = df["genres"].str.split(",").str[0]

    df = df.dropna(subset=["total_seasons", "total_episodes", "primary_genre"])

    print("\nTransform complete")
    print(f"Total shows: {len(df)}")
    print(f"Cancelled (good rating, short run): {df['is_cancelled'].sum()}")
    print(f"Survived: {(df['is_cancelled'] == 0).sum()}")

    return df


if __name__ == "__main__":
    df = transform()
    print("\nSample data:")
    print(df[["primaryTitle", "averageRating", "total_seasons", "is_cancelled"]].head(10))
