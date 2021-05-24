// Bar Chart Example
var ctx = document.getElementById("myBarChart");
var myLineChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ["January", "February", "March", "April", "May", "June"],
        datasets: [{
            label: "Frames captured",
            backgroundColor: "#8892CA",
            borderColor: "#111111",
            data: [4215, 5312, 6251, 7841, 9821, 14984],
            barThickness: 40,
        }],
    },
    options: {
        scales: {
            xAxes: [{
                time: {
                    unit: 'month'
                },
                gridLines: {
                    display: false
                },
                ticks: {
                    maxTicksLimit: 6
                }
            }],
            yAxes: [{
                ticks: {
                    min: 0,
                    max: 15000,
                    maxTicksLimit: 5
                },
                gridLines: {
                    display: true
                }
            }],
        },
        legend: {
            display: false
        }
    }
});

// Pie Chart Example
var ctx = document.getElementById("myPieChart");
var myPieChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: ["Blue", "Red", "Yellow", "Green"],
        datasets: [{
            data: [12.21, 15.58, 11.25, 8.32],
            backgroundColor: ['#007bff', '#dc3545', '#ffc107', '#28a745'],
        }],
        aspectratio:0.5,
    },
});
