import pandas as pd

def update_student(df):
    sbd = int(input("Nhập SBD của thí sinh cần cập nhật: "))
    if sbd in df['SBD'].values:
        column = input("Nhập tên cột cần cập nhật (Toan, Van, Ly, ...): ")
        new_value = input("Nhập giá trị mới (hoặc để trống): ")
        new_value = float(new_value) if new_value else 'NaN'
        df.loc[df['SBD'] == sbd, column] = new_value
        print("Đã cập nhật thông tin thí sinh.")
    else:
        print("Không tìm thấy thí sinh với SBD này.")
    return df
