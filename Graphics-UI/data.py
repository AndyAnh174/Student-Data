import pandas as pd
import requests
from io import StringIO
from datetime import datetime, timedelta
import os

# Đường dẫn files
cleaned_file_path = "https://andyanh.id.vn/index.php/s/psPTAMbDrzzMnWk/download"
Summary_Result_By_Year = "https://andyanh.id.vn/index.php/s/49ZJgJxeMe5GfSA/download"


def fetch_csv_from_api(api_url, cache_name):
    cache_file = f"{cache_name}_cache.csv"
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
        raise Exception(f"Không thể tải dữ liệu: {response.status_code}")


# Tải dữ liệu với cache
try:
    df = fetch_csv_from_api(cleaned_file_path, "cleaned_data")
    df_2 = fetch_csv_from_api(Summary_Result_By_Year, "summary_data")
    print("Đã tải dữ liệu thành công")

    # Lọc dữ liệu theo năm
    df_years = {2018: df[df["Year"] == 2018], 2019: df[df["Year"] == 2019]}

except Exception as e:
    print(f"Lỗi khi tải dữ liệu: {e}")
    print("Không thể tải dữ liệu. Vui lòng kiểm tra kết nối internet và thử lại.")
    exit()
cached = "cleaned_data_cache.csv"
