var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'bar', // Thay đổi loại biểu đồ tại đây: 'line', 'bar', 'pie', v.v.
    data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [{
            label: '# of Votes',
            data: [12, 19, 3, 5, 2, 3],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                ...
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                ...
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

var myChart = new Chart(ctx, {
    type: 'bar',
    data: {...},
    options: {
        onClick: function(event, elements) {
            if (elements.length > 0) {
                var firstElement = elements[0];
                var label = this.data.labels[firstElement.index];
                var value = this.data.datasets[firstElement.datasetIndex].data[firstElement.index];
                alert('Label: ' + label + '\nValue: ' + value);
            }
        }
    }
});

// Cập nhật dữ liệu
myChart.data.datasets[0].data = [20, 30, 40, 50, 60, 70];

// Vẽ lại biểu đồ
myChart.update();

