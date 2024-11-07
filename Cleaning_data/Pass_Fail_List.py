import pandas as pd

# Load data
data_df = pd.read_csv('../Data/Data.csv')  # Đường dẫn đến Data.csv trong thư mục Data
tinh_df = pd.read_csv('../Data/Tinh.csv')  # Đường dẫn đến Tinh.csv trong thư mục Data

# Merge data based on 'MaTinh'
merged_df = pd.merge(data_df, tinh_df, on='MaTinh', how='left')

# Calculate the total score across all subjects for each student
merged_df['Total_Score'] = merged_df[['Toan', 'Van', 'Ly', 'Sinh', 'Ngoai ngu', 'Hoa', 'Lich su', 'Dia ly', 'GDCD']].sum(axis=1, skipna=True)

# Count the number of subjects each student has taken
merged_df['Subjects_Taken'] = merged_df[['Toan', 'Van', 'Ly', 'Sinh', 'Ngoai ngu', 'Hoa', 'Lich su', 'Dia ly', 'GDCD']].notnull().sum(axis=1)

# Label students with 3 or fewer subjects as "Thí sinh thi lại"
merged_df['Ket_Qua'] = merged_df['Subjects_Taken'].apply(lambda x: "Thí sinh thi lại" if x <= 3 else None)

# Determine pass/fail for students with more than 3 subjects
# Assuming a passing score threshold (e.g., 15)
passing_score = 15
merged_df['Ket_Qua'] = merged_df.apply(
    lambda row: "Đậu" if row['Total_Score'] >= passing_score and row['Ket_Qua'] is None else 
                ("Rớt" if row['Ket_Qua'] is None else row['Ket_Qua']),
    axis=1
)

# Select relevant columns for the final output
result_df = merged_df[['SBD', 'Total_Score', 'Subjects_Taken', 'Ket_Qua', 'TenTinh']]

# Export to CSV
result_df.to_csv('../Data/Pass_Fail_List.csv', index=False)  # Kết quả được xuất vào thư mục Data
