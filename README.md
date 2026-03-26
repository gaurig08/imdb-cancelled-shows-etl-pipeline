# IMDb Cancelled Shows ETL Pipeline

End-to-end ETL pipeline analyzing 8K+ IMDb TV shows to identify cancellation patterns using Python, SQL, and PostgreSQL.

---

## Overview

This project builds a data engineering pipeline that:

• Extracts IMDb datasets  
• Transforms and cleans data  
• Engineers analytical features  
• Loads data into PostgreSQL  
• Performs SQL analysis  
• Generates visual insights  

---

## Tech Stack

**Languages:** Python, SQL  

**Libraries:**  
Pandas  
SQLAlchemy  
Matplotlib  
Seaborn  

**Tools:**  
PostgreSQL  
Docker  
Git  

---

## Pipeline Architecture


IMDb Data → Ingestion → Transformation → PostgreSQL → SQL Analysis → Dashboard


---

## Key Features

• Processed 8,293 TV shows  
• Identified 3,130 cancelled shows  
• Built star-schema warehouse  
• Created cancellation detection logic  
• SQL analytics on genre & ratings  
• Visualization dashboard  

---

## How to Run

Install dependencies:


pip install -r requirements.txt


Run pipeline:


python pipeline.py


Run analysis:


psql shows_db < analyze.sql


Generate dashboard:


python dashboard.py


---

## Project Structure


├── ingest.py
├── transform.py
├── load.py
├── pipeline.py
├── analyze.sql
├── dashboard.py
├── requirements.txt
└── README.md


---

## Skills Demonstrated

ETL Pipeline  
Data Cleaning  
Feature Engineering  
SQL Analytics  
Data Warehousing  
Visualization  

---

## Future Improvements

Airflow orchestration  
Incremental loading  
ML prediction model  
Cloud deployment
