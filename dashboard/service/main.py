from typing import Optional
from fastapi import FastAPI, Request, Header
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates  # For HTML templates
from fastapi.staticfiles import StaticFiles  # for mounting static files
from fastapi.responses import RedirectResponse
import copy

import os  # For file paths
import debugpy  # For debugging

# Importing scripts
from dashboard.service.udemy_stats.courses_stats import Courses
import dashboard.service.udemy_stats.courses_stats as courses_stats

# For debugging
debugpy.listen(("0.0.0.0", 5678))

# Create the FastAPI app
app = FastAPI()

# Set-up templating engine
templates_directory = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "../templates/")
)
templates = Jinja2Templates(directory=templates_directory)

# Mount static assets
app.mount("/assets", StaticFiles(directory="./dashboard/assets"), name="assets")

"""Load all data
To accelerate the request, we'll load the data beforehand.
"""

# generate scatter plot of courses for chosen category
def load_dashboard_sections(courses, subcategories_filter=[]):

    subcategories_in_use = ", ".join(subcategories_filter)
    if len(subcategories_filter) == 0: 
        subcategories_in_use = 'all categories'

    return [
        {
            "title": "Courses overview",
            "description": f"Below you have a list of top 10 courses and the scatter of all courses in the following subcategories: {subcategories_in_use}.",
            "charts": [
                courses_stats.plot_scatter(courses.df),
                courses_stats.plot_box_deciles(courses.df)
            ],
            "tables": [
                {
                    "title": "Top 10 courses",
                    "data": (
                        courses
                        .top10_by_revenue()[['title', 'num_subscribers', 'price', 'estimated_revenue']]
                        .rename(columns={
                            'title': 'Course',
                            'num_subscribers': 'Subscribers',
                            'price': 'Price',
                            'estimated_revenue': 'Revenue (millions USD)'}
                        )
                    )
                }
            ]
        },
        {
            "title": "Ratings",
            "description": f"How does the ratings of a course in { subcategories_in_use } could afect the number of subscribers?",
            "charts": [
                courses_stats.plot_scatter_ratings(courses.df)
            ]
        },
        {
            "title": "Price",
            "description": f"How does the pricing of a course in { subcategories_in_use } could afect the number of subscribers?",
            "charts": [
                courses_stats.plot_scatter_price(courses.df)
            ],
            "tables": [
                {
                    "title": "Price categories",
                    "data": courses.price_categories()
                }
            ]
        },
        {
            "title": "Time of Publication",
            "description": f"How does the time of publication could affect the number of subscribers of a course in { subcategories_in_use }?",
            "charts": [
                courses_stats.plot_time_publication(courses.df),
                courses_stats.plot_subscribers_by_year(courses.df)
            ]
        },
        {
            "title": "Curriculum and Course Length",
            "description": f"How does the number of curriculum items and content length in { subcategories_in_use } could affect the number of subscribers of a course?",
            "charts": [
                courses_stats.plot_scatter_curriculum_items(courses.df),
                courses_stats.plot_scatter_content_length(courses.df)
            ]
        },
        {
            "title": "Topics",
            "description": f"What are the topics most popular in a courses in { subcategories_in_use }?",
            "charts": [
                courses_stats.plot_topn_labels_by_count(courses.df)
            ]
        },
        {
            "title": "Instructors",
            "description": f"What are the most popular instructors in { subcategories_in_use }?",
            "charts": [
                courses_stats.plot_topn_instructors_by_subscribers(courses.df),
                courses_stats.plot_topn_instructors_by_courses(courses.df)
            ]
        }
    ]

# Load courses 
data_folder_path = os.path.join(
    os.path.dirname(__file__), "../../data/"
)

file_path = os.path.normpath(
    data_folder_path + "courses_numerical_categorical_data.csv"
)

# First load
courses = Courses(csv_file_path=file_path)
all_categories = courses.subcategories()

# Get data to fill dashboard
stats = courses.summarize()
dashboard_sections = load_dashboard_sections(courses=courses)

# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request,
                    hx_request: Optional[str] = Header(None)):
    context = {
        "request": request,
        "summary_stats": stats,
        "sections": dashboard_sections,
        "subcategories": all_categories
    }

    return templates.TemplateResponse("dashboard.html", context)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request,
                    subcategory: str = None,
                    hx_request: Optional[str] = Header(None)):
    
    courses_filtered = copy.deepcopy(courses)

    if subcategory is None:
        subcategories_filter = []
    if subcategory == "All Subcategories":
        subcategories_filter = []
    else:
        subcategories_filter = [subcategory]
        courses_filtered.filter_by_subcategories(subcategories_filter)

    # Get data to fill dashboard
    stats = courses_filtered.summarize()
    dashboard_sections = load_dashboard_sections(courses=courses_filtered, subcategories_filter=subcategories_filter)

    context = {
        "request": request,
        "summary_stats": stats,
        "sections": dashboard_sections,
        "subcategories": all_categories
    }
    return templates.TemplateResponse("partials/dashboard_content.html", context)

@app.get("/notebook")
async def redirect_to_new_url():
    return RedirectResponse(url="/assets/notebook.html")
