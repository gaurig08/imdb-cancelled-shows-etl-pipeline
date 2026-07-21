# Power BI Build Guide — IMDb Cancelled Shows

Follow these steps in **Power BI Desktop**. Total build time: 30–40
minutes.

## 1. Get the data

1. Run `python pipeline.py` (after placing the IMDb .tsv files in
   `data/`) so `powerbi/dim_genre.csv` and `powerbi/fact_shows.csv`
   exist.
2. **Home → Get Data → Text/CSV** → load `powerbi/dim_genre.csv` →
   **Transform Data**.
3. **Get Data → Text/CSV** → load `powerbi/fact_shows.csv` →
   **Transform Data**.

## 2. Clean up types in Power Query

For **fact_shows**:
- `genre_id`, `start_year`, `end_year`, `num_votes`, `total_seasons`,
  `total_episodes`, `runtime_minutes`, `is_cancelled` → Whole Number
- `average_rating` → Decimal Number
- `title` → Text
- Rename the query to `fact_shows`

For **dim_genre**:
- `genre_id` → Whole Number, `genre_name` → Text
- Rename the query to `dim_genre`

Click **Close & Apply**.

## 3. Build the relationship

**Model view** → drag `genre_id` from `fact_shows` onto `genre_id` in
`dim_genre`. Confirm **One (dim_genre) to Many (fact_shows)**, single
cross-filter direction from `dim_genre` → `fact_shows`.

## 4. Add a decade column

You'll want to group by decade like the original SQL analysis did.
In Power Query, add a **Custom Column** on `fact_shows`:

```
Decade = Number.RoundDown([start_year] / 10) * 10
```

## 5. Add DAX measures

```DAX
Cancellation Rate % = 
DIVIDE(
    CALCULATE(COUNTROWS(fact_shows), fact_shows[is_cancelled] = 1),
    COUNTROWS(fact_shows)
)
```

```DAX
Avg Rating = AVERAGE(fact_shows[average_rating])
```

```DAX
Avg Episodes = AVERAGE(fact_shows[total_episodes])
```

```DAX
Total Shows = COUNTROWS(fact_shows)
```

```DAX
Cancelled Shows = CALCULATE([Total Shows], fact_shows[is_cancelled] = 1)
```

## 6. Build the visuals

Create a page called **"Why Do Good Shows Get Cancelled?"** and add:

1. **Bar chart — Cancellation Rate by Genre**: Axis = `genre_name`,
   Value = `Cancellation Rate %`. Filter to genres with a reasonable
   sample size (e.g. add a visual-level filter: Total Shows ≥ 20).
2. **Histogram — rating distribution**: Use `average_rating` on the
   axis (binned), with `is_cancelled` as legend/small multiple, to
   compare cancelled vs. survived rating distributions.
3. **Line/column chart — cancellation trend by decade**: Axis =
   `Decade`, Values = `Total Shows` and `Cancelled Shows` (or stacked
   column: survived vs cancelled).
4. **Clustered column — avg episodes cancelled vs. survived**: Axis
   = `is_cancelled`, Value = `Avg Episodes`.
5. **Card visuals**: `Total Shows`, `Cancelled Shows`,
   `Cancellation Rate %`.
6. **Slicers**: `genre_name`, `Decade`.

## 7. Polish

- Give it a clear title and one-line takeaway (e.g. "Comedy and
  Drama see the highest cancellation rates despite strong ratings").
- Save/publish and screenshot for your portfolio.

## Talking points if asked "why Power BI here?"

- Lets a viewer filter by genre/decade interactively instead of
  regenerating a 4-panel Matplotlib figure for every slice they want
  to see.
- DAX measures like `Cancellation Rate %` recompute live under any
  filter combination — the Python version only ever showed the
  overall global rate per chart.
- This makes the same underlying analysis reusable for other
  stakeholders without touching Python.
