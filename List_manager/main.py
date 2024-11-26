import pandas as pd
import create
import read
import update
import delete

# Đường dẫn tới file CSV
file_path = 'D:/python-thtp/Data/Data.csv'  # Đường dẫn tương đối từ List_manager tới data
df = pd.read_csv(file_path)

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
            updated_file_path = 'D:/python-thtp/output/Updated_Data.csv'  # Đường dẫn tương đối để lưu file cập nhật
            df.to_csv(updated_file_path, index=False)
            print("Đã lưu thay đổi vào Updated_Data.csv và thoát.")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")

# Chạy hàm List_manager khi chạy file main.py trong List_manager
if __name__ == "__main__":
    List_manager()
