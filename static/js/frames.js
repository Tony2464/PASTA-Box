
$(document).ready(function () {
    //Table search
    $("#myInput").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("#myTable tr").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
    //Checkbox
    $("#checkIP").change(function () {
        if (this.checked) {
            $("#groupIP").hide()
        } else {
            $("#groupIP").show()
        }
    });
    $("#checkPort").change(function () {
        if (this.checked) {
            $("#groupPort").hide()
        } else {
            $("#groupPort").show()
        }
    });
});

function ajaxGetFrame() {
    // Check if value is empty
    if ($('#limit').val() === "") {
        return 0
    }

    // Get all params
    params = {}

    if ($('#limit').val() != "") {
        params["limit"] = $('#limit').val()
    }

    if ($('#startDate').val() != "") {
        params["startDate"] = $('#startDate').val()
    }

    if ($('#endDate').val() != "") {
        params["endDate"] = $('#endDate').val()
    }

    if ($('#domain').val() != "") {
        params["domain"] = $('#domain').val()
    }

    if ($('#info').val() != "") {
        params["info"] = $('#info').val()
    }

    if ($('#application').val() != "") {
        params["application"] = $('#application').val()
    }

    if ($('#transport').val() != "") {
        params["transport"] = $('#transport').val()
    }

    if ($('#network').val() != "") {
        params["network"] = $('#network').val()
    }

    // Both IP (OR)
    if ($('.collapseIPboth').attr('class') == "collapseIPboth collapse show") {
        if ($('#ipSourceAndDest').val() != "") {
            params["ipSourceAndDest"] = $('#ipSourceAndDest').val()
        }
    } else {
        //IP Source and Dest (AND)
        if ($('#ipSource').val() != "") {
            params["ipSource"] = $('#ipSource').val()
        }
        if ($('#ipDest').val() != "") {
            params["ipDest"] = $('#ipDest').val()
        }
    }

    // Both Port (OR)
    if ($('.collapsePortBoth').attr('class') == "collapsePortBoth collapse show") {
        if ($('#portSourceAndDest').val() != "") {
            params["portSourceAndDest"] = $('#portSourceAndDest').val()
        }
    } else {
        // Port Source and Dest (AND)
        if ($('#portSource').val() != "") {
            params["portSource"] = $('#portSource').val()
        }
        if ($('#portDest').val() != "") {
            params["portDest"] = $('#portDest').val()
        }
    }

    // Both MAC (OR)
    if ($('.collapseMacBoth').attr('class') == "collapseMacBoth collapse show") {
        if ($('#macSourceAndDest').val() != "") {
            params["macSourceAndDest"] = $('#macSourceAndDest').val()
        }
    } else {
        // MAC Source and Dest (AND)
        if ($('#macAddrSource').val() != "") {
            params["macAddrSource"] = $('#macAddrSource').val()
        }
        if ($('#macAddrDest').val() != "") {
            params["macAddrDest"] = $('#macAddrDest').val()
        }
    }

    //console.log(params)

    $.ajax({
        method: "GET",
        url: '/api/frames',
        data: params,
        success: function (response) {
            $('#myTable').empty();
            $.each(response, function (index) {
                $('#myTable').append(
                    '<tr>' +
                    '<td>' + response[index].ipSource + '</td>' +
                    '<td>' + response[index].ipDest + '</td>' +
                    '<td>' + response[index].portSource + '</td>' +
                    '<td>' + response[index].portDest + '</td>' +
                    '<td>' + response[index].macAddrSource + '</td>' +
                    '<td>' + response[index].macAddrDest + '</td>' +
                    '<td>' + response[index].protocolLayerApplication + '</td>' +
                    '<td>' + formatToString(response[index].protocolLayerTransport) + '</td>' +
                    '<td>' + response[index].protocolLayerNetwork + '</td>' +
                    '<td>' + response[index].domain + '</td>' +
                    '<td>' + response[index].date + '</td>' +
                    '<td>' + response[index].info + '</td>' +
                    '</tr>'
                )
            });
        },
        error: function (error) {
            console.log(error);
        }
    });
}

// Transform IP protocol numbers into actual names
function formatToString(number) {
    switch (number) {
        case '1':
            return "ICMP"
        case '6':
            return "TCP"
        case '17':
            return "UDP"
            break;
        case '27':
            return "RDP"
            break;
        case '41':
            return "IPv6"
            break;
        case '6':
            return "EIGRP"
            break;
        case '89':
            return "OSPF"
            break;
        case '143':
            return "Ethernet"
            break;
        default:
            return number
    }
}

$(document).ready(function () {
    ajaxGetFrame();
    //Ajax request
    $('.inputs').on('input', function (event) {
        ajaxGetFrame();
    });
});