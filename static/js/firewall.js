function verifyInputs() {

    let ipAddrSrc = document.getElementById('ipAddrSrc');
    let ipAddrDst = document.getElementById('ipAddrDst');
    let portSrc = document.getElementById('portSrc');
    let portDst = document.getElementById('portDst');
    let protoRadios = document.getElementsByName('gridRadiosProtocol');
    let protocol;

    for (let index = 0; index < protoRadios.length; index++)
        if (protoRadios[index].checked)
            protocol = protoRadios[index];

    if (ipAddrDst.value == "" && ipAddrSrc.value == "" && portDst.value == "" && portSrc.value == "") {

        displayError("Please specify at least one IP address/one port for this firewall rule");
        return;

    }

    if ((ipAddrDst.value != "" && ipAddrDst.disabled == true) || (ipAddrSrc.value != "" && ipAddrSrc.disabled == true) || (portSrc.value != "" && portSrc.disabled == true) || (portDst.value != "" && portDst.disabled == true)) {

        displayError("Invalid input");
        return;
    }

    if (testSameIpVersion() == false) {

        displayError("The firewall rule can handle one type of IP version at the time");
        return;

    }

    if ((portSrc.value != "" || portDst.value != "") && protocol.value == '3') {

        displayError("You can't specify a port number with the ICMP protocol");
        return;

    }

    if (protocol.value != 1 && protocol.value != 2 && protocol.value != 3 && protocol.value != 0) {

        displayError("Invalid protocol");
        return;

    }

    if (portSrc.value != "" && (portSrc.value < 1 || portSrc.value > 65535)) {

        displayError("Invalid source port");
        return;

    }

    if (portDst.value != "" && (portDst.value < 1 || portDst.value > 65535)) {

        displayError("Invalid source port");
        return;

    }

    flushAlerts();
    console.log('ok');

}