import pandas as pd
import requests
from io import StringIO
import create
import read
import update
import delete
from datetime import datetime, timedelta
import os
# API URLs
row_data_api = 'https://andyanh.id.vn/index.php/s/p7XMy828G8NKiZp/download'

def fetch_csv_from_api(api_url):

    
    cache_file = 'row_data_cache.csv' if 'p7XMy' in api_url else 'tinh_cache.csv'
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

# Tải dữ liệu
try:
    df = fetch_csv_from_api(row_data_api)
    print("Đã tải dữ liệu thành công từ API")
except Exception as e:
    print(f"Lỗi khi tải dữ liệu từ API: {e}")
    print("Không thể tải dữ liệu. Vui lòng kiểm tra kết nối internet và thử lại.")
    exit()

def show_menu():
    print("\nMenu:")
    print("1. Create (Thêm thí sinh)")
    print("2. Read (Xem thông tin thí sinh)")
    print("3. Update (Cập nhật thông tin thí sinh)")
    print("4. Delete (Xóa thí sinh)")
    print("5. Exit")

def List_manager():
    global df
    while True:
        show_menu()
        choice = input("Chọn thao tác: ")
        if choice == '1':
            df = create.create_student(df)
        elif choice == '2':
            read.read_student(df)
        elif choice == '3':
            df = update.update_student(df)
        elif choice == '4':
            df = delete.delete_student(df)
        elif choice == '5':
            updated_file_path = 'C:/Users/admin/Nextcloud4/andyanh/Data-Project-Student-Manager/Update Data/Updated_Data.csv'  # Đường dẫn tương đối để lưu file cập nhật
            df.to_csv(updated_file_path, index=False)
            print("Đã lưu thay đổi vào Updated_Data.csv và thoát.")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")

# Chạy hàm List_manager khi chạy file main.py trong List_manager
if __name__ == "__main__":
    List_manager()
