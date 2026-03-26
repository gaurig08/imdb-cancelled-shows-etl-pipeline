-- 1. Which genres have the most cancellations?
SELECT g.genre_name,
       COUNT(*) FILTER (WHERE f.is_cancelled = 1) AS cancelled,
       COUNT(*) FILTER (WHERE f.is_cancelled = 0) AS survived,
       ROUND(AVG(f.average_rating)::numeric, 2) AS avg_rating
FROM fact_shows f
JOIN dim_genre g ON f.genre_id = g.genre_id
GROUP BY g.genre_name
ORDER BY cancelled DESC
LIMIT 10;

-- 2. High rated but cancelled shows (the injustice list)
SELECT title, average_rating, total_seasons,
       total_episodes, start_year, end_year
FROM fact_shows
WHERE is_cancelled = 1
ORDER BY average_rating DESC
LIMIT 20;

-- 3. Does more episodes = better survival?
SELECT is_cancelled,
       ROUND(AVG(total_episodes)::numeric, 1) AS avg_episodes,
       ROUND(AVG(total_seasons)::numeric, 1) AS avg_seasons,
       ROUND(AVG(average_rating)::numeric, 2) AS avg_rating,
       COUNT(*) AS total_shows
FROM fact_shows
GROUP BY is_cancelled;

-- 4. Cancellation trend by decade
SELECT (start_year / 10 * 10) AS decade,
       COUNT(*) FILTER (WHERE is_cancelled = 1) AS cancelled,
       COUNT(*) FILTER (WHERE is_cancelled = 0) AS survived
FROM fact_shows
WHERE start_year IS NOT NULL
GROUP BY decade
ORDER BY decade;

-- 5. What rating threshold saves a show?
SELECT
  CASE
    WHEN average_rating >= 9.0 THEN '9.0+'
    WHEN average_rating >= 8.0 THEN '8.0-8.9'
    WHEN average_rating >= 7.0 THEN '7.0-7.9'
    ELSE 'below 7'
  END AS rating_bucket,
  COUNT(*) FILTER (WHERE is_cancelled = 1) AS cancelled,
  COUNT(*) FILTER (WHERE is_cancelled = 0) AS survived
FROM fact_shows
GROUP BY rating_bucket
ORDER BY rating_bucket DESC;