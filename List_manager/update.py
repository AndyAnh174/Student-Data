import pandas as pd

def update_student(df):
    sbd = int(input("Nhập SBD của thí sinh cần cập nhật: "))
    year = int(input("Nhập năm thi: "))
    
    # Kiểm tra xem SBD và năm thi có tồn tại không
    student_mask = (df['SBD'] == sbd) & (df['Year'] == year)
    if student_mask.any():
        print("Thí sinh này đã có điểm thi năm", year)
        return df
        
    if sbd in df['SBD'].values:
        if year not in df['Year'].values:
            print("Không tìm thấy thí sinh thi năm", year)
            return df
            
        column = input("Nhập tên cột cần cập nhật (Toan, Van, Ly, ...): ")
        new_value = input("Nhập giá trị mới (hoặc để trống): ")
        new_value = float(new_value) if new_value else 'NaN'
        
        # Cập nhật cả SBD và Year
        df.loc[df['SBD'] == sbd, 'Year'] = year
        df.loc[df['SBD'] == sbd, column] = new_value
        print("Đã cập nhật thông tin thí sinh.")
    else:
        print("Không tìm thấy thí sinh với SBD này.")
    return df
