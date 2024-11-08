import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Load your cleaned data
cleaned_file_path = "Cleaned_Data.csv"
df = pd.read_csv(cleaned_file_path)

# Filter data by years
df_years = {2018: df[df["Year"] == 2018], 2019: df[df["Year"] == 2019]}

# Define score columns
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

# Compute mean scores for each subject by year
mean_scores_2018 = df_years[2018][score_columns].replace(-1, float("nan")).mean()
mean_scores_2019 = df_years[2019][score_columns].replace(-1, float("nan")).mean()
mean_scores = pd.DataFrame({"2018": mean_scores_2018, "2019": mean_scores_2019})

# Create the main Tkinter window
root = tk.Tk()
root.title("Chương trình xử lý dữ liệu")
root.geometry("1200x800")

# Frame for control elements (dropdowns and buttons)
control_frame = tk.Frame(root)
control_frame.pack(pady=10)

# Notebook widget to create tabs
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Frames for Plot and Data Table tabs
plot_frame = tk.Frame(notebook)
data_frame = tk.Frame(notebook)
notebook.add(plot_frame, text="Biểu Đồ")
notebook.add(data_frame, text="Bảng Dữ Liệu")

# Global variables for pagination
current_page = 0
page_size = 50
selected_year = tk.IntVar(value=2018)
selected_chart = tk.StringVar(value="Bar Chart")


# Function to display plots within the Tkinter window
def display_plot(fig):
    for widget in plot_frame.winfo_children():
        widget.destroy()

    # Embed the plot in Tkinter using FigureCanvasTkAgg
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


# Function to clear the plot from the display
def clear_plot():
    for widget in plot_frame.winfo_children():
        widget.destroy()


# Function to generate the selected plot type
def plot_selected_chart():
    chart_type = selected_chart.get()

    try:
        # Font for Vietnamese characters
        plt.rcParams["font.sans-serif"] = ["Arial"]

        if chart_type == "Bar Chart":
            fig, ax = plt.subplots(figsize=(10, 6))
            mean_scores.plot(kind="bar", ax=ax)
            ax.set_title("So sánh điểm trung bình các môn giữa năm 2018 và 2019")
            ax.set_xlabel("Môn học")
            ax.set_ylabel("Điểm trung bình")
            ax.legend(title="Năm")

        elif chart_type == "Box Plot":
            fig, ax = plt.subplots(figsize=(12, 6))
            df_years[selected_year.get()][score_columns].replace(
                -1, float("nan")
            ).boxplot(ax=ax)
            ax.set_title("Biểu đồ hộp cho điểm các môn học")
            ax.set_xlabel("Môn học")
            ax.set_ylabel("Điểm")
            plt.xticks(rotation=45)

        elif chart_type == "Biểu đồ tỉnh 2018":
            fig, ax = plt.subplots(figsize=(15, 6))
            # Count the number of students by province for 2018
            student_count_by_province = df_years[2018]["TenTinh"].value_counts()
            student_count_by_province.plot(kind="bar", color="lightcoral", ax=ax)
            ax.set_title("Số lượng thí sinh tham gia theo tỉnh (Năm 2018)")
            ax.set_xlabel("Tên tỉnh")
            ax.set_ylabel("Số lượng thí sinh")
            plt.xticks(rotation=90)
        elif chart_type == "Biểu đồ tỉnh 2019":
            fig, ax = plt.subplots(figsize=(15, 6))
            # Count the number of students by province for 2018
            student_count_by_province = df_years[2019]["TenTinh"].value_counts()
            student_count_by_province.plot(kind="bar", color="lightcoral", ax=ax)
            ax.set_title("Số lượng thí sinh tham gia theo tỉnh (Năm 2019)")
            ax.set_xlabel("Tên tỉnh")
            ax.set_ylabel("Số lượng thí sinh")
            plt.xticks(rotation=90)

        display_plot(fig)

    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể tạo biểu đồ: {e}")


# Function to display data in a table with pagination
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

    # Navigation buttons
    navigation_frame = tk.Frame(data_frame)
    navigation_frame.pack(pady=10)

    prev_button = tk.Button(
        navigation_frame,
        text="Previous",
        command=lambda: load_page(page - 1) if page > 0 else None,
    )
    prev_button.grid(row=0, column=0, padx=10)

    next_button = tk.Button(
        navigation_frame,
        text="Next",
        command=lambda: (
            load_page(page + 1) if (page + 1) * page_size < len(dataframe) else None
        ),
    )
    next_button.grid(row=0, column=1, padx=10)


# Function to load selected data and reset pagination
def load_data():
    global current_page
    current_page = 0  # Reset to first page
    year = selected_year.get()
    display_data(df_years[year], current_page)
    messagebox.showinfo("Thông báo", f"Đã tải dữ liệu năm {year} thành công!")


# Function to load selected page of data
def load_page(page):
    global current_page
    current_page = page
    year = selected_year.get()
    display_data(df_years[year], current_page)


# Dropdowns and buttons for selecting year, chart type, and actions
year_label = tk.Label(control_frame, text="Năm:")
year_label.grid(row=0, column=0, padx=10, pady=5)

year_dropdown = ttk.Combobox(
    control_frame, textvariable=selected_year, values=[2018, 2019]
)
year_dropdown.grid(row=0, column=1, padx=10, pady=5)

chart_label = tk.Label(control_frame, text="Loại biểu đồ:")
chart_label.grid(row=0, column=2, padx=10, pady=5)

chart_dropdown = ttk.Combobox(
    control_frame,
    textvariable=selected_chart,
    values=["Bar Chart", "Box Plot", "Biểu đồ tỉnh 2018", "Biểu đồ tỉnh 2019"],
)
chart_dropdown.grid(row=0, column=3, padx=10, pady=5)

plot_button = tk.Button(control_frame, text="Vẽ biểu đồ", command=plot_selected_chart)
plot_button.grid(row=0, column=4, padx=10, pady=5)

load_data_button = tk.Button(control_frame, text="Tải dữ liệu", command=load_data)
load_data_button.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

clear_plot_button = tk.Button(control_frame, text="Xóa biểu đồ", command=clear_plot)
clear_plot_button.grid(row=1, column=2, columnspan=2, padx=10, pady=5)

# Run the Tkinter main loop
root.mainloop()
