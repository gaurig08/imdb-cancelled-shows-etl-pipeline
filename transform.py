import pandas as pd
from ingest import load_basics, load_ratings, load_episodes

def transform():
    basics = load_basics()
    ratings = load_ratings()
    episodes = load_episodes()

    print("\nMerging series with ratings...")
    # Merge series with ratings
    df = basics.merge(ratings, on="tconst", how="inner")

    # Only keep series with meaningful data
    df = df[
        (df["numVotes"] >= 1000) &        # at least 1000 votes
        (df["startYear"] >= 2000) &        # modern era
        (df["averageRating"].notna())
    ].copy()

    print(f"Series after filtering: {len(df)}")

    # Calculate number of seasons per show
    print("Calculating seasons per show...")
    seasons = episodes.groupby("parentTconst")["seasonNumber"].nunique().reset_index()
    seasons.columns = ["tconst", "total_seasons"]

    # Calculate total episode count
    ep_count = episodes.groupby("parentTconst")["episodeNumber"].count().reset_index()
    ep_count.columns = ["tconst", "total_episodes"]

    # Merge everything
    df = df.merge(seasons, on="tconst", how="left")
    df = df.merge(ep_count, on="tconst", how="left")

    # Flag cancelled shows
    # A show is "cancelled" if it has an endYear and ran less than 3 seasons
    df["is_cancelled"] = (
        (df["endYear"].notna()) &
        (df["total_seasons"] <= 3) &
        (df["averageRating"] >= 7.0)   # good rating but still ended
    ).astype(int)

    # Clean genres — take first genre only
    df["primary_genre"] = df["genres"].str.split(",").str[0]

    # Drop nulls in key columns
    df = df.dropna(subset=["total_seasons", "total_episodes", "primary_genre"])

    print(f"\n✅ Transform complete")
    print(f"Total shows: {len(df)}")
    print(f"Cancelled (good rating, short run): {df['is_cancelled'].sum()}")
    print(f"Survived: {(df['is_cancelled'] == 0).sum()}")

    return df

if __name__ == "__main__":
    df = transform()
    print("\nSample data:")
    print(df[["primaryTitle", "averageRating", "total_seasons", "is_cancelled"]].head(10))