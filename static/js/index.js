
function getServicesOccurrence() {
    $.ajax({
        method: "GET",
        url: '/api/frames/servicesOccurrence',
        success: function (response) {
            serviceBar(response)
        },
        error: function (error) {
            console.log(error);
        }
    });
}


function sum(obj) {
    var sum = 0;
    for (var el in obj) {
        if (obj.hasOwnProperty(el)) {
            sum += parseFloat(obj[el]);
        }
    }
    return sum;
}

// Protocols
function serviceBar(data) {
    services = {}
    $.each(data, function (index) {
        services[data[index].protocolLayerApplicaction] = data[index].occurrence
    })

    delete services["null"]
    
    totalOccurrence = sum(services)
    
    occurrence = []
    for (let i in services) {
        occurrence.push(services[i]*100/totalOccurrence)
    }
    
    var ctx = document.getElementById("chartProtocols");
    var myLineChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(services),
            datasets: [{
                label: "Protocols (%)",
                backgroundColor: "#8892CA",
                borderColor: "#111111",
                data: occurrence,
                barThickness: 40,
            }],
        },
    });
}


// Number of alerts

function getAlertsByTime(){
    $.ajax({
        method: "GET",
        url: '/api/alert_devices/alertsByDate',
        success: function (response) {
            alertsBar(response)
        },
        error: function (error) {
            console.log(error);
        }
    });
}

function alertsBar(data){

    alerts = {}
    $.each(data, function (index) {
        alerts[data[index].date] = data[index].alerts
    })

    occurrence = []
    for (let i in alerts) {
        occurrence.push(alerts[i])
    }

    console.log(data)

    var ctx = document.getElementById("alertsBar");
    var myLineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Object.keys(alerts),
            datasets: [{
                data: occurrence,
                label: "Alerts",
                borderColor: "#8892CA",
                fill: false
            }]
        },
        options: {
            title: {
                display: true,
                text: 'HI'
            },
            scale: {
                ticks: {
                    precision: 0
                }
            }
        }
    });
}


// Pie Chart Example
var ctx = document.getElementById("myPieChart");
var myPieChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ["Unix/Linux", "Windows", "MacOS", "Other"],
        datasets: [
            {
                label: "Population (%)",
                backgroundColor: ["#fcb316", "#16a0fc", "#fc6a49", "#424242"],
                data: [15, 75, 5, 5]
            }
        ]
    },
    options: {
        title: {
            display: true,
            text: 'Predicted world population (millions) in 2050'
        }
    }
});

getServicesOccurrence()
getAlertsByTime()