# Mini-project-Employee-Data-Analytics
A practical project connecting SQL, Python, NumPy and Pandas.

## Employee Data Analytics

A Python project that stores employee records in a SQLite database, queries them with SQL, and analyses them with NumPy and Pandas to produce insights, CSV summaries and charts.

> **Note:** the dataset is **synthetic** (generated with NumPy, fixed seed), so no real employee data is used. Results are for learning and demonstration.

### Features
- **SQLite database** with full CRUD: add, view, search, update, delete employees (`src/database.py`)
- **NumPy data generation**: 300 reproducible employee records across 6 departments (`src/seed_data.py`)
- **SQL analytics**: department summary with `GROUP BY`, top earners with `ORDER BY ... LIMIT`
- **Pandas + NumPy analytics**: salary statistics and percentiles, correlations, linear fit (`np.polyfit`), per-department z-score outlier detection, experience bands, hiring trend
- **Visualisation**: 8 matplotlib charts saved to `outputs/charts/`
- **Auto-generated report** and CSV exports in `outputs/`

### Project Structure
```
├── main.py              # runs the full pipeline
├── requirements.txt
├── src/
│   ├── database.py      # schema + CRUD (sqlite3)
│   ├── seed_data.py     # synthetic data (NumPy)
│   ├── analysis.py      # SQL + Pandas + NumPy analysis
│   └── visualize.py     # matplotlib charts
├── data/                # employees.db is created here (git-ignored)
└── outputs/
    ├── report.txt
    ├── *.csv
    └── charts/*.png
```

### How to Run
```bash
pip install -r requirements.txt
python main.py
```
This creates the database, seeds it on first run, prints the report, and writes everything to `outputs/`.

### Sample Findings (seed 42)
- Highest average pay: Data Science, then Engineering; lowest: HR
- Experience correlates moderately with salary (r ≈ 0.49); performance rating barely does (r ≈ 0.05)
- Each extra year of experience is associated with roughly Rs 31,000 more annual salary
- Raw male–female average pay gap of about 3.7%, which is unadjusted for role, department or experience

### Tech Stack
- Python
- SQL / SQLite
- NumPy
- Pandas
- Matplotlib
- Git & GitHub

### Learning Outcomes
- Database design and SQL fundamentals
- Python–database connectivity
- Data retrieval, manipulation and aggregation
- Statistical analysis with NumPy and Pandas
- Data visualisation and reporting

### Future Improvements
- Command-line menu for the CRUD operations
- Interactive dashboard (Streamlit or Plotly)
- Regression model for salary prediction
