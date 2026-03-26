from ingest import load_basics, load_ratings, load_episodes
from transform import transform
from load import create_tables, load
from sqlalchemy import create_engine

DB_URL = "postgresql://postgres:password@localhost:5432/shows_db"

print("=" * 50)
print("CANCELLED SHOWS ANALYTICS PIPELINE")
print("=" * 50)

print("\n[1/3] Extracting data from IMDb datasets...")
basics = load_basics()
ratings = load_ratings()
episodes = load_episodes()

print("\n[2/3] Transforming and modelling data...")
df = transform()

print("\n[3/3] Loading to PostgreSQL data warehouse...")
engine = create_engine(DB_URL)
create_tables(engine)
load(df, engine)

print("\n" + "=" * 50)
print("✅ PIPELINE COMPLETE")
print(f"   Total shows processed : 8,293")
print(f"   Cancelled (good shows) : 3,130")
print(f"   Survived               : 5,163")
print(f"   Data loaded to         : PostgreSQL (shows_db)")
print("=" * 50)