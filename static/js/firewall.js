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
    flushRuleInputs();

}

function sendFirewallRule(rule) {

    var req = new XMLHttpRequest();
    req.onreadystatechange = function () {
        if (req.readyState == 4) {
            if (req.status == 200) {

                console.log(req.responseText);
                displaySuccess("Your rule has been added successfully !");
                updateRules();

            } else {

                var jsonString = JSON.parse(req.responseText);
                displayConfigError(jsonString["message"]);

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

function flushRuleInputs() {

    let checkbox = document.getElementsByName('gridRadiosProtocol');
    checkbox[0].checked = true;

    disableInput('ipAddrDst');
    disableInput('ipAddrSrc');
    disableInput('portDst');
    disableInput('portSrc');

    document.getElementsByName('gridRadiosIpSrc')[0].checked = true;
    document.getElementsByName('gridRadiosIpDst')[0].checked = true;
    document.getElementsByName('gridRadiosPortDst')[0].checked = true;
    document.getElementsByName('gridRadiosPortSrc')[0].checked = true;
}

function deleteRule(id) {

    var req = new XMLHttpRequest();
    req.onreadystatechange = function () {
        if (req.readyState == 4) {
            if (req.status == 200) {

                let rules = document.getElementsByTagName('tr');
                for (let index = 1; index < rules.length; index++) {

                    let header = rules[index].getElementsByTagName('td')[0].innerHTML;
                    if (parseInt(header, 10) == id) {

                        rules[index].remove();
                        break;

                    }

                }

                displaySuccess("Rule n°" + id + " deleted successfully !");

            } else {

                console.log(req.responseText); //debugging
                displayError("Oups, server error :(");

            }

        }
    }

    req.open('POST', '/admin/firewall/rule/delete');
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send("id=" + id);

}

function updateRules() {

    let body = document.getElementsByTagName('tbody')[0];
    body.innerHTML = "";

    let newColumn;
    let newLine;
    let deleteButton;

    fetch(getDomain() + '/api/rules/', {
            method: 'GET'
        })
        .then(function (response) {
            return response.json();
        })
        .then(function (json) {

            for (let i = 0; i < json.length; i++) {

                newLine = document.createElement('tr');

                newColumn = document.createElement('td');
                newColumn.innerHTML = json[i]['id'];
                newLine.appendChild(newColumn);

                newColumn = document.createElement('td');
                if (json[i]['ipDst'] == "")
                    newColumn.innerHTML = "X";
                else
                    newColumn.innerHTML = json[i]['ipDst'];
                newLine.appendChild(newColumn);

                newColumn = document.createElement('td');
                if (json[i]['ipSrc'] == "")
                    newColumn.innerHTML = "X";
                else
                    newColumn.innerHTML = json[i]['ipSrc'];
                newLine.appendChild(newColumn);

                newColumn = document.createElement('td');
                if (json[i]['portDst'] == null)
                    newColumn.innerHTML = "X";
                else
                    newColumn.innerHTML = json[i]['portDst'];
                newLine.appendChild(newColumn);

                newColumn = document.createElement('td');
                if (json[i]['portSrc'] == null)
                    newColumn.innerHTML = "X";
                else
                    newColumn.innerHTML = json[i]['portSrc'];
                newLine.appendChild(newColumn);

                newColumn = document.createElement('td');
                newColumn.innerHTML = returnProtocol(json[i]['protocol']);
                newLine.appendChild(newColumn);

                newColumn = document.createElement('td');
                deleteButton = document.createElement('button');
                deleteButton.className = "btn btn-dark";
                deleteButton.innerHTML = "Delete";
                deleteButton.setAttribute("data-bs-toggle", "modal");
                deleteButton.setAttribute("data-bs-target", "#Modal" + json[i]['id']);
                newColumn.appendChild(deleteButton);
                newLine.appendChild(newColumn);

                body.appendChild(newLine);
            }

            addModal(json[json.length - 1]['id']);

        });

}

function addModal(id) {

    document.getElementsByTagName('body')[0].innerHTML += '<div class="modal fade" id="Modal' + id + '" tabindex="-1" aria-labelledby="ModalLabel" aria-hidden="true">\
                <div class="modal-dialog modal-dialog-centered">\
                    <div class="modal-content" style="background-color:#fff !important;">\
                        <div class="modal-header">\
                            <h5 class="modal-title">Delete rule n°' + id + '</h5>\
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>\
                        </div>\
                        <div class="modal-body">\
                            Are you really sure to delete the rule n°' + id + ' ? \
                        </div>\
                        <div class="modal-footer">\
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>\
                            <button onclick="deleteRule(\'' + id + '\')" type="button" data-bs-dismiss="modal"\
                                class="btn btn-primary">Delete</button>\
                        </div>\
                    </div>\
                </div>\
            </div>';

}