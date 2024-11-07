import pandas as pd

# Load the data
data_df = pd.read_csv('../Data/Data.csv')  # Đường dẫn tới file Data.csv trong thư mục Data
tinh_df = pd.read_csv('../Data/Tinh.csv')  # Đường dẫn tới file Tinh.csv trong thư mục Data

# Merge data based on 'MaTinh'
merged_df = pd.merge(data_df, tinh_df, on='MaTinh', how='left')

# Tính tổng điểm của các khối
merged_df['Tong_Diem_Khoi_A'] = merged_df[['Toan', 'Ly', 'Hoa']].sum(axis=1, skipna=False)
merged_df['Tong_Diem_Khoi_B'] = merged_df[['Toan', 'Sinh', 'Hoa']].sum(axis=1, skipna=False)
merged_df['Tong_Diem_Khoi_C'] = merged_df[['Van', 'Lich su', 'Dia ly']].sum(axis=1, skipna=False)
merged_df['Tong_Diem_Khoi_D'] = merged_df[['Toan', 'Van', 'Ngoai ngu']].sum(axis=1, skipna=False)

# Lọc chỉ các cột cần thiết cho kết quả cuối cùng
total_scores_df = merged_df[['SBD', 'Tong_Diem_Khoi_A', 'Tong_Diem_Khoi_B', 'Tong_Diem_Khoi_C', 'Tong_Diem_Khoi_D', 'TenTinh']]

# Xuất kết quả ra file CSV
total_scores_df.to_csv('../Data/Total_Scores.csv', index=False)  # Xuất kết quả ra thư mục Data