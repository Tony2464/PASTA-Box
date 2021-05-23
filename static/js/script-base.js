/*!
    * Start Bootstrap - SB Admin v6.0.2 (https://startbootstrap.com/template/sb-admin)
    * Copyright 2013-2020 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-sb-admin/blob/master/LICENSE)
    */
(function ($) {
    "use strict";

    // Add active state to sidbar nav links
    var path = window.location.href; // because the 'href' property of the DOM element is the absolute path
    $("#layoutSidenav_nav .sb-sidenav a.nav-link").each(function () {
        if (this.href === path) {
            $(this).addClass("active");
        }
    });

    // Toggle the side navigation
    $("#sidebarToggle").on("click", function (e) {
        e.preventDefault();
        $("body").toggleClass("sb-sidenav-toggled");
    });
})(jQuery);

$(document).ready(function () {
    getSysInfo()
    window.setInterval(function () {
        /// call your function here
        getSysInfo()
    }, 1500);
});

function getSysInfo() {
    $.ajax({
        method: "GET",
        url: '/api/system/info',
        success: function (response) {
            totalCpu = response["totalCpu"]
            totalMemPercent = response["totalMemPercent"]
            totalMem = response["totalMem"]
            usedMem = response["usedMem"]
            hostname = response["hostname"]

            // $('#totalCpu').append(
            //     '<div style="width:100px" class="text-left">' + response["totalCpu"] + ' %</div>'
            // )

            // CPU Bar
            $('#totalCpu').empty();
            $('#totalCpuText').empty();
            $('#barCpu').css("width", totalCpu + "%")
            if (totalCpu > 80) {
                // Above 80%
                $('#barCpu').addClass("bg-danger")
                $('#barCpu').removeClass("bg-warning")
                $('#barCpu').removeClass("bg-success")
            } else if (totalCpu > 50) {
                // Between 50% and 80%
                $('#barCpu').addClass("bg-warning")
                $('#barCpu').removeClass("bg-danger")
                $('#barCpu').removeClass("bg-success")
            } else {
                // Below 50%
                $('#barCpu').addClass("bg-success")
                $('#barCpu').removeClass("bg-warning")
                $('#barCpu').removeClass("bg-danger")
            }

            $('#totalCpuText').append(
                '<div class="float-left">CPU : </div><b>' + totalCpu + ' <div class="float-right">%</div>'
            )

            // Mem Bar
            $('#totalMem').empty();
            $('#totalMemText').empty();
            $('#barMem').css("width", totalMemPercent + "%")
            if (totalMemPercent > 80) {
                // Above 80%
                $('#barMem').addClass("bg-danger")
                $('#barMem').removeClass("bg-warning")
                $('#barMem').removeClass("bg-success")
            } else if (totalMemPercent > 50) {
                // Between 50% and 80%
                $('#barMem').addClass("bg-warning")
                $('#barMem').removeClass("bg-danger")
                $('#barMem').removeClass("bg-success")
            } else {
                // Below 50%
                $('#barMem').addClass("bg-success")
                $('#barMem').removeClass("bg-warning")
                $('#barMem').removeClass("bg-danger")
            }

            $('#totalMemText').append(
                '<div class="float-left">Mem : </div><b>' + totalMemPercent + ' <div class="float-right">%</div>'
            )
            $('#totalMemText').attr('title', usedMem + ' / ' + totalMem + ' used')

            // Hostname Bar
            $('#hostname').empty()
            $('#hostname').append(
                hostname
            )

        },
        error: function (error) {
            console.log(error);
        }
    });
}

$(document).ready(function () {
    $('[data-toggle="tooltip"]').tooltip();
});