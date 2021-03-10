var regexIPv4 = new RegExp('^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$');
var regexIPv6 = new RegExp('(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))');

function checkPort(id) {

    let input = document.getElementById(id).value;
    if (input < 1 || input > 65535)
        displayError("Invalid port");
    else
        flushAlerts();

}

function checkIP(id) {

    let input = document.getElementById(id).value;
    if (checkIpVersion(input) != 0) {
        if (testSameIpVersion() == false)
            displayError("The firewall rule can handle one type of IP version at the time");
    } else
        displayError("Invalid IP address");

}

function testSameIpVersion() {

    let ip1 = document.getElementById('ipAddrSrc').value;
    let ip2 = document.getElementById('ipAddrDst').value;

    if (ip1 != "" && ip2 != "")
        if (checkIpVersion(ip1) != checkIpVersion(ip2))
            return false;

    return true;

}

function checkIpVersion(IPaddress) {

    if (regexIPv4.test(IPaddress) == true)
        return 1;
    else if (regexIPv6.test(IPaddress) == true)
        return 2;
    else
        return 0;

}