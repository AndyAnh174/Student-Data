# PHÂN TÍCH ĐIỂM THI THPT CỦA HỌC SINH TRÊN TOÀN NƯỚC GIỮA NĂM 2018 VÀ 2019

Dự án này là một hệ thống quản lý và phân tích dữ liệu sinh viên. Nó bao gồm các chức năng như làm sạch dữ liệu, quản lý danh sách sinh viên, chuẩn hóa dữ liệu, và hiển thị biểu đồ.

## 📁 Cấu trúc thư mục

- **📈 Chart**
  - `chart.ipynb`: Notebook để tạo và hiển thị biểu đồ từ dữ liệu sinh viên.

- **🧹 Cleaning_data**
  - `cleaner.py`: Mã nguồn để làm sạch dữ liệu, loại bỏ các giá trị không hợp lệ.
  - `config.py`: Cấu hình cho quá trình làm sạch dữ liệu.
  - `main.py`: Tập tin chính để chạy các chức năng làm sạch dữ liệu.

- **🖥️ Graphics-UI**
  - `add.py`: Thêm dữ liệu sinh viên qua giao diện đồ họa.
  - `data.py`: Quản lý và hiển thị dữ liệu.
  - `delete.py`: Xóa dữ liệu sinh viên qua giao diện đồ họa.
  - `main.py`: Tập tin chính cho giao diện đồ họa.
  - `update.py`: Cập nhật dữ liệu sinh viên qua giao diện đồ họa.

- **📋 List_manager**
  - `create.py`: Tạo danh sách sinh viên mới.
  - `delete.py`: Xóa danh sách sinh viên.
  - `main.py`: Tập tin chính để quản lý danh sách.
  - `read.py`: Đọc dữ liệu từ danh sách sinh viên.
  - `update.py`: Cập nhật danh sách sinh viên.

- **📊 Standardization**
  - `data_struct_block.ipynb`: Notebook về cấu trúc dữ liệu của từng khối.
  - `pass_or_fail.ipynb`: Xác định sinh viên đậu hay rớt dựa trên điểm số.
  - `score_distribution.ipynb`: Phân tích phân phối điểm số của sinh viên.
  - `sum_all_block.ipynb`: Tổng hợp dữ liệu từ tất cả các khối.
  - `sum_pass_fail.ipynb`: Tổng hợp dữ liệu sinh viên đậu/rớt.

## 📄 Tập tin khác

- `.gitignore`: Các tập tin và thư mục bị bỏ qua bởi Git.
- `Data.zip`: Tập tin nén chứa dữ liệu thô.
- `history.csv`: Lịch sử dữ liệu sinh viên.
- `main.ipynb`: Notebook chính cho dự án.

## 🌐 Tải dữ liệu

Dữ liệu Dataset được tải về từ link: [Datasetv](https://andyanh.id.vn/index.php/s/R87b2JJT96ZiysQ). 
Trong các file đều chứa link API Curl để tải dữ liệu.

## 👥 Thành viên nhóm

- Hồ Việt Anh (Nhóm trưởng) - 23133002
- Nguyễn Đặng Quốc Anh - 23133004
- Trần Minh Khánh - 23133060
- Lưu Chí Đan - 23133014
- Phạm Minh Quân - 23133060

## 🚀 Hướng dẫn sử dụng

1. **Cài đặt**: Clone repository và cài đặt các thư viện cần thiết.
2. **Chạy dự án**: Sử dụng các tập tin `main.py` trong từng thư mục để thực hiện các chức năng tương ứng.
3. **Phân tích dữ liệu**: Sử dụng các notebook trong thư mục `Standardization` để phân tích dữ liệu.

## 🤝 Đóng góp

Nếu nhóm mình có sai sót gì, mong các bạn góp ý để nhóm mình có thể hoàn thiện hơn.
