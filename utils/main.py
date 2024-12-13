import pandas as pd
from data_cleaning import *
from data_inspection import *
from helpers import *

# Load your data into a DataFrame
df = pd.read_csv("your_data.csv")

# Perform data cleaning steps
df = remove_duplicates(df)
df, removed_rows = drop_empty_rows(df)

# Show some basic data inspection results
show_basic_info(df)

# Continue with further operations if needed