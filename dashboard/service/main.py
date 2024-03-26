from typing import Optional
from fastapi import FastAPI, Request, Header
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates  # For HTML templates
from fastapi.staticfiles import StaticFiles  # for mounting static files
from fastapi.responses import RedirectResponse

import os  # For file paths
import debugpy  # For debugging

# Importing scripts
from dashboard.service.udemy_stats import courses_stats

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


# Routes
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request,
                    hx_request: Optional[str] = Header(None)):
    context = {
        "request": request,
        "summary_stats": {
            "num_courses": len(courses_stats.courses)
        },
        "chart": courses_stats.plot
    }

    return templates.TemplateResponse("dashboard.html", context)


@app.get("/notebook")
async def redirect_to_new_url():
    return RedirectResponse(url="/assets/notebook.html")
