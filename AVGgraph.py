import pandas as pd
import matplotlib.pyplot as plt
import pymysql

def divide_columns(excel_file):
    # Kết nối đến cơ sở dữ liệu SQL
    connection = pymysql.connect(
        host='localhost',     
        user='root',      
        password='', 
        database='bctc' 
    )

    # Nhận dữ liệu từ bàn phím
    choice = input("Nhập số lượng mã chứng khoán (1, 2 hoặc 3): ")
    years = input("Nhập các năm cần lọc, cách nhau bởi dấu phẩy: ")
    quarters = input("Nhập các quý cần lọc, cách nhau bởi dấu phẩy: ")

    # Chuyển đổi chuỗi years thành danh sách các năm
    years = [int(year) for year in years.split(',')]

    # Chuyển đổi chuỗi quarters thành danh sách các quý
    quarters = [int(quarter) for quarter in quarters.split(',')]

    # Truy vấn SQL để lấy dữ liệu từ cơ sở dữ liệu
    query = f"SELECT * FROM testdataup_txt WHERE nam IN {tuple(years)} AND quy IN {tuple(quarters)};"

    # Đọc dữ liệu từ SQL vào DataFrame
    data = pd.read_sql_query(query, connection)

    # Đóng kết nối sau khi lấy dữ liệu
    connection.close()

    # Sắp xếp dữ liệu theo năm và quý theo thứ tự tăng dần
    data = data.sort_values(by=['nam', 'quy'])

    # Tạo một bản sao của dữ liệu gốc
    original_data = data.copy()

    # Lấy dữ liệu từ cột thứ nhất và cột thứ hai
    first_column = data.iloc[:, 3]
    second_column = data.iloc[:, 4]
    third_column = data.iloc[:, 5]

    # Thực hiện phép chia giữa dữ liệu của cột thứ nhất và cột thứ hai
    result = (first_column / (second_column + third_column)) * 100

    # Thêm cột kết quả vào DataFrame
    data['Result'] = result

    if choice == '1':
        # Nhận mã chứng khoán từ bàn phím
        stock_code = input("Nhập mã chứng khoán: ")

        # Lọc dữ liệu theo điều kiện cho mã chứng khoán đã chọn
        data1 = data[data['mack'] == stock_code]

        # Vẽ biểu đồ cho mã chứng khoán đã chọn
        plt.plot(data1['nam'].astype(str) + ' Q' + data1['quy'].astype(str), data1['Result'], label=stock_code)

        # Hiển thị giá trị tại các đỉnh của đồ thị
        for i in range(len(data1)):
            plt.text(data1['nam'].iloc[i] + data1['quy'].iloc[i] / 10, data1['Result'].iloc[i], str(round(data1['Result'].iloc[i], 2)))

    elif choice == '2':
        # Nhận 2 mã chứng khoán từ bàn phím
        stock_code1 = input("Nhập mã chứng khoán thứ nhất: ")
        stock_code2 = input("Nhập mã chứng khoán thứ hai: ")

        # Lọc dữ liệu theo điều kiện cho mã chứng khoán thứ nhất
        data1 = data[data['mack'] == stock_code1]

        # Vẽ biểu đồ cho mã chứng khoán thứ nhất
        plt.plot(data1['nam'].astype(str) + ' Q' + data1['quy'].astype(str), data1['Result'], label=stock_code1)

        # Lọc dữ liệu theo điều kiện cho mã chứng khoán thứ hai
        data2 = data[data['mack'] == stock_code2]

        # Vẽ biểu đồ cho mã chứng khoán thứ hai
        plt.plot(data2['nam'].astype(str) + ' Q' + data2['quy'].astype(str), data2['Result'], label=stock_code2)

        # Hiển thị giá trị tại các đỉnh của đồ thị cho mã chứng khoán thứ nhất
        for i in range(len(data1)):
            plt.text(data1['nam'].iloc[i] + data1['quy'].iloc[i] / 10, data1['Result'].iloc[i], str(round(data1['Result'].iloc[i], 2)))

        # Hiển thị giá trị tại các đỉnh của đồ thị cho mã chứng khoán thứ hai
        for i in range(len(data2)):
            plt.text(data2['nam'].iloc[i] + data2['quy'].iloc[i] / 10, data2['Result'].iloc[i], str(round(data2['Result'].iloc[i], 2)))

    elif choice == '3':
        # Nhận 2 mã chứng khoán từ bàn phím
        stock_code1 = input("Nhập mã chứng khoán thứ nhất: ")
        stock_code2 = input("Nhập mã chứng khoán thứ hai: ")

        # Lọc dữ liệu theo điều kiện cho mã chứng khoán thứ nhất
        data1 = data[data['mack'] == stock_code1]

        # Lọc dữ liệu theo điều kiện cho mã chứng khoán thứ hai
        data2 = data[data['mack'] == stock_code2]

        # Vẽ biểu đồ cho mã chứng khoán thứ nhất
        plt.plot(data1['nam'].astype(str) + ' Q' + data1['quy'].astype(str), data1['Result'], label=stock_code1)

        # Vẽ biểu đồ cho mã chứng khoán thứ hai
        plt.plot(data2['nam'].astype(str) + ' Q' + data2['quy'].astype(str), data2['Result'], label=stock_code2)

        # Tính đường trung bình của kết quả 2 mã chứng khoán đã chọn
        avg_result = (data1['Result'] + data2['Result']) / 2

        # Vẽ đường trung bình
        plt.plot(data1['nam'].astype(str) + ' Q' + data1['quy'].astype(str), avg_result, label='Đường trung bình', linestyle='dashed')

        # Hiển thị giá trị tại các đỉnh của đồ thị cho mã chứng khoán thứ nhất
        for i in range(len(data1)):
            plt.text(data1['nam'].iloc[i] + data1['quy'].iloc[i] / 10, data1['Result'].iloc[i], str(round(data1['Result'].iloc[i], 2)))

        # Hiển thị giá trị tại các đỉnh của đồ thị cho mã chứng khoán thứ hai
        for i in range(len(data2)):
            plt.text(data2['nam'].iloc[i] + data2['quy'].iloc[i] / 10, data2['Result'].iloc[i], str(round(data2['Result'].iloc[i], 2)))

        # Hiển thị giá trị tại các điểm của đường trung bình
        for i in range(len(avg_result)):
            plt.text(data1['nam'].iloc[i] + data1['quy'].iloc[i] / 10, avg_result.iloc[i], str(round(avg_result.iloc[i], 2)))

    else:
        print("Lựa chọn không hợp lệ. Vui lòng nhập lại.")

    # Đặt tên và hiển thị biểu đồ
    plt.title("Biểu đồ Tiền gửi NHNN/Tổng tài sản theo năm và quý")
    plt.xlabel('Năm và Quý')
    plt.ylabel('Tiền gửi NHNN/Tổng tài sản (%)')
    plt.legend()
    plt.xticks(rotation=45)  # Để trục x hiển thị dễ đọc hơn
    plt.show()

    # Trả về dữ liệu gốc
    return original_data

# Sử dụng hàm divide_columns với tên tệp excel của bạn
original_data = divide_columns('tiengui.xlsx')
