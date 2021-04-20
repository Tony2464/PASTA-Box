function checkMainSettingsInputs() {

    var config = {

        ipAddr: document.getElementById('ipAddr'),
        netmask: document.getElementById('netmask'),
        gateway: document.getElementById('gateway'),
        hostname: document.getElementById('hostname')

    }

    if (config['ipAddr'].value == "" || config['ipAddr'] == null){

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
    // sendConfig(config);

}