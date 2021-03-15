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

    if (rule['ipDst'].value == "" && rule['ipDst'].disabled == false) {

        displayError("Invalid destination IP address");
        return;
    }

    if (rule['ipSrc'].value == "" && rule['ipSrc'].disabled == false) {

        displayError("Invalid source IP address");
        return;
    }

    if (rule['portSrc'].value == "" && rule['portSrc'].disabled == false) {

        displayError("Invalid source port");
        return;

    }

    if (rule['portDst'].value == "" && rule['portDst'].disabled == false) {

        displayError("Invalid destination port");
        return;

    }

    rule['ipVersion'] = testSameIpVersion();
    if (rule['ipVersion'] == 4) {

        displayError("The firewall rule can handle one type of IP version for the source/destination address");
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
    sendFirewallRule(rule);

}

function sendFirewallRule(rule) {

    var req = new XMLHttpRequest();
    req.onreadystatechange = function () {
        if (req.readyState == 4) {
            if (req.status == 200) {

                console.log(req.responseText);

            } else {

                displayServerError(req.responseText);

            }

        }
    }

    req.open('POST', '/admin/firewall/rule');
    req.setRequestHeader("Content-type", "application/json");
    req.send(JSON.stringify({
        ipSrc: rule['ipSrc'].value,
        ipDst: rule['ipDst'].value,
        portSrc: rule['portSrc'].value,
        portDst: rule['portDst'].value,
        protocol: rule['protocol'].value,
        ipVersion: rule['ipVersion']
    }));
}

function displayServerError(error) {

    switch (error) {

        case "error_proto":
            displayError("Invalid protocols");
            break;

        case "error_icmp":
            displayError("You can't specify a port number with the ICMP protocol");
            break;

        case "no_inputs":
            displayError("Please specify at least one IP address/one port for this firewall rule");
            break;

        case "error_ipvers_dst":
            displayError("Invalid destination IP address");
            break;

        case "error_ipvers_src":
            displayError("Invalid source IP address");
            break;

        case "error_ipvers_notsame":
            displayError("The firewall rule can handle one type of IP version for the source/destination address");
            break;

        case "error_port_src":
            displayError("Invalid source port");
            break;

        case "error_port_dst":
            displayError("Invalid destination port");
            break;

        default:
            console.log(error); //debugging
            displayError("Oups, server error :(");

    }

}