import pandas as pd

# Load the data
data_df = pd.read_csv('../Data/Data.csv')  # Đường dẫn tới file Data.csv trong thư mục Data
tinh_df = pd.read_csv('../Data/Tinh.csv')  # Đường dẫn tới file Tinh.csv trong thư mục Data

# Merge data based on 'MaTinh'
merged_df = pd.merge(data_df, tinh_df, on='MaTinh', how='left')

# Define block calculations
merged_df['Khoi_A'] = merged_df[['Toan', 'Ly', 'Hoa']].mean(axis=1)
merged_df['Khoi_B'] = merged_df[['Toan', 'Sinh', 'Hoa']].mean(axis=1)
merged_df['Khoi_C'] = merged_df[['Van', 'Lich su', 'Dia ly']].mean(axis=1)
merged_df['Khoi_D'] = merged_df[['Toan', 'Van', 'Ngoai ngu']].mean(axis=1)

# Check if any block has exactly two scores (indicating "Thí Sinh Thi Lại")
merged_df['Thi_Lai'] = (
    (merged_df[['Toan', 'Ly', 'Hoa']].notnull().sum(axis=1) == 2) |
    (merged_df[['Toan', 'Sinh', 'Hoa']].notnull().sum(axis=1) == 2) |
    (merged_df[['Van', 'Lich su', 'Dia ly']].notnull().sum(axis=1) == 2) |
    (merged_df[['Toan', 'Van', 'Ngoai ngu']].notnull().sum(axis=1) == 2)
)

# Determine the best block for students not marked as "Thi Lai"
merged_df['Best_Khoi'] = merged_df[['Khoi_A', 'Khoi_B', 'Khoi_C', 'Khoi_D']].idxmax(axis=1)
merged_df['Best_Khoi'] = merged_df.apply(lambda row: "Thí Sinh Thi Lại" if row['Thi_Lai'] else row['Best_Khoi'], axis=1)

# Select relevant columns for output
block_analysis_final_df = merged_df[['SBD', 'Best_Khoi', 'TenTinh']]

# Export the final result to CSV
block_analysis_final_df.to_csv('../Data/Block_Analysis_Final.csv', index=False)  # Xuất kết quả ra thư mục Data
