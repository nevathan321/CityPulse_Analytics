# CityPulse: Toronto 311 Dashboard

CityPulse is an interactive dashboard for visualizing and predicting Toronto 311 service requests. It features real-time data visualizations, machine learning predictions, and insightful KPIs for city operations.

## Features

- Interactive charts for service requests by time, ward, status, division, and more
- Machine learning model to predict request completion
- KPI highlights for city performance
- Modern frontend with Plotly.js and responsive design
- Flask backend serving processed data and ML predictions

## Project Structure

```
LICENSE
README.md
requirements.txt
backend/
    app.py
data/
    processed/
        insights.json
        model.joblib
    raw/
        SR2025.csv
data_pipeline/
    data_pipeline.py
frontend/
    index.html
    main.js
    styles.css
Pyt/
    classification/
        start.py
    data/
        fetch.py
        SR2025.csv
    visualizations/
        daysData.txt
        Requests_per_hour.py
        requestsDivision.py
        SR_per_day.py
        statusCompare.py
        top_SRQ.py
        wardRequests.py
        weekDaysData.py
```

## Installation

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/CityPulse-.git
cd CityPulse-
```

### 2. Install Python Dependencies

It is recommended to use a virtual environment:

```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Prepare Data

- Place your raw data CSV in `data/raw/SR2025.csv`.
- Run the data pipeline to process data and train the ML model:

```sh
python data_pipeline/data_pipeline.py
```

This will generate `insights.json` and `model.joblib` in `data/processed/`.

### 4. Start the Backend

```sh
python backend/app.py
```

The backend will run at `http://localhost:5000/api`.

### 5. Start the Frontend

Open `frontend/index.html` in your browser.  
Make sure the backend is running for full functionality.

## Usage

- View KPIs and charts on the dashboard.
- Use the ML prediction form to estimate the likelihood of request completion.
- If the backend is not running, the dashboard will show placeholder data.

## Development

- Frontend code: [frontend/main.js](frontend/main.js), [frontend/styles.css](frontend/styles.css)
- Backend code: [backend/app.py](backend/app.py)
- Data pipeline: [data_pipeline/data_pipeline.py](data_pipeline/data_pipeline.py)
- ML and analysis scripts: [Pyt/](Pyt/)

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

*Developed by Muntasir Contractor & Nevathan Arasanchandrasegara
