import pandas as pd

# Load the data
import requests
from io import StringIO

data_api = 'https://andyanh.id.vn/index.php/s/p7XMy828G8NKiZp/download'
tinh_api = 'https://andyanh.id.vn/index.php/s/zbHTAjksBekNB4M/download'

def fetch_csv_from_api(api_url):
    from datetime import datetime, timedelta
    import os
    
    cache_file = 'data_cache.csv' if 'p7XMy' in api_url else 'tinh_cache.csv'
    cache_timeout = timedelta(hours=24)
    
    if os.path.exists(cache_file):
        modified_time = datetime.fromtimestamp(os.path.getmtime(cache_file))
        if datetime.now() - modified_time < cache_timeout:
            print(f"Đang tải dữ liệu từ cache {cache_file}...")
            return pd.read_csv(cache_file)
    
    print(f"Đang tải dữ liệu từ API {api_url}...")
    response = requests.get(api_url)
    if response.status_code == 200:
        df = pd.read_csv(StringIO(response.text))
        df.to_csv(cache_file, index=False)
        return df
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

# Tải dữ liệu từ API
try:
    data_df = fetch_csv_from_api(data_api)
    tinh_df = fetch_csv_from_api(tinh_api)
    print("Đã tải dữ liệu thành công từ API")
except Exception as e:
    print(f"Lỗi khi tải dữ liệu từ API: {e}")
    print("Không thể tải dữ liệu. Vui lòng kiểm tra kết nối internet và thử lại.")
    exit()

# Merge data based on 'MaTinh'
merged_df = pd.merge(data_df, tinh_df, on='MaTinh', how='left')

# Thêm cột "Năm" dựa trên logic từ dữ liệu
merged_df['Nam'] = merged_df['SBD'].astype(str).apply(
    lambda x: 2018 if "18" in x else (2019 if "19" in x else None)  # Điều chỉnh logic tùy thuộc vào dữ liệu thực tế
)

# Chỉ giữ lại các hàng có "Năm" là 2018 hoặc 2019
merged_df = merged_df[merged_df['Nam'].isin([2018, 2019])]

# Tính tổng điểm của các khối
merged_df['Tong_Diem_Khoi_A'] = merged_df[['Toan', 'Ly', 'Hoa']].sum(axis=1, skipna=False)
merged_df['Tong_Diem_Khoi_B'] = merged_df[['Toan', 'Sinh', 'Hoa']].sum(axis=1, skipna=False)
merged_df['Tong_Diem_Khoi_C'] = merged_df[['Van', 'Lich su', 'Dia ly']].sum(axis=1, skipna=False)
merged_df['Tong_Diem_Khoi_D'] = merged_df[['Toan', 'Van', 'Ngoai ngu']].sum(axis=1, skipna=False)

# Loại bỏ các thí sinh không có kết quả thi bất kỳ khối nào (tất cả tổng điểm khối đều NaN hoặc 0)
merged_df = merged_df[
    (merged_df['Tong_Diem_Khoi_A'] > 0) |
    (merged_df['Tong_Diem_Khoi_B'] > 0) |
    (merged_df['Tong_Diem_Khoi_C'] > 0) |
    (merged_df['Tong_Diem_Khoi_D'] > 0)
]

# Sắp xếp dữ liệu theo thứ tự năm (2018 trước, 2019 sau)
merged_df = merged_df.sort_values(by='Nam')

# Lọc chỉ các cột cần thiết cho kết quả cuối cùng
total_scores_df = round(merged_df[['SBD', 'Tong_Diem_Khoi_A', 'Tong_Diem_Khoi_B', 'Tong_Diem_Khoi_C', 'Tong_Diem_Khoi_D', 'TenTinh', 'Nam']], 2)

# Xuất kết quả ra file CSV
total_scores_df.to_csv('Total_Scores_2018_2019.csv', index=False)
