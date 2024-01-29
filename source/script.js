function drawChart() {
    var year = document.getElementById('year').value;
    var quarter = document.getElementById('quarter').value;
    var stockCode = document.getElementById('stockCode').value;

    // Gửi yêu cầu đến server với các thông tin được nhập
    fetch('/draw_chart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({year, quarter, stockCode}),
    })
    .then(response => response.json())
    .then(data => {
        // Hiển thị biểu đồ
        document.getElementById('chartContainer').innerHTML = `<img src="data:image/png;base64,${data.plotUrl}" />`;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
