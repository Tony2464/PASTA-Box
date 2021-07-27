var auditMode = 0;

function updateMode(value) {

    window.auditMode = value;

}

function changeAuditMode(mode) {

    switch (mode) {
        case 2:
            loadSemiAutoMode();
            break;

        case 3:
            loadManualMode();
            break;

        default:
            loadAutoMode();
            break;
    }
}

function loadAutoMode() {

    let description = document.getElementById('des1');
    description.style.display = "block";
    disableDescriptions(0);

    let changeButton = document.getElementById('changeModeButton');
    let buttonMode2 = document.getElementById('buttonMode2');
    let buttonMode3 = document.getElementById('buttonMode3');

    if (auditMode != 1) {

        changeButton.style.display = "block";
        changeButton.setAttribute("onclick", "updateAuditMode(1)");

        buttonMode2.style.display = "none";
        buttonMode3.style.display = "none";

    } else {

        changeButton.setAttribute("onclick", "");
        changeButton.style.display = "none";
        buttonMode2.style.display = "none";
        buttonMode3.style.display = "none";

    }

}

function loadSemiAutoMode() {

    let description = document.getElementById('des2');
    description.style.display = "block";
    disableDescriptions(1);

    let changeButton = document.getElementById('changeModeButton');
    let buttonMode2 = document.getElementById('buttonMode2');
    let buttonMode3 = document.getElementById('buttonMode3');

    if (auditMode != 2) {

        changeButton.style.display = "block";
        changeButton.setAttribute("onclick", "updateAuditMode(2)");

        buttonMode2.style.display = "none";
        buttonMode3.style.display = "none";

    } else {

        changeButton.setAttribute("onclick", "");
        changeButton.style.display = "none";
        buttonMode2.style.display = "block";
        buttonMode3.style.display = "none";

    }

}

function loadManualMode() {

    let description = document.getElementById('des3');
    description.style.display = "block";
    disableDescriptions(2);

    let changeButton = document.getElementById('changeModeButton');
    let buttonMode2 = document.getElementById('buttonMode2');
    let buttonMode3 = document.getElementById('buttonMode3');

    if (auditMode != 3) {

        changeButton.style.display = "block";
        changeButton.setAttribute("onclick", "updateAuditMode(3)");

        buttonMode2.style.display = "none";
        buttonMode3.style.display = "none";

    } else {

        changeButton.setAttribute("onclick", "");
        changeButton.style.display = "none";
        buttonMode2.style.display = "none";
        buttonMode3.style.display = "block";

    }


}

function disableDescriptions(exception) {

    let descriptions = document.getElementsByClassName('description');
    for (let index = 0; index < descriptions.length; index++) {
        if (exception != index) descriptions[index].style.display = "none";

    }

}

function updateAuditMode(mode) {

    if (mode < 1 || mode > 3)
        return;

    var req = new XMLHttpRequest();
    req.onreadystatechange = function () {
        if (req.readyState == 4) {

            var jsonString = JSON.parse(req.responseText);
            if (req.status == 200) {

                displaySuccess(jsonString["message"]);
                setTimeout(redirect, 4000);

            } else {

                displayError(jsonString["message"]);

            }

        }
    }

    req.open('POST', '/admin/audit/mode');
    req.setRequestHeader("Content-type", "application/json");
    req.send(JSON.stringify({
        mode: mode
    }));

}

function scanSpecificIP() {

    let ipAddr = document.getElementById('specificIpAddr').value.trim();
    if (ipAddr == "") return;

    var req = new XMLHttpRequest();
    req.onreadystatechange = function () {

        if (req.readyState == 4) {

            if (req.status == 400) {

                var jsonString = JSON.parse(req.responseText);
                displayError(jsonString["message"]);

            } else {

                let a = document.createElement('a');
                a.target = '_blank';
                a.href = req.responseURL;
                a.click();

            }

        }
    }

    req.open('POST', '/admin/audit/scanip');

    req.setRequestHeader("Content-type", "application/json");
    req.send(JSON.stringify({
        ipAddr: ipAddr
    }));

}

function redirect() {

    self.location.href = "/admin/audit";

}

function scanDevice(id) {

    var req = new XMLHttpRequest();
    req.onreadystatechange = function () {

        if (req.readyState == 4) {

            if (req.status == 200) {

                var jsonString = JSON.parse(req.responseText);
                displaySuccess(jsonString["message"]);
                document.getElementById('scanButton').disabled = true;

            } else {

                var jsonString = JSON.parse(req.responseText);
                displayError(jsonString["message"]);

            }

        }
    }

    req.open('POST', '/admin/device/scan/' + id);
    req.setRequestHeader("Content-type", "application/json");
    req.send();

}