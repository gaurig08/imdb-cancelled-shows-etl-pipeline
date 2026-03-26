import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
from sqlalchemy import create_engine

DB_URL = "postgresql://postgres:password@localhost:5432/shows_db"
engine = create_engine(DB_URL)

sns.set_theme(style="darkgrid")
plt.rcParams["figure.dpi"] = 150

# --- Load data ---
df = pd.read_sql("SELECT * FROM fact_shows", engine)
genre_df = pd.read_sql("SELECT * FROM dim_genre", engine)
df = df.merge(genre_df, on="genre_id", how="left")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle("Why Do Good Shows Get Cancelled?\nIMDb Data Analysis (2000–Present)",
             fontsize=16, fontweight="bold", y=1)

# --- Chart 1: Cancellation by Genre ---
genre_stats = df.groupby("genre_name").agg(
    cancelled=("is_cancelled", "sum"),
    total=("is_cancelled", "count")
).reset_index()
genre_stats["cancel_rate"] = genre_stats["cancelled"] / genre_stats["total"] * 100
genre_stats = genre_stats[genre_stats["total"] >= 20].sort_values("cancel_rate", ascending=False).head(10)

axes[0, 0].barh(genre_stats["genre_name"], genre_stats["cancel_rate"], color="#e05c5c")
axes[0, 0].set_title("Cancellation Rate by Genre", fontweight="bold")
axes[0, 0].set_xlabel("Cancellation Rate (%)")
axes[0, 0].xaxis.set_major_formatter(mtick.PercentFormatter())

# --- Chart 2: Rating distribution cancelled vs survived ---
cancelled = df[df["is_cancelled"] == 1]["average_rating"]
survived = df[df["is_cancelled"] == 0]["average_rating"]
axes[0, 1].hist(survived, bins=20, alpha=0.6, label="Survived", color="#5c9ee0")
axes[0, 1].hist(cancelled, bins=20, alpha=0.6, label="Cancelled", color="#e05c5c")
axes[0, 1].set_title("Rating Distribution: Cancelled vs Survived", fontweight="bold")
axes[0, 1].set_xlabel("IMDb Rating")
axes[0, 1].set_ylabel("Number of Shows")
axes[0, 1].legend()

# --- Chart 3: Cancellation by decade ---
decade_df = df.copy()
decade_df["decade"] = (decade_df["start_year"] // 10 * 10).astype("Int64")
decade_stats = decade_df.groupby("decade").agg(
    cancelled=("is_cancelled", "sum"),
    survived=("is_cancelled", lambda x: (x == 0).sum())
).reset_index().dropna()
decade_stats = decade_stats[decade_stats["decade"] >= 2000]

x = range(len(decade_stats))
axes[1, 0].bar(x, decade_stats["survived"], label="Survived", color="#5c9ee0")
axes[1, 0].bar(x, decade_stats["cancelled"], bottom=decade_stats["survived"],
               label="Cancelled", color="#e05c5c")
axes[1, 0].set_xticks(x)
axes[1, 0].set_xticklabels(decade_stats["decade"].astype(str))
axes[1, 0].set_title("Cancellation Trend by Decade", fontweight="bold")
axes[1, 0].set_ylabel("Number of Shows")
axes[1, 0].legend()

# --- Chart 4: Avg episodes cancelled vs survived ---
ep_stats = df.groupby("is_cancelled").agg(
    avg_episodes=("total_episodes", "mean"),
    avg_rating=("average_rating", "mean")
).reset_index()
ep_stats["label"] = ep_stats["is_cancelled"].map({0: "Survived", 1: "Cancelled"})

axes[1, 1].bar(ep_stats["label"], ep_stats["avg_episodes"],
               color=["#5c9ee0", "#e05c5c"])
axes[1, 1].set_title("Avg Episodes: Cancelled vs Survived", fontweight="bold")
axes[1, 1].set_ylabel("Average Episode Count")
for i, v in enumerate(ep_stats["avg_episodes"]):
    axes[1, 1].text(i, v + 1, f"{v:.1f}", ha="center", fontweight="bold")

plt.tight_layout()
plt.subplots_adjust(top=1)
plt.savefig("dashboard.png", bbox_inches="tight")
print("✅ Dashboard saved as dashboard.png")
plt.show()