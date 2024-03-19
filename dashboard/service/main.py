from typing import Optional
from fastapi import FastAPI, Request, Header
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates  # For HTML templates

import debugpy  # For debugging

import pandas as pd
import plotly.express as px
import plotly.io as pio
import os  # For file paths

# For debugging
debugpy.listen(("0.0.0.0", 5678))

# Create the FastAPI app
app = FastAPI()

# Templates
templates_directory = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "../templates/")
)
templates = Jinja2Templates(directory=templates_directory)


def load_csv():
    # Load data
    print("Reading JSON input")

    data_folder_path = os.path.join(os.path.dirname(__file__), "../../data/")
    csv_file_path = os.path.normpath(
        data_folder_path + "courses_numerical_categorical_data.csv"
    )

    df = pd.read_csv(csv_file_path)
    df.info()

    print("Finished loading data from csv")
    return df


courses_data = load_csv()
# Sort data frame by number od subscribers
courses_data.sort_values(
    by='num_subscribers',
    ascending=False,
    inplace=True
)

# Routes


# Root route
@app.get("/")
def read_root():
    return {"Container FastAPI + Docker!"}


@app.get("/movies", response_class=HTMLResponse)
async def movielist(request: Request,
                    hx_request: Optional[str] = Header(None)):
    films = [
        {'name': 'Blade Runner', 'director': 'Ridley Scott'},
        {'name': 'Pulp Fiction', 'director': 'Quentin Tarantino'},
        {'name': 'Mulholland Drive', 'director': 'David Lynch'},
    ]
    context = {"request": request, 'films': films}
    if hx_request:
        return templates.TemplateResponse("partials/table.html", context)
    return templates.TemplateResponse("index.html", context)


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request,
                    hx_request: Optional[str] = Header(None)):
    context = {"request": request, 'courses': courses_data}
    return templates.TemplateResponse("dashboard.html", context)


@app.get("/dashboard/histogram", response_class=HTMLResponse)
async def dashboard_chart(request: Request,
                          hx_request: Optional[str] = Header(None)):
    fig = px.strip(
        courses_data, x="num_subscribers",
        hover_data=courses_data.columns
    )

    chart_html = pio.to_html(fig, full_html=False)

    context = {
        "request": request,
        'courses': courses_data,
        'chart': chart_html
    }

    return templates.TemplateResponse("chart.html", context)
