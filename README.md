# Project

### **Goal**

There are several providers such as Coursera, Youtube, Udemy, etc. Many course instructors also choose to publish the course themselves. Taking the perspective of a vendor or an instructor, there are two main questions I want to investigate

* Which categories are the most successful? e.g. Data Science, Java, React.
* What factors are most important to the success of the course in these categories?

### **Record**

I hope that by understanding the Udemy courses data, I can gain insight into the questions. I can't select all course categories, so I chose Udemy courses in software development (https://www.udemy.com/courses/development/).

All course details were scraped from the Udemy website using a web scraping tool (Apify). No private data was read, i.e. only publicly available data for search engines was taken into account. The dataset contains 10,000 courses and is stored in a JSON file. Each sample (a course) is a mix of numerical, textual, pictorial, and categorical information. This enables different analysis methods for this and other projects.

**Challenges and Considerations with Data**

*Unfortunately, this data set does not contain any information regarding the way we promote a course or conversion rate optimization. The Udemy recommender system, the price optimization algorithm, and online advertising (e.g. through the newsletter, or search engines, or social networks) could have a greater influence on the success of a course.

* Additionally, Udemy offers ongoing discounts for new and existing users. Therefore, we cannot completely rely on the pricing data. In any case, the discounts are usually proportional to the original course prices.

* The data set is read via a US-based proxy. This means that all information is stored in English. In addition, your location could influence the information read out.

### Project steps

**1. :white_check_mark: Create record**

I used a "scrapper" from Apify (online infrastructure provider for running crawler scripts) to collect the data.

I didn't create the scrapper myself, but found an existing one. However, the Scrapper required several trial runs to work. Creating the complete data set takes several hours (around 3 hours to be exact).

The data was saved in a 72MB JSON file. The JSON file contains 10,000 courses. In the `/extract` folder you will find the Python script to start the scrapper "remotely", but it requires an Apify API key.

The result can be found in the `/data` folder. The JSON file is called `courses_udemy_raw.json`.

**2. :white_check_mark: Cleaning and preparing the data set**

From the `courses_udemy_raw.json` file I created two CSV files. `courses_numerical_categorical_data.csv` is the numeric and categorical data set, `courses_textual_data.csv` is the textual data set. I also created an example file for each data set (with 10% of the data).

The transformation scripts are saved in the `transformation` folder. You extract the data from `courses_udemy_raw.json` and write it in CSV format. You also edit each column to clean it up and write only the relevant information.

I didn't use Jupyter notebooks because I needed reliable and fast data slicing.

**3. :white_check_mark: Explotative analysis in Jupyter Notebook**

Please see the file `analyse_udemy_courses.ipynb` in the `analysis` folder. It contains detailed analysis of the dataset.

**4. :white_check_mark: Web dashboard**

I created a web app structure using FastAPI/HTMX/Tailwind to display the most import charts from the exploratory data analysis. It allows the user to select which categories to explore, and shows all charts and KPIs based on the selection.

**5. :white_check_mark: Deployment **

I created a Docker setting in `Dockerfile` and `docker-compose.yml` to deploy the project. Fly.io can automatically deploy my web app using the Docker setting.

Unfortunately, the first-page load is slow due to auto-sleep of fly.io (0 machine running to save costs) but as soon as the machine wakes up (~3s) then the dashboard is responsive.
