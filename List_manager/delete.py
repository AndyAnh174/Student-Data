def delete_student(df):
    sbd = int(input("Nhập SBD của thí sinh cần xóa: "))
    if sbd in df['SBD'].values:
        df = df[df['SBD'] != sbd]
        print("Đã xóa thí sinh.")
    else:
        print("Không tìm thấy thí sinh với SBD này.")
    return df
