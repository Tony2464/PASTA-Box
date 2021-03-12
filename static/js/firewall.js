function verifyInputs() {

    let protoRadios = document.getElementsByName('gridRadiosProtocol');
    let protocol;

    for (let index = 0; index < protoRadios.length; index++) {

        if (protoRadios[index].checked) {
            protocol = protoRadios[index];
            break;
        }
    }

    var rule = {

        ipSrc: document.getElementById('ipAddrSrc'),
        ipDst: document.getElementById('ipAddrDst'),
        portSrc: document.getElementById('portSrc'),
        portDst: document.getElementById('portDst'),
        protocol: protocol,
        ipVersion: ""

    }

    if (rule['ipSrc'].value == "" && rule['ipDst'].value == "" && rule['portSrc'].value == "" && rule['portDst'].value == "") {

        displayError("Please specify at least one IP address/one port for this firewall rule");
        return;

    }

    if ((rule['ipDst'].value != "" && rule['ipDst'].disabled == true) || (rule['ipSrc'].value != "" && rule['ipSrc'].disabled == true) || (rule['portSrc'].value != "" && rule['portSrc'].disabled == true) || (rule['portDst'].value != "" && rule['portDst'].disabled == true)) {

        displayError("Invalid input");
        return;
    }

    rule['ipVersion'] = testSameIpVersion();

    if (rule['ipVersion'] == 0) {

        displayError("The firewall rule can handle one type of IP version at the time");
        return;

    }

    if ((rule['portSrc'].value != "" || rule['portDst'].value != "") && rule['protocol'].value == '3') {

        displayError("You can't specify a port number with the ICMP protocol");
        return;

    }

    if (rule['protocol'].value != 1 && rule['protocol'].value != 2 && rule['protocol'].value != 3 && rule['protocol'].value != 0) {

        displayError("Invalid protocol");
        return;

    }

    if (rule['portSrc'].value != "" && (rule['portSrc'].value < 1 || rule['portSrc'].value > 65535)) {

        displayError("Invalid source port");
        return;

    }

    if (rule['portDst'].value != "" && (rule['portDst'].value < 1 || rule['portDst'].value > 65535)) {

        displayError("Invalid source port");
        return;

    }

    flushAlerts();
    //sendFirewallRule(rule);

}

function sendFirewallRule(rule) {

    var req = new XMLHttpRequest();
    req.onreadystatechange = function () {
        if (req.readyState == 4) {
            if (req.status != 200) {
                //error handling code here
            } else {
                var response = JSON.parse(req.responseText)
                document.getElementById('myDiv').innerHTML = response.username
            }
        }
    }

    req.open('POST', '/ajax');
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send(rule)

}