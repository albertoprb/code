# Importing analysis libraries
import pandas as pd
from ast import literal_eval


# Importing charting libraries
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go


class Courses:

    df = None

    def __init__(self, csv_file_path):
        self.load(csv_file_path)

    def load(self, csv_file_path):
        print("Reading JSON input")

        self.df = pd.read_csv(csv_file_path)
        self.df.sort_values(by="num_subscribers", ascending=False, inplace=True)

        self.add_deciles()  # Add a decile column to the dataframe

        print("Finished loading data from csv")
        return self.df

    def add_deciles(self):
        # Calculate deciles and add a new column to the dataframe
        self.df["decile"] = pd.qcut(
            self.df["num_subscribers"],
            q=10,
            labels=[
                "Decile 1",
                "Decile 2",
                "Decile 3",
                "Decile 4",
                "Decile 5",
                "Decile 6",
                "Decile 7",
                "Decile 8",
                "Decile 9",
                "Decile 10",
            ],
        )
        return self.df

    def summarize(self):
        # Summary stats
        # Averaage rate
        # Total number of subscribers
        summary = {
            "num_courses": len(self.df),
            "avg_rate": round(self.df["rating"].mean(), 2), 
            "total_subscribers": self.df["num_subscribers"].sum(),
            "instructors": instructors_summary_from(self.df)["instructors"].count(),
        }
        return summary

    def top10_by_revenue(self):
        courses_with_revenue = self.df.copy()

        # Calculating potential revenue for each course
        # Adding 80% discount because Udemy courses are often on sale. This is the minimum possible revenue.
        # The 0.0000001 is moving it to millions
        courses_with_revenue["estimated_revenue"] = round(
            courses_with_revenue["num_subscribers"]
            * courses_with_revenue["price"]
            * 0.2
            * 0.0000001,
            2,
        )

        courses_top_10_revenue = courses_with_revenue.sort_values(
            by="estimated_revenue", ascending=False
        ).head(10)

        return courses_top_10_revenue

    def filter_by_subcategories(self, subcategories):
        self.df = self.df[self.df["subcategory"].isin(subcategories)]
        return self.df

    def price_categories(self):
        # Creating bins for each price category
        courses_with_price_category = self.df.copy()
        courses_with_price_category['price_category'] = pd.cut(
            courses_with_price_category['price'],
            bins=5,
            labels=['$', '$$', '$$$', '$$$$', '$$$$$']
        )

        # Calculate the stats for each price category
        price_category_summary = (
            courses_with_price_category
            .groupby('price_category', observed=True)['price']
            .agg(['min', 'max', 'mean', 'median', 'count'])
        )
        return price_category_summary
    
    def subcategories(self):
        return self.df["subcategory"].unique()


def plot_scatter(courses):

    fig = px.scatter(
        courses,
        y="num_subscribers",
        x="udemy_id",
        hover_data=courses.columns,
        render_mode="webgl",
    )

    fig_html = pio.to_html(fig, full_html=False)
    print("# Finished creating scatter plot")
    return {"title": "Scatter Plot of Number of Subscribers", "figure": fig_html}


def plot_box_deciles(courses, decile_filter=[]):
    # Create a box plot to visualize dispersion across deciles
    fig = px.box(
        courses[~courses["decile"].isin(decile_filter)],
        x="num_subscribers",
        color="decile",
    )

    # Configure chart labels and focus view
    fig.update_layout(
        yaxis_title="Decile",
        xaxis_title="Total Number of Subscribers",
        xaxis=dict(
            range=[0, 120000]
        ),  # Set the initial y-axis range to focus on lower deciles
    )

    # Add an annotation to explain the chart is opened in a focused view
    fig.add_annotation(
        text="<sup>Opened with Zoom below 120k subscribers. Use autoscale to view all data. </sup> ",
        xref="paper",
        yref="paper",
        x=1,
        y=1.05,
        showarrow=False,
    )

    fig_html = pio.to_html(fig, full_html=False)
    print("# Finished creating box plot with deciles")
    return {"title": "Dispersion of Number of Subscribers per Decile", "figure": fig_html}


def plot_scatter_ratings(courses):
    fig = px.scatter(
        courses,
        y="num_subscribers",
        x="rating",
        trendline="ols",
        color="decile",
        hover_data=courses.columns,
        render_mode="webgl",
    )

    # Configure chart labels and focus view
    fig.update_layout(
        xaxis_title="Rating",
        yaxis_title="Number of Subscribers",
        yaxis=dict(
            range=[0, 300000]
        ),  # Set the initial y-axis range to focus on lower deciles
    )

    # Add an annotation to explain the chart is opened in a focused view
    fig.add_annotation(
        text="<sup>Opened with Zoom below 300k subscribers. Use autoscale to view all data. </sup> ",
        xref="paper",
        yref="paper",
        x=1,
        y=1.05,
        showarrow=False,
    )

    fig_html = pio.to_html(fig, full_html=False)
    print("# Finished creating scatter of ratings")
    return {"title": "Number of Subscribers vs. Rating", "figure": fig_html}


def plot_scatter_price(courses):
    # Create scatter plot
    fig = px.scatter(
        courses,
        y="num_subscribers",
        x="price",
        trendline="ols",
        color="decile",
        hover_data=courses.columns
    )

    # Configure chart labels and focus view
    fig.update_layout(
        xaxis_title="Price",
        yaxis_title="Number of Subscribers",
        yaxis=dict(range=[0, 300000])  # Set the initial y-axis range to focus on lower deciles
    )

    # Add an annotation to explain the chart is opened in a focused view
    fig.add_annotation(
        text="<sup>Opened with Zoom below 300k subscribers. Use autoscale to view all data. </sup> ",
        xref="paper", yref="paper",
        x=1, y=1.05,
        showarrow=False,
    )

    fig_html = pio.to_html(fig, full_html=False)
    print("# Finished creating scatter of price")
    return {"title": "Number of Subscribers vs. Price", "figure": fig_html}


def plot_time_publication(courses):
    # Prepare a new dataframe with created year and sorted by year
    courses_with_created_year = courses.copy()
    courses_with_created_year['created_year'] = (
        courses_with_created_year['created']
        .apply(lambda date: pd.Timestamp(date).year)
    )

    # Sort by created date to create line plot
    df_line_trace = courses_with_created_year.sort_values(by='created', ascending=True)
    df_line_trace.reset_index(drop=True, inplace=True) # Reset index and drop the old index

    # Plot line with course 'index' over the time
    line_trace = go.Scatter(
        x=df_line_trace['created'], 
        y=df_line_trace.index,
        name="Cumulative courses created"
    )

    # Counting the values per year
    df_bar_trace = (
        courses_with_created_year['created_year']
        .value_counts()
        .reset_index()
    )

    # Plotting the number of courses per year
    bar_trace = go.Bar(
        y=df_bar_trace['count'], 
        x=df_bar_trace['created_year'],
        name="Courses created per year"
    )

    fig = go.Figure(data=[line_trace, bar_trace])

    fig.update_xaxes(tickvals=courses_with_created_year['created_year'], tickformat="%Y")
    
    fig_html = pio.to_html(fig, full_html=False)
    print("# Finished creating scatter of time of publication")
    return {"title": "Courses over time", "figure": fig_html}

def plot_subscribers_by_year(courses):
    courses_with_created_year = courses.copy()
    courses_with_created_year['created_year'] = (
        courses_with_created_year['created']
        .apply(lambda date: pd.Timestamp(date).year)
    )

    #courses_with_created_year = courses_with_created_year[~courses_with_created_year['decile'].isin(['Decile 10'])] # Remove the last decile

    # Create box chart
    fig = px.box(
        courses_with_created_year,
        x='created_year',
        y='num_subscribers',
        hover_data=courses_with_created_year.columns
    )

    # Configure chart labels and focus view
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Number of subscribers",
        yaxis=dict(range=[0, 75000])  # Set the initial y-axis range to focus on lower deciles
    )

    fig.update_xaxes(tickvals=courses_with_created_year['created_year'], tickformat="%Y")

    fig.add_annotation(
        text="<sup>Opened with Zoom below 75k subscribers. Use autoscale to view all data. </sup> ",
        xref="paper", yref="paper",
        x=1, y=1.05,
        showarrow=False,
    )

    # Show the box plot
    fig_html = pio.to_html(fig, full_html=False)
    print("# Finished creating plot of subscribers by year")
    return {"title": "Number of subscribers by year", "figure": fig_html}

def plot_scatter_curriculum_items(courses):
    fig = px.scatter(
        courses,
        x="num_curriculum_items",
        y="num_subscribers",
        trendline="ols",
        color="decile",
        hover_data=courses.columns
    )

    fig.update_layout(
        height=600,
        yaxis=dict(range=[0, 1000000])  # Set the initial y-axis range to make the visual less affected by outliers
    )

    # Add an annotation to explain the chart is opened in a focused view
    fig.add_annotation(
        text="<sup>Opened with Zoom below 1M subscribers. Use autoscale to view all data. </sup> ",
        xref="paper", yref="paper",
        x=1, y=1.05,
        showarrow=False,
    )

    # Show the box plot
    fig_html = pio.to_html(fig, full_html=False)
    print("# Finished creating scatter plot of curriculum items")
    return {"title": "Number of Subscribers vs Curriculum Items", "figure": fig_html}

def plot_scatter_content_length(courses):
    fig = px.scatter(
        courses, 
        x="content_length_hours",
        y="num_subscribers",
        trendline="ols",
        color="decile",
        hover_data=courses.columns
    )

    fig.update_layout(
        height=600,
        yaxis=dict(range=[0, 1000000])  # Set the initial y-axis range to make the visual less affected by outliers
    )

    # Add an annotation to explain the chart is opened in a focused view
    fig.add_annotation(
        text="<sup>Opened with Zoom below 1M subscribers. Use autoscale to view all data. </sup> ",
        xref="paper", yref="paper",
        x=1, y=1.05,
        showarrow=False,
    )

    fig_html = pio.to_html(fig, full_html=False)
    print("# Finished creating scatter plot of content length")
    return {"title": "Number of Subscribers vs Content length (hours)", "figure": fig_html}

def explode_labels(df):
    # Create a working copy of the dataframe
    courses_exploded_labels = df.copy()

    # Ensure labels are treated as a list (not strings)
    courses_exploded_labels['labels'] = courses_exploded_labels['labels'].apply(literal_eval)

    # Explode the rows (one row per label in course)
    courses_exploded_labels = courses_exploded_labels.explode('labels')

    # Clean up rows with no labels ('No labels')
    courses_exploded_labels['labels'] = courses_exploded_labels['labels'].fillna('No Label')

    # Sort the rows based on label name
    courses_exploded_labels.sort_values(by='labels', ascending=True, inplace=True)

    return courses_exploded_labels

def plot_topn_labels_by_count(courses, n=50):

    courses = explode_labels(courses)

    top50_label_count = (
        courses
        .groupby('labels')['num_subscribers']
        .agg(['min', 'max', 'mean', 'median', 'sum', 'count'])
        .reset_index()
        .sort_values(by='count', ascending=False)
        .head(n)
    )

    fig = px.histogram(
        top50_label_count,
        hover_data=top50_label_count.columns,
        x="labels",
        y="count",
        labels={'labels': 'Label name', 'count': 'Courses'}
    )

    fig.update_xaxes(
        tickvals=top50_label_count['labels'], tickfont=dict(size=10)
    )

    fig.update_layout(
        height=600
    )

    fig_html = pio.to_html(fig, full_html=False)
    print("# Finished creating plot of top N labels by number of courses")
    return {"title": "Top 50 Labels by number of courses", "figure": fig_html}

def plot_topn_labels_by_subscribers(courses, n=50):

    courses = explode_labels(courses)

    top50_label_subscribers = (
        courses
        .groupby('labels')['num_subscribers']
        .agg(['min', 'max', 'mean', 'median', 'sum', 'count'])
        .reset_index()
        .sort_values(by='sum', ascending=False)
        .head(n)
    )

    fig = px.histogram(
        top50_label_subscribers,
        hover_data=top50_label_subscribers.columns,
        x="labels",
        y="sum",
        labels={'labels': 'Label name', 'sum': 'Subscribers'}
    )

    fig.update_xaxes(tickvals=top50_label_subscribers['labels'], tickfont=dict(size=10))

    fig.update_layout(
        height=600
    )

    fig_html = pio.to_html(fig, full_html=False)
    print("# Finished creating plot of top N labels by subscribers")
    return {"title": "Top 50 labels by Number of subscribers", "figure": fig_html}

def instructors_summary_from(df):
    # Create a working copy of the dataframe
    courses_exploded_instructors = df.copy()

    # Ensure instructors are treated as lists not strings
    courses_exploded_instructors['instructors'] = courses_exploded_instructors['instructors'].apply(literal_eval)

    # Explode the courses list with one instructor per row
    courses_exploded_instructors = courses_exploded_instructors.explode('instructors')

    # Organize instructors list for visualization
    instructors_stats_summary = (courses_exploded_instructors.pivot_table(
        index='instructors',  # Group by instructor
        values=['udemy_id', 'num_subscribers'],  # Keep these 2 columns
        aggfunc={
            'udemy_id': 'count', # Count courses
            'num_subscribers': 'sum'  # Sum subscribers
        },
    ))

    # Reorganize columns for visualization
    instructors_stats_summary.reset_index(inplace=True)
    instructors_stats_summary.rename(columns={'udemy_id': 'num_courses'}, inplace=True)

    return instructors_stats_summary

def plot_topn_instructors_by_subscribers(courses, subscribers_threshold=100000):

    instructors_stats_summary = instructors_summary_from(courses)

    # Get instructors with more than 1M subscribers then sort by number of subscribers. 
    instructors_1M_subscribers = (
        instructors_stats_summary[instructors_stats_summary['num_subscribers'] > subscribers_threshold]
        .sort_values(by='num_subscribers', ascending=False) 
    )

    # Chart results
    fig = px.histogram(
        instructors_1M_subscribers,
        hover_data=instructors_1M_subscribers.columns,
        x="instructors",
        y="num_subscribers",
        labels={'instructors': 'Instructor name', 'num_subscribers': 'Number of Subscribers'}
    )
    fig.update_xaxes(tickfont=dict(size=10))
    fig.update_layout(
        height=600
    )

    fig_html = pio.to_html(fig, full_html=False)
    print("# Finished creating plot of top instructors by subscribers count")
    return {"title": f"Instructors with more than {subscribers_threshold} subscribers", "figure": fig_html}

def plot_topn_instructors_by_courses(courses, n=10):

    instructors_stats_summary = instructors_summary_from(courses)
    instructors_stats_summary = (
        instructors_stats_summary
        .sort_values(by='num_courses', ascending=False)
        .head(n)
    )

    fig = px.histogram(
        instructors_stats_summary,
        hover_data=instructors_stats_summary.columns,	
        x="instructors",
        y="num_courses",
        labels={'instructors': 'Instructor name', 'num_courses': 'Courses'}
    )
    fig.update_xaxes(tickfont=dict(size=10))
    fig.update_layout(height=600)

    fig_html = pio.to_html(fig, full_html=False)
    print("# Finished creating plot of top instructors by course count")
    return {"title": "Number of courses created by Instructors with more than 1M subscribers", "figure": fig_html}