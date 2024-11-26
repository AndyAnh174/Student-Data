import pandas as pd

# Tải dữ liệu đã làm sạch
cleaned_file_path = "Cleaned_Data.csv"
Summary_Result_By_Year = "Summary_Result_By_Year.csv"
# Lọc dữ liệu theo năm
df = pd.read_csv(cleaned_file_path)
df_years = {2018: df[df["Year"] == 2018], 2019: df[df["Year"] == 2019]}
df_2 = pd.read_csv(Summary_Result_By_Year)
