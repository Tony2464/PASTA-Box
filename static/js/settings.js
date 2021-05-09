function checkMainSettingsInputs() {

    var config = {

        ipAddr: document.getElementById('ipAddr'),
        netmask: document.getElementById('netmask'),
        gateway: document.getElementById('gateway'),
        hostname: document.getElementById('hostname')

    }

    if (config['ipAddr'].value == "" || config['ipAddr'] == null) {

        displayError("The IP address can't be empty");
        return;

    }

    if (config['netmask'].value == "" || config['netmask'] == null) {

        displayError("The subnet mask can't be empty");
        return;

    }

    if (config['gateway'].value == "" || config['gateway'] == null) {

        displayError("The IP address of the gateway can't be empty");
        return;

    }

    if (config['hostname'].value == "" || config['hostname'] == null) {

        displayError("The hostname of the PASTA-Box can't be empty");
        return;

    }

    flushAlerts();
    sendConfig(config);

}

function sendConfig(config) {

    var req = new XMLHttpRequest();
    req.onreadystatechange = function () {
        if (req.readyState == 4) {
            if (req.status == 200) {

                console.log(req.responseText);
                displaySuccess("Configuration updated successfully !");

            } else {

                displayConfigError(req.responseText);

            }

        }
    }

    req.open('POST', '/admin/settings/system');
    req.setRequestHeader("Content-type", "application/json");
    req.send(JSON.stringify({
        ipAddr: config['ipAddr'].value,
        netmask: config['netmask'].value,
        gateway: config['gateway'].value,
        hostname: config['hostname'].value
    }));
}

function displayConfigError(error) {

    switch (error) {

        case "error_ip":
            displayError("Invalid IP address");
            break;

        case "error_gw":
            displayError("Invalid gateway");
            break;

        case "error_hostname":
            displayError("Invalid hostname, maybe it's not formatted correctly or contains some unauthorized characters");
            break;

        case "error_gw":
            displayError("Invalid gateway");
            break;

        case "error_mask":
            displayError("Invalid netmask");
            break;

        case "error_cmd":
            displayError("Invali command");
            break;

        default:
            console.log(error); //debugging
            displayError("Oups, server error :(");

    }

}

function sendComand(cmd) {

    var req = new XMLHttpRequest();
    req.onreadystatechange = function () {
        if (req.readyState == 4) {
            if (req.status == 200) {

                console.log(req.responseText);

                switch (cmd) {

                    case "restart":
                        displaySuccess("The PASTA-Box will restart in few seconds...");
                        break;

                    case "shutdown":
                        displaySuccess("The PASTA-Box will shutdown in few seconds...");
                        break;

                    case "restart_services":
                        displaySuccess("The PASTA-Box is reloading all the services...");
                        break;

                }


            } else {

                displayConfigError(req.responseText);

            }

        }
    }

    req.open('POST', '/admin/settings/system/actions');
    req.setRequestHeader("Content-type", "application/json");
    req.send(JSON.stringify({
        command: cmd
    }));

}