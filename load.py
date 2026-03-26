import pandas as pd
from sqlalchemy import create_engine, text
from transform import transform

DB_URL = "postgresql://postgres:password@localhost:5432/shows_db"

def create_tables(engine):
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dim_genre (
                genre_id SERIAL PRIMARY KEY,
                genre_name VARCHAR(100) UNIQUE
            );
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS fact_shows (
                tconst VARCHAR(20) PRIMARY KEY,
                title VARCHAR(300),
                start_year INT,
                end_year INT,
                average_rating FLOAT,
                num_votes INT,
                total_seasons INT,
                total_episodes INT,
                runtime_minutes INT,
                is_cancelled INT,
                genre_id INT REFERENCES dim_genre(genre_id)
            );
        """))
        conn.commit()
    print("✅ Tables created")

def load_genres(df, engine):
    genres = df["primary_genre"].dropna().unique()
    genre_df = pd.DataFrame({"genre_name": genres})
    genre_df.to_sql("dim_genre", engine, if_exists="append", index=False)
    
    # Get genre IDs back
    genre_map = pd.read_sql("SELECT genre_id, genre_name FROM dim_genre", engine)
    return dict(zip(genre_map["genre_name"], genre_map["genre_id"]))

def load(df, engine):
    genre_map = load_genres(df, engine)
    df["genre_id"] = df["primary_genre"].map(genre_map)
    
    fact_df = df[[
        "tconst", "primaryTitle", "startYear", "endYear",
        "averageRating", "numVotes", "total_seasons",
        "total_episodes", "runtimeMinutes", "is_cancelled", "genre_id"
    ]].copy()

    fact_df.columns = [
        "tconst", "title", "start_year", "end_year",
        "average_rating", "num_votes", "total_seasons",
        "total_episodes", "runtime_minutes", "is_cancelled", "genre_id"
    ]

    fact_df["end_year"] = fact_df["end_year"].astype("Int64")
    fact_df["start_year"] = fact_df["start_year"].astype("Int64")
    fact_df["runtime_minutes"] = fact_df["runtime_minutes"].astype("Int64")
    fact_df["total_seasons"] = fact_df["total_seasons"].astype("Int64")
    fact_df["total_episodes"] = fact_df["total_episodes"].astype("Int64")

    fact_df.to_sql("fact_shows", engine, if_exists="append", index=False)
    print(f"✅ Loaded {len(fact_df)} shows into fact_shows")

if __name__ == "__main__":
    engine = create_engine(DB_URL)
    print("Creating tables...")
    create_tables(engine)
    print("Transforming data...")
    df = transform()
    print("Loading to PostgreSQL...")
    load(df, engine)
    print("\n✅ Load complete")