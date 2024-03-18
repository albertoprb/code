import pandas as pd
import os

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
Dropping all columns that have no meaningful distinctive values
"""


# Drop columns that have no meaningful distinctive values
print("Dropping is_paid and has_certificate given >95% non-unique data")
df = df.drop(columns=["is_paid"])
df = df.drop(columns=["has_certificate"])

# Dropping all textual columns
df = df.drop(
    columns=[
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
)


"""
Extract price from JSON
"""


print("Transforming price to keep only amount and currency")
df_price_detail = pd.json_normalize(df["price_detail"]).reset_index(drop=True)
df["price"] = df_price_detail["amount"]
df["currency"] = df_price_detail["currency"]
df = df.drop(columns=["price_detail"])


"""
Adjust course content duration columns
"""


print("Transforming duration to keep only numbers")
df["content_info"] = df["content_info"].str.replace(
    "total hours?", "", case=False, regex=True
)
df["content_info"] = df["content_info"].str.replace(
    "total mins?", "", case=False, regex=True
)
# Find all content_info column values with 'questions' inside the string with 0
df.loc[
    df["content_info"].str.contains("questions?", case=False, na=False, regex=True),
    "content_info",
] = 0

df = df.rename(columns={"content_info": "content_length_hours"})
df = df.rename(columns={"estimated_content_length": "content_length_minutes"})


"""
Tranforming instructors
"""

print("Transforming instructors to keep only names")


def keep_only_instructor_name(instructors):
    instructor_names = []
    for instructor in instructors:
        instructor_names.append(
            instructor["title"]
        )  # Create a list of instructor names
    return instructor_names


df["visible_instructors"] = df["visible_instructors"].apply(
    keep_only_instructor_name
)
df = df.rename(columns={"visible_instructors": "instructors"})


"""
Transforming labels
"""

print("Transforming labels")


def keep_only_label_title(labels):
    label_titles = []
    for label in labels:
        label_titles.append(label["title"])
    return label_titles


df["labels"] = df["labels"].apply(keep_only_label_title)


"""
Transforming locales to keep only locale title
"""

print("Flattening locales")
# Using only the title of locale as reference
df_locale = pd.json_normalize(df["locale"]).reset_index(drop=True)["title"]
# Assigning the locale the processed value
df["locale"] = df_locale


"""
Transforming categories to keep only category title
"""

print("Transforming categories")
# Using title for the categories
df_primary_category = pd.json_normalize(
    df["primary_category"]
).reset_index(drop=True)["title"]
df_primary_subcategory = pd.json_normalize(
    df["primary_subcategory"]
).reset_index(drop=True)["title"]

# Assigning the categories to the processed values
df["primary_category"] = df_primary_category
df["primary_subcategory"] = df_primary_subcategory
df = df.rename(columns={"primary_category": "category"})
df = df.rename(columns={"primary_subcategory": "subcategory"})


"""
Flattening course features
"""

print("Flattening course features disabled as >99% of features are True")
# features = pd.json_normalize(df['features']).reset_index(drop=True)
# df2 = pd.concat([df,features], axis=1)
print("--- Dropping features column")
df = df.drop(columns=["features"])



"""
Creating discounted prices
Udemy offers a 80% discount for new users and regular discounts
Therefore, I'll normalize the price
"""


print("Creating discounting prices and dropping discount columns")

discount = 0.82  # 82% discount
df['price_discounted'] = (df['price'] * (1-discount))
# rounding price discounted to 2 decimal digits
df['price_discounted'] = df['price_discounted'].apply(
    lambda x: '{:.2f}'.format(x)
)

# dropping discount and discount_price columns
df = df.drop(columns=['discount', 'discount_price'])

"""
Exporting results to CSV
"""

print("Exporting csv files to data folder")

courses_numerical_categorical_csv = "courses_numerical_categorical_data"

df.to_csv(
    data_folder_path + courses_numerical_categorical_csv + ".csv",
    index=False
)

print("Exporting 10% samples to data folder")
shuffled_df = df.sample(frac=1)  # Shuffle total set
shuffled_df = shuffled_df.sample(frac=0.1)  # 10% sample
shuffled_df.to_csv(
    data_folder_path + courses_numerical_categorical_csv + "_sample.csv",
    index=False
)
