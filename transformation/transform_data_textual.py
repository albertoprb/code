import pandas as pd
import os
from bs4 import BeautifulSoup

data_folder_path = os.path.join(os.path.dirname(__file__), "../data/")
json_file_path = os.path.normpath(data_folder_path + "courses_udemy_raw.json")

print("Reading JSON input")
df = pd.read_json(json_file_path)


"""
Changing ID column name
"""


# Setting the primary key clearly
print("Renaming id column to udemy_id")
df = df.rename(columns={"id": "udemy_id"})


"""
Selecting only textual columns from the dataframe
"""


print("Extracting full text fields")
df_text = df[
    [
        "udemy_id",
        "title",
        "url",
        "description",
        "headline",
        "image",
        "requirements_data",
        "what_you_will_learn_data",
        "target_audiences",
        "objectives",
    ]
]


"""
Transforming description field
"""

print("Converting description from HTML to text")


# Convertor description from HTML to text
def html_to_string(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()


df_text.loc[:, 'description'] = df_text["description"].apply(html_to_string)


"""
Exporting results to CSV
"""


print("Exporting csv files to data folder")

courses_text_csv = "courses_text_data"

df_text.to_csv(data_folder_path + courses_text_csv + ".csv", index=False)

print("Exporting 10% samples to data folder")
shuffled_df_text = df_text.sample(frac=1)  # Shuffle total set
shuffled_df_text = df_text.sample(frac=0.1)  # 10% sample
shuffled_df_text.to_csv(
    data_folder_path + courses_text_csv + "_sample.csv", index=False
)
