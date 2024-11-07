import pandas as pd

# Load the original data
data_df = pd.read_csv('../Data/Data.csv')  # Đường dẫn đến file Data.csv
tinh_df = pd.read_csv('../Data/Tinh.csv')  # Đường dẫn đến file Tinh.csv

# Merge the two datasets on 'MaTinh'
merged_df = pd.merge(data_df, tinh_df, on='MaTinh', how='left')

# Fill missing values in score columns with -1 to indicate missing scores
score_columns = ['Toan', 'Van', 'Ly', 'Sinh', 'Ngoai ngu', 'Hoa', 'Lich su', 'Dia ly', 'GDCD']
merged_df[score_columns] = merged_df[score_columns].fillna(-1)

# Drop rows where essential columns like 'SBD', 'Year', or 'MaTinh' are missing
cleaned_df = merged_df.dropna(subset=['SBD', 'Year', 'MaTinh'])

# Export the cleaned data to CSV
cleaned_df.to_csv('../Data/Cleaned_Data.csv', index=False)  # Đường dẫn đến file Cleaned_Data.csv
