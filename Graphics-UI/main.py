from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from data import df, df_2, df_years, cleaned_file_path
from pandas import DataFrame
import time
import os
import subprocess

# Bắt đầu đo thời gian
start_time = time.time()
root = Tk()
root.title("Chương trình xử lý dữ liệu")
root.geometry("1000x600")
score_columns = [
    "Toan",
    "Van",
    "Ly",
    "Sinh",
    "Ngoai ngu",
    "Hoa",
    "Lich su",
    "Dia ly",
    "GDCD",
]


control_frame = Frame(root)
control_frame.pack(pady=10)

# Widget Notebook để tạo các tab
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)
# Các khung cho tab Biểu Đồ và Bảng Dữ Liệu
plot_frame = Frame(notebook)
data_frame = Frame(notebook)
notebook.add(plot_frame, text="Biểu Đồ")
notebook.add(data_frame, text="Bảng Dữ Liệu")
# Các biến toàn cục cho phân trang
current_page = 0
page_size = 50
selected_year = IntVar(value=2018)
selected_chart = StringVar(value="Bar Chart")

# Khung cho tab Tìm Kiếm
search_frame = Frame(notebook)
notebook.add(search_frame, text="Tìm Kiếm")
# Khung để hiển thị kết quả
result_frame = Frame(search_frame)
result_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=10, sticky="nsew")

# Label kết quả
result_label = Label(result_frame, text="")
result_label.pack(pady=10)

# Biến để lưu kết quả tìm kiếm
result_text = StringVar()
result_label = Label(result_frame, textvariable=result_text)
result_label.pack(pady=10)


# Hàm tìm kiếm theo SBD
def search_by_sbd():
    # Lấy giá trị nhập vào từ ô SBD và năm chọn
    sbd = sbd_entry.get()
    year = selected_year.get()

    # Kiểm tra dữ liệu tồn tại
    if year not in df_years:
        result_label.config(text="Năm không hợp lệ")
        return

    # Lọc dữ liệu theo SBD
    result = df_years[year][df_years[year]["SBD"] == sbd]

    if not result.empty:
        # Hiển thị kết quả
        result_label.config(text=f"Kết quả tìm kiếm cho SBD {sbd}:")

        # Lấy điểm của tất cả các môn thi và lọc bỏ những môn có điểm -1
        points = result.iloc[0][
            [
                "Toan",
                "Van",
                "Ly",
                "Sinh",
                "Ngoai ngu",
                "Hoa",
                "Lich su",
                "Dia ly",
                "GDCD",
            ]
        ].to_dict()

        # Lọc ra những môn có điểm hợp lệ (không phải -1)
        valid_points = {
            subject: points[subject] for subject in points if points[subject] != -1
        }

        # Tạo chuỗi kết quả để hiển thị
        result_text.set(
            f"SBD: {result['SBD'].values[0]} | Tên: {result['TenTinh'].values[0]} | "
            + " | ".join(
                [f"{subject}: {valid_points[subject]}" for subject in valid_points]
            )
        )
    else:
        result_label.config(text=f"Không tìm thấy SBD {sbd} trong năm {year}")


# Thêm giao diện tìm kiếm trong tab "Tìm Kiếm" với grid layout
search_label = Label(search_frame, text="Nhập SBD:")
search_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

sbd_entry = Entry(search_frame)
sbd_entry.grid(row=0, column=1, padx=5, pady=5)

search_button = Button(search_frame, text="Tìm kiếm", command=search_by_sbd)
search_button.grid(row=0, column=2, padx=5, pady=5)


def open_file_explorer():
    try:
        # Lấy thư mục chứa tệp hiện tại
        file_directory = os.path.dirname(
            os.path.abspath(cleaned_file_path)
        )  # Đối với tệp cleaned_data
        # Mở thư mục trong File Explorer (Windows)
        if os.name == "nt":  # Nếu hệ điều hành là Windows
            subprocess.run(["explorer", file_directory])
        elif os.name == "posix":  # Nếu hệ điều hành là macOS hoặc Linux
            subprocess.run(["open", file_directory])  # Dành cho macOS
        messagebox.showinfo("Thông báo", f"Đã mở thư mục chứa tệp: {file_directory}")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể mở thư mục: {e}")


def display_plot(fig):
    for widget in plot_frame.winfo_children():
        widget.destroy()

    # Nhúng biểu đồ vào Tkinter bằng FigureCanvasTkAgg
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


# Hàm để xóa biểu đồ khỏi màn hình
def clear_plot():
    for widget in plot_frame.winfo_children():
        widget.destroy()


# Thêm Combobox chọn môn học vào control_frame
subject_label = Label(control_frame, text="Môn học:")
subject_label.grid(row=0, column=4, padx=10, pady=5)

selected_subject = StringVar(
    value=score_columns[0]
)  # Giá trị mặc định là môn đầu tiên trong danh sách
subject_dropdown = ttk.Combobox(
    control_frame,
    textvariable=selected_subject,
    values=score_columns,
)
subject_dropdown.grid(row=0, column=5, padx=10, pady=5)


# Hàm hiển thị dữ liệu trong bảng với phân trang
def display_data(dataframe, page=0):
    for widget in data_frame.winfo_children():
        widget.destroy()

    start_idx = page * page_size
    end_idx = start_idx + page_size
    data_subset = dataframe.iloc[start_idx:end_idx]

    cols = list(dataframe.columns)
    tree = ttk.Treeview(data_frame, columns=cols, show="headings")

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    for index, row in data_subset.iterrows():
        tree.insert("", "end", values=list(row))

    tree.pack(fill="both", expand=True)

    # Nút điều hướng và số trang
    navigation_frame = Frame(data_frame)
    navigation_frame.pack(pady=10)

    prev_button = Button(
        navigation_frame,
        text="Previous",
        command=lambda: load_page(page - 1) if page > 0 else None,
    )
    prev_button.grid(row=0, column=0, padx=10)

    # Hiển thị số trang
    total_pages = (len(dataframe) + page_size - 1) // page_size
    page_label = Label(
        navigation_frame,
        text=f"Page {page + 1} of {total_pages}",
        font=("Arial", 10),
    )
    page_label.grid(row=0, column=1, padx=10)

    next_button = Button(
        navigation_frame,
        text="Next",
        command=lambda: (
            load_page(page + 1) if (page + 1) * page_size < len(dataframe) else None
        ),
    )
    next_button.grid(row=0, column=2, padx=10)


# Hàm tạo biểu đồ theo loại biểu đồ được chọn
def plot_selected_chart():
    chart_type = selected_chart.get()
    subject = selected_subject.get()  # Lấy môn học được chọn
    try:
        # Thiết lập font cho ký tự tiếng Việt
        plt.rcParams["font.sans-serif"] = ["Arial"]

        if chart_type == "Bar Chart":
            # Tính điểm trung bình cho từng môn theo năm
            mean_scores_2018 = (
                df_years[2018][score_columns].replace(-1, float("nan")).mean()
            )
            mean_scores_2019 = (
                df_years[2019][score_columns].replace(-1, float("nan")).mean()
            )
            mean_scores = DataFrame(
                {"2018": mean_scores_2018, "2019": mean_scores_2019}
            )
            fig, ax = plt.subplots(figsize=(10, 6))
            mean_scores.plot(kind="bar", ax=ax)
            ax.set_title("So sánh điểm trung bình các môn giữa năm 2018 và 2019")
            ax.set_xlabel("Môn học")
            ax.set_ylabel("Điểm trung bình")
            ax.legend(title="Năm")

        elif chart_type == "Biểu đồ thay đổi":
            fig, ax = plt.subplots(figsize=(15, 6))
            mean_scores_by_year = df.groupby("Year")[score_columns].mean()
            mean_scores_by_year.plot(kind="line", marker="o", ax=ax)
            ax.set_title("Biểu đồ thay đổi điểm trung bình")
            ax.set_ylabel("Điểm trung bình")
            ax.legend(title="Môn học")
            plt.xticks(rotation=90)

        elif chart_type == "Phân phối điểm 2018":
            # Vẽ biểu đồ phân phối điểm cho môn học được chọn năm 2018
            fig, ax = plt.subplots(figsize=(8, 5))
            df_years[2018][subject].replace(-1, float("nan")).dropna().hist(
                bins=20, color="skyblue", edgecolor="black", ax=ax
            )
            ax.set_title(f"Phân phối điểm cho môn {subject} (2018)")
            ax.set_xlabel("Điểm")
            ax.set_ylabel("Số lượng thí sinh")

        elif chart_type == "Phân phối điểm 2019":
            # Vẽ biểu đồ phân phối điểm cho môn học được chọn năm 2019
            fig, ax = plt.subplots(figsize=(8, 5))
            df_years[2019][subject].replace(-1, float("nan")).dropna().hist(
                bins=20, color="skyblue", edgecolor="black", ax=ax
            )
            ax.set_title(f"Phân phối điểm cho môn {subject} (2019)")
            ax.set_xlabel("Điểm")
            ax.set_ylabel("Số lượng thí sinh")
        elif chart_type == "Biểu đồ tròn":
            # Labels for the pie chart
            labels = ["Đậu", "Rớt"]

            # df for 2018
            passed_2018 = df_2["Số thí sinh đậu 2018"].sum()
            failed_2018 = df_2["Số thí sinh rớt 2018"].sum()
            values_2018 = [passed_2018, failed_2018]

            # df for 2019
            passed_2019 = df_2["Số thí sinh đậu 2019"].sum()
            failed_2019 = df_2["Số thí sinh rớt 2019"].sum()
            values_2019 = [passed_2019, failed_2019]

            # Plotting
            fig, ax = plt.subplots(1, 2, figsize=(12, 6))

            # 2018 Pie Chart
            ax[0].pie(
                values_2018,
                labels=labels,
                autopct="%1.1f%%",
                startangle=140,
                colors=["#4CAF50", "#F44336"],
            )
            ax[0].set_title("2018 Đậu Rớt")

            # 2019 Pie Chart
            ax[1].pie(
                values_2019,
                labels=labels,
                autopct="%1.1f%%",
                startangle=140,
                colors=["#4CAF50", "#F44336"],
            )
            ax[1].set_title("2019 Đậu Rớt")

        display_plot(fig)

    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể tạo biểu đồ: {e}")


# Hàm tải dữ liệu được chọn và đặt lại phân trang
def load_data():
    global current_page
    current_page = 0  # Đặt lại trang đầu tiên
    year = selected_year.get()
    display_data(df_years[year], current_page)
    messagebox.showinfo("Thông báo", f"Đã tải dữ liệu năm {year} thành công!")


# Hàm tải trang dữ liệu được chọn
def load_page(page):
    global current_page
    current_page = page
    year = selected_year.get()
    display_data(df_years[year], current_page)


# Dropdown và nút để chọn năm, loại biểu đồ, và các thao tác
year_label = Label(control_frame, text="Năm:")
year_label.grid(row=0, column=0, padx=10, pady=5)

year_dropdown = ttk.Combobox(
    control_frame, textvariable=selected_year, values=[2018, 2019]
)
year_dropdown.grid(row=0, column=1, padx=10, pady=5)

chart_label = Label(control_frame, text="Loại biểu đồ:")
chart_label.grid(row=0, column=2, padx=10, pady=5)

chart_dropdown = ttk.Combobox(
    control_frame,
    textvariable=selected_chart,
    values=[
        "Bar Chart",
        "Biểu đồ thay đổi",
        "Phân phối điểm 2018",
        "Phân phối điểm 2019",
        "Biểu đồ tròn",
    ],
)
chart_dropdown.grid(row=0, column=3, padx=10, pady=5)

plot_button = Button(control_frame, text="Vẽ biểu đồ", command=plot_selected_chart)
plot_button.grid(row=0, column=4, padx=10, pady=5)

load_data_button = Button(control_frame, text="Tải dữ liệu", command=load_data)
load_data_button.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

clear_plot_button = Button(control_frame, text="Xóa biểu đồ", command=clear_plot)
clear_plot_button.grid(row=1, column=2, columnspan=2, padx=10, pady=5)


# Hàm thoát ứng dụng
def exit_app():
    # Hỏi xác nhận trước khi thoát
    if messagebox.askokcancel("Thoát ứng dụng", "Bạn có chắc chắn muốn thoát?"):
        root.quit()
        root.destroy()  # Đóng cửa sổ


# Gán sự kiện cho nút "X" đóng cửa sổ
root.protocol("WM_DELETE_WINDOW", exit_app)
# Thêm menu vào ứng dụng
menu_bar = Menu(root)
# Menu File
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Mở tới nơi chứa file", command=open_file_explorer)
file_menu.add_command(label="Thoát", command=exit_app)
menu_bar.add_cascade(label="File", menu=file_menu)
# Menu View
view_menu = Menu(menu_bar, tearoff=0)
view_menu.add_command(label="Hiển thị dữ liệu", command=load_data)
view_menu.add_command(label="Hiển thị biểu đồ", command=plot_selected_chart)
view_menu.add_command(label="Xóa biểu đồ", command=clear_plot)
menu_bar.add_cascade(label="View", menu=view_menu)
# Menu File
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Thoát", command=exit_app)
menu_bar.add_cascade(label="File", menu=file_menu)
# Menu Settings
settings_menu = Menu(menu_bar, tearoff=0)
settings_menu.add_command(
    label="Chọn năm",
    command=lambda: messagebox.showinfo(
        "Chọn năm", "Sử dụng dropdown để chọn năm trong phần điều khiển."
    ),
)
settings_menu.add_command(
    label="Chọn môn học",
    command=lambda: messagebox.showinfo(
        "Chọn môn học", "Sử dụng dropdown để chọn môn học trong phần điều khiển."
    ),
)
settings_menu.add_command(
    label="Chọn loại biểu đồ",
    command=lambda: messagebox.showinfo(
        "Chọn loại biểu đồ",
        "Sử dụng dropdown để chọn kiểu biểu đồ trong phần điều khiển.",
    ),
)
menu_bar.add_cascade(label="Settings", menu=settings_menu)

# Menu Help
help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(
    label="Hướng dẫn",
    command=lambda: messagebox.showinfo(
        "Hướng dẫn",
        "Sử dụng các menu hoặc nút trong giao diện để thực hiện chức năng.",
    ),
)
help_menu.add_command(
    label="Thông tin phiên bản",
    command=lambda: messagebox.showinfo("Phiên bản", "Chương trình xử lý dữ liệu v1.0"),
)
menu_bar.add_cascade(label="Help", menu=help_menu)

# Gán thanh menu vào cửa sổ chính
root.config(menu=menu_bar)
# Đo thời gian kết thúc
end_time = time.time()

elapsed_time = end_time - start_time
print(f"Thời gian khởi động: {elapsed_time:.2f} giây.")

root.mainloop()
