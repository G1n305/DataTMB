from flask import Flask, request, send_file, make_response
from flask_cors import CORS
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
import pymysql

app = Flask(__name__)
CORS(app)
@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Biểu Đồ Chứng Khoán</title>
    <link rel="stylesheet" type="text/css" href="style.css">
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
    <div class="input-form">
        <label for="year">Năm:</label>
        <!-- Năm -->
<div class="dropdown">
    <button class="dropbtn">Chọn Năm</button>
    <div class="dropdown-content" id="yearDropdown">
        <label><input type="checkbox" value="all" onchange="checkAll(this, 'year')"> All</label>
        <!-- Lặp để tạo các checkboxes cho mỗi năm từ 2009 đến năm hiện tại -->
        <script>
            var currentYear = new Date().getFullYear();
            for (var i = 2009; i <= currentYear; i++) {
                document.write('<label><input type="checkbox" name="year" value="' + i + '"> ' + i + '</label>');
            }
        </script>
    </div>
</div>

        <select id="year" name="year" multiple>
            <option value="all">All</option>
            <!-- Lặp từ 2009 đến năm hiện tại -->
            <script>
                var currentYear = new Date().getFullYear();
                for (var i = 2009; i <= currentYear; i++) {
                    document.write('<option value="' + i + '">' + i + '</option>');
                }
            </script>
        </select>

        <label for="quarter">Quý:</label>
        <!-- Quý -->
<div class="dropdown">
    <button class="dropbtn">Chọn Quý</button>
    <div class="dropdown-content" id="quarterDropdown">
        <label><input type="checkbox" value="all" onchange="checkAll(this, 'quarter')"> All</label>
        <label><input type="checkbox" name="quarter" value="1"> Q1</label>
        <label><input type="checkbox" name="quarter" value="2"> Q2</label>
        <label><input type="checkbox" name="quarter" value="3"> Q3</label>
        <label><input type="checkbox" name="quarter" value="4"> Q4</label>
    </div>
</div>
        <select id="quarter" name="quarter" multiple>
            <option value="all">All</option>
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="4">4</option>
        </select>

        <label for="stockCode">Mã Chứng Khoán:</label>
        <input type="text" id="stockCode" name="stockCode" placeholder="VCB,BID,...">

        <button onclick="drawChart()">Vẽ Biểu Đồ</button>
    </div>

    <div id="chartContainer">
        <!-- Nơi hiển thị biểu đồ -->
        <img id="chartImage" src="" alt="Biểu đồ chứng khoán" style="display: none;" />
    </div>
<script>
    function drawChart() {
        // Lấy tất cả giá trị được chọn từ select box năm và quý
        var yearSelect = document.getElementById('year');
        var quarterSelect = document.getElementById('quarter');
        var years = Array.from(yearSelect.selectedOptions).map(option => option.value);
        var quarters = Array.from(quarterSelect.selectedOptions).map(option => option.value);
        var stockCode = document.getElementById('stockCode').value;
    
        // Kiểm tra nếu lựa chọn là 'all', thì lấy tất cả các giá trị
        years = years.includes('all') ? Array.from(yearSelect.options).filter(option => option.value !== 'all').map(option => option.value) : years;
        quarters = quarters.includes('all') ? [1, 2, 3, 4] : quarters;
    
        fetch('/draw_chart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'year': years,
                'quarter': quarters,
                'stockCode': stockCode
            })
        })
        .then(response => response.blob())
            .then(blob => {
                var url = URL.createObjectURL(blob);
                document.getElementById('chartImage').src = url;
                document.getElementById('chartImage').style.display = 'block';
            })
            return false;
    }
</script>
<script>function checkAll(source, name) {
    checkboxes = document.getElementsByName(name);
    for (var i = 0, n = checkboxes.length; i < n; i++) {
        checkboxes[i].checked = source.checked;
    }
}
</script>
</body>
</html>
    '''

@app.route('/draw_chart', methods=['POST'])
def draw_chart():
    stockCount = request.form['stockCount']
    years = request.form['years']
    quarters = request.form['quarters']
    stockCode = request.form.get('stockCode')

    years = [int(year) for year in years.split(',')]
    quarters = [int(quarter) for quarter in quarters.split(',')]

    connection = pymysql.connect(
        host='localhost',     
        user='root',      
        password='', 
        database='bctc'
    )

    query = f"SELECT * FROM bctc2_txt WHERE nam IN {tuple(years)} AND quy IN {tuple(quarters)};"
    data = pd.read_sql_query(query, connection)
    connection.close()

    data = data.sort_values(by=['nam', 'quy'])
    original_data = data.copy()

    first_column = data.iloc[:, 4]
    second_column = data.iloc[:, 3]
    third_column = data.iloc[:, 5]
    result = (first_column / (second_column + third_column)) * 100
    data['Result'] = result

    if stockCount == '1' or stockCount == '2':
        stock_codes = stockCode.split(',')
        for code in stock_codes:
            data1 = data[data['mack'] == code.strip().upper()]
            plt.plot(data1['nam'].astype(str) + ' Q' + data1['quy'].astype(str), data1['Result'], label=code.strip().upper())
            for i in range(len(data1)):
                plt.text(data1['nam'].iloc[i] + data1['quy'].iloc[i] / 10, data1['Result'].iloc[i], str(round(data1['Result'].iloc[i], 2)))
    elif stockCount == 'QN':
        for code in ['BID', 'VCB', 'CTG', 'ABB']:
            dataX = data[data['mack'] == code]
            plt.plot(dataX['nam'].astype(str) + ' Q' + dataX['quy'].astype(str), dataX['Result'], label=code)
            for i in range(len(dataX)):
                plt.text(dataX['nam'].iloc[i] + dataX['quy'].iloc[i] / 10, dataX['Result'].iloc[i], str(round(dataX['Result'].iloc[i], 2)))
    else:
        return "Lựa chọn không hợp lệ. Vui lòng nhập lại."

    plt.title("Biểu đồ LDR")
    plt.xlabel('Năm và Quý')
    plt.ylabel('Result')
    plt.legend()
    plt.xticks(rotation=45)

    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close()

# Tạo phản hồi và thêm các HTTP headers
    response = make_response(send_file(buf, mimetype='image/png'))
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate' # Cấu hình này không lưu trữ cache
    response.headers['Pragma'] = 'no-cache' # Dành cho HTTP/1.0
    response.headers['Expires'] = '0' # Dành cho proxy servers
    return response
    #return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(port=5500)