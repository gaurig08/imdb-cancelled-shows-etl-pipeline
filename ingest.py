import pandas as pd
import os

DATA_PATH = "data/"

def load_basics():
    print("Loading title basics...")
    df = pd.read_csv(
        os.path.join(DATA_PATH, "title.basics.tsv"),
        sep="\t",
        na_values="\\N",
        low_memory=False,
        usecols=["tconst", "titleType", "primaryTitle", "startYear", "endYear", "genres", "runtimeMinutes"]
    )
    # Keep only TV series
    df = df[df["titleType"] == "tvSeries"].copy()
    df["startYear"] = pd.to_numeric(df["startYear"], errors="coerce")
    df["endYear"] = pd.to_numeric(df["endYear"], errors="coerce")
    df["runtimeMinutes"] = pd.to_numeric(df["runtimeMinutes"], errors="coerce")
    print(f"Found {len(df)} TV series")
    return df

def load_ratings():
    print("Loading ratings...")
    df = pd.read_csv(
        os.path.join(DATA_PATH, "title.ratings.tsv"),
        sep="\t",
        na_values="\\N"
    )
    print(f"Found {len(df)} ratings")
    return df

def load_episodes():
    print("Loading episodes...")
    df = pd.read_csv(
        os.path.join(DATA_PATH, "title.episode.tsv"),
        sep="\t",
        na_values="\\N"
    )
    df["seasonNumber"] = pd.to_numeric(df["seasonNumber"], errors="coerce")
    df["episodeNumber"] = pd.to_numeric(df["episodeNumber"], errors="coerce")
    print(f"Found {len(df)} episodes")
    return df

if __name__ == "__main__":
    basics = load_basics()
    ratings = load_ratings()
    episodes = load_episodes()
    print("\n✅ All data loaded successfully")
    print(f"Series: {len(basics)} | Ratings: {len(ratings)} | Episodes: {len(episodes)}")