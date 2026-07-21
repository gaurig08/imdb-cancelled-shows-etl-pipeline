# Interview Prep — IMDb Cancelled Shows ETL Pipeline

## 30-second summary (memorize this)

"I built a pipeline that pulls IMDb's public TV dataset, filters it
down to shows with meaningful vote counts, and engineers a specific
label: was this show actually good (7.0+ rating) but still cancelled
within 3 seasons? Out of about 8,300 shows, roughly 3,100 fit that
pattern. I loaded the result into a small star-schema warehouse and
built a Power BI dashboard so you can slice the cancellation rate by
genre and decade interactively."

## Likely questions and how to answer them

**Q: Walk me through the pipeline.**
A: Extract (`ingest.py` reads title basics, ratings, and episode
data from IMDb's TSVs) → Transform (`transform.py` merges them,
filters low-signal rows, computes seasons/episodes per show, and
flags `is_cancelled`) → Load (either into PostgreSQL as a star
schema, or exported to CSV for Power BI).

**Q: Why the specific filters — 1,000+ votes, 2000+ start year?**
A: Vote count is a proxy for how many people actually watched and
rated a show; shows with only a handful of votes produce unreliable
average ratings. The 2000+ start year keeps the analysis to the
streaming/modern-TV era, where cancellation patterns are more
comparable to each other than, say, a 1960s network show.

**Q: Why is "cancelled" defined as rating >= 7.0 AND <= 3 seasons?**
A: Because the interesting business question isn't "which shows
ended" — most shows end eventually. It's "which shows ended despite
being good," which is the pattern viewers actually complain about.
Rating alone doesn't capture "ended early"; season count alone
doesn't capture "was actually good." Combining both is what makes the
flag meaningful.

**Q: What are the weaknesses of this definition?**
A: A few, worth naming proactively:
1. It can't distinguish "cancelled by the network" from "creators
   planned a 3-season limited series" — both look identical in this
   data. A true cancellation flag would need production/announcement
   data IMDb doesn't expose.
2. The 7.0 and 3-season thresholds are somewhat arbitrary judgment
   calls, not derived from any external validation.
3. Vote count and rating can be inflated by review-bombing or
   coordinated voting, which this pipeline doesn't attempt to detect.

**Q: Why a star schema (dim_genre + fact_shows) instead of one flat
table?**
A: It avoids repeating genre name text on every one of 8,000+ rows,
keeps the fact table lean, and matches how Power BI/most BI tools
expect data to be modeled for efficient relationships and
aggregation.

**Q: Why Power BI instead of just Matplotlib?**
A: Matplotlib produces a fixed 4-panel PNG — great for a one-time
snapshot, but a reviewer can't ask "show me just sci-fi shows" without
someone re-running the script. Power BI's slicers make that
self-service, and DAX measures like Cancellation Rate % recompute
live under any filter combination.

**Q: How would you extend this into a real product?**
A: Turn `is_cancelled` from a rule-based flag into an actual ML
classifier trained on early-season signals (rating trajectory across
season 1, vote velocity, genre, network) to *predict* cancellation
risk before a show is fully aired — instead of only labeling it after
the fact.

**Q: How would you productionize the pipeline itself?**
A: Move it to Airflow/Prefect for scheduled reruns as IMDb refreshes
its datasets (they update daily), switch from full reload to
incremental loading keyed on `tconst`, and point Power BI at the
PostgreSQL warehouse directly with scheduled refresh instead of
manual CSV re-export.
