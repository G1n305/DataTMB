import pandas as pd
import matplotlib.pyplot as plt
import pymysql

# Hàm tạo kết nối đến cơ sở dữ liệu
def create_connection(host, user, password, database):
    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        print("Kết nối đến cơ sở dữ liệu thành công!")
        return connection

    except pymysql.Error as e:
        print("Không thể kết nối đến cơ sở dữ liệu:")
        print(e)
        return None

# Hàm lấy dữ liệu từ bảng của mỗi database
def get_data_from_database(database, table):
    # Thay thế 'your_connection_string' bằng chuỗi kết nối đến database của bạn
    host = 'localhost'
    user = 'root'
    password = ''
    
    # Tạo kết nối đến database
    connection = create_connection(host, user, password, database)
    if connection is None:
        return None
    
    # Lấy dữ liệu từ bảng
    query = f"SELECT * FROM {table};"
    df = pd.read_sql_query(query, connection)
    
    # Đóng kết nối database
    connection.close()
    
    return df

# Hàm thực hiện phép tính tiengui/voncap1 và vẽ biểu đồ đường
def draw_line_chart(df1, df2, mack_list, nams_quys):
    # Tạo DataFrame để lưu kết quả tính toán và vẽ biểu đồ
    result_df = pd.DataFrame(columns=['mack', 'nam', 'quy', 'TIENGUI/VONCAP1'])
    
    for mack in mack_list:
        for nam_quy in nams_quys:
            nam, quy = nam_quy
            
            # Lấy dữ liệu từ bảng 1 và bảng 2 tương ứng với mã chứng khoán và năm, quý được chọn
            df1_filtered = df1[(df1['mack'] == mack) & (df1['nam'] == nam) & (df1['quy'] == quy)]
            df2_filtered = df2[(df2['mack'] == mack) & (df2['nam'] == nam) & (df2['quy'] == quy)]
            
            # Thực hiện tính toán tiengui/voncap1
            if not df1_filtered.empty and not df2_filtered.empty:
                tiengui = df1_filtered['tienguitainganhangnhanuoc'].iloc[3]  # Giả sử cột tiengui trong bảng 1 là 'TIENGUI'
                voncap1 = df2_filtered['voncap1'].iloc[8]  # Giả sử cột voncap1 trong bảng 2 là 'VONCAP1'
                tiengui_voncap1 = tiengui / voncap1
                
                # Lưu kết quả vào DataFrame
                result_df = result_df.append({'mack': mack, 'nam': nam, 'quy': quy, 'TIENGUI/VONCAP1': tiengui_voncap1}, ignore_index=True)
                
    # Vẽ biểu đồ đường
    for mack in mack_list:
        df_mack = result_df[result_df['mack'] == mack]
        plt.plot(df_mack['nam'].astype(str) + 'Q' + df_mack['quy'].astype(str), df_mack['TIENGUI/VONCAP1'], label=mack)
        #test du lieu dataframe
        print(result_df)
        print(df1_filtered)
        print(df2_filtered)
        print(df1_bctc)
        print(df2_rwa)
    plt.xlabel('Năm và Quý')
    plt.ylabel('Tiengui/Voncap1')
    plt.legend()
    plt.grid()
    plt.show()

# Người dùng nhập các thông tin cần thiết
mack_list = input("Nhập mã chứng khoán (MACK) cần vẽ (các mã cách nhau bằng dấu cách): ").split()
nams_quys = []
num_years_quarters = int(input("Nhập số năm và quý cần lọc: "))
for i in range(num_years_quarters):
    nam_quy = input(f"Năm và Quý {i + 1} (theo định dạng 'năm quý', ví dụ: '2023 1'): ").split()
    nams_quys.append((int(nam_quy[0]), int(nam_quy[1])))

# Gọi hàm để lấy dữ liệu từ database
database_bctc = 'bctc'
table1_bctc = 'testdataup_txt'
df1_bctc = get_data_from_database(database_bctc, table1_bctc)

database_rwa = 'bank_risk_report'
table1_rwa = 'book4cpy_txt'
df2_rwa = get_data_from_database(database_rwa, table1_rwa)

# Gọi hàm để thực hiện tính toán và vẽ biểu đồ đường
draw_line_chart(df1_bctc, df2_rwa, mack_list, nams_quys)
