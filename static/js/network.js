var stringRegexIPv4 = /^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/gm;
var regexIPv4 = new RegExp(stringRegexIPv4);
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
        if (testSameIpVersion() == 0)
            displayError("The firewall rule can handle one type of IP version for the source/destination address");
        else
            flushAlerts();
    } else
        displayError("Invalid IP address");

}

function testSameIpVersion() {

    let ip1 = document.getElementById('ipAddrSrc').value;
    let ip2 = document.getElementById('ipAddrDst').value;

    let versionSrc = 0;
    let versionDst = 0;

    if (ip1 != "")
        versionSrc = checkIpVersion(ip1)

    if (ip2 != "")
        versionDst = checkIpVersion(ip2)

    if (versionSrc != 0) {
        if (versionDst != 0) {
            if (versionSrc == versionDst)
                return versionSrc;
            else
                return 0
        } else {
            return versionSrc;
        }
    } else {
        return versionDst;
    }

}

function checkIpVersion(IPaddress) {

    if (regexIPv4.test(IPaddress) == true)
        return 1;
    else if (regexIPv6.test(IPaddress) == true)
        return 2;
    else
        return 0;

}