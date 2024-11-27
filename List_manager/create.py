import pandas as pd

def create_student(df):
    new_student_data = {
        'SBD': int(input("Nhập SBD: ")),
        'Toan': float(input("Điểm Toán (hoặc để trống): ") or 'NaN'),
        'Van': float(input("Điểm Văn (hoặc để trống): ") or 'NaN'),
        'Ly': float(input("Điểm Lý (hoặc để trống): ") or 'NaN'),
        'Sinh': float(input("Điểm Sinh (hoặc để trống): ") or 'NaN'),
        'Ngoai ngu': float(input("Điểm Ngoại Ngữ (hoặc để trống): ") or 'NaN'),
        'Year': int(input("Năm: ")),
        'Hoa': float(input("Điểm Hóa (hoặc để trống): ") or 'NaN'),
        'Lich su': float(input("Điểm Lịch Sử (hoặc để trống): ") or 'NaN'),
        'Dia ly': float(input("Điểm Địa Lý (hoặc để trống): ") or 'NaN'),
        'GDCD': float(input("Điểm GDCD (hoặc để trống): ") or 'NaN'),
        'MaTinh': int(input("Mã Tỉnh: "))
    }
    filtered_student_data = {k: v for k, v in new_student_data.items() if pd.notnull(v)}
    new_student_df = pd.DataFrame([filtered_student_data])
    df = pd.concat([df, new_student_df], ignore_index=True)
    print("Đã thêm thí sinh mới.")
    return df
