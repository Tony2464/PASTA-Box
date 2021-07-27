
// Called to draw the map
function draw() {
    // Get all devices to show
    var devices = []
    $.ajax({
        method: "GET",
        url: '/api/devices/mapDevices',
        success: function (response) {
            //Beginning
            devices = response
            drawMap(devices)
        },
        error: function (error) {
            console.log(error);
        }
    });
}

// Determine range of an IP address, return '0' '1' or '2'
// 1 ==> 10.0.0.0 – 10.255.255.255	
// 2 ==> 172.16.0.0 – 172.31.255.255
// 3 ==> 192.168.0.0 – 192.168.255.255	
function ipPrivateClass(ip) {
    var parts = ip.split('.')
    // 10.0.0.0 – 10.255.255.255
    if (parts[0] === '10')
        return 1
    // 172.16.0.0 – 172.31.255.255
    if (parts[0] === '172' && (parseInt(parts[1], 10) >= 16 && parseInt(parts[1], 10) <= 31))
        return 2
    // 192.168.0.0 – 192.168.255.255
    if (parts[0] === '192' && parts[1] === '168')
        return 3
}

// Actually drawing the map
function drawMap(devices) {

    var nodes = null;
    var edges = null;
    var network = null;

    var DIR = "/static/icons/";
    var EDGE_LENGTH_MAIN = 200;
    var EDGE_LENGTH_SUB = 200;

    var changeChosenNodeSize = function (values, id, selected, hovering) {
        values.shadow = true;
    };

    // Create a data table with nodes.
    nodes = [];

    // Create a data table with links.
    edges = [];


    //Get PASTA-Box info

    nodes.push({
        id: -1,
        label: "PASTA-Box\n" + getPastaIP().ipAddr,
        image: "/static/img/favicon.png",
        shape: "image",
        opacity: 0.7,
        // chosen: { label: false, node: changeChosenNodeShadow },
        chosen: { label: true, node: changeChosenNodeSize },
    });

    createPastaModal()

    //10.0.0.0 – 10.255.255.255
    firstRange = false
    // 172.16.0.0 – 172.31.255.255
    secondRange = false
    // 192.168.0.0 – 192.168.255.255
    thirdRange = false

    for (var i = 0; i < devices.length; i++) {

        deviceIp = devices[i].ipAddr

        // First range
        if (ipPrivateClass(deviceIp) == 1) {
            if (!firstRange) {
                // Add network node
                nodes.push({
                    id: "firstRange",
                    label: "Network\n10.0.0.0 – 10.255.255.255",
                    image: DIR + "hdd-network.svg",
                    shape: "image",
                });
                edges.push({ from: -1, to: "firstRange", length: EDGE_LENGTH_MAIN, color: { color: "red" } });
                firstRange = true
            }
            // Add computers
            deviceId = devices[i].id
            deviceIp = devices[i].ipAddr
            nodes.push({
                id: deviceId,
                label: "Device n°" + deviceId + "\n" + deviceIp,
                image: DIR + "laptop.svg",
                shape: "image",
                group: "computer",
                opacity: 1,
            });
            edges.push({ from: "firstRange", to: deviceId, length: EDGE_LENGTH_SUB });

            createModal()
        }
        // Second range
        if (ipPrivateClass(deviceIp) == 2) {

            if (!secondRange) {
                // Add network node
                nodes.push({
                    id: "secondRange",
                    label: "Network\n172.16.0.0 – 172.31.255.255",
                    image: DIR + "hdd-network.svg",
                    shape: "image",
                });
                edges.push({ from: -1, to: "secondRange", length: EDGE_LENGTH_MAIN, color: { color: "red" } });
                secondRange = true
            }
            // Add computers
            deviceId = devices[i].id
            deviceIp = devices[i].ipAddr
            nodes.push({
                id: deviceId,
                label: "Device n°" + deviceId + "\n" + deviceIp,
                image: DIR + "laptop.svg",
                shape: "image",
                group: "computer",
                opacity: 1,
            });
            edges.push({ from: "secondRange", to: deviceId, length: EDGE_LENGTH_SUB });

            createModal()
        }
        // Third range
        if (ipPrivateClass(deviceIp) == 3) {
            if (!thirdRange) {
                // Add network node
                nodes.push({
                    id: "thirdRange",
                    label: "Network\n192.168.0.0 – 192.168.255.255",
                    image: DIR + "hdd-network.svg",
                    shape: "image",
                });
                edges.push({ from: -1, to: "thirdRange", length: EDGE_LENGTH_MAIN, color: { color: "red" } });
                thirdRange = true
            }
            // Add computers
            deviceId = devices[i].id
            deviceIp = devices[i].ipAddr

            if (devices[i].activeStatus) {
                deviceStatus = "Active"
            } else {
                deviceStatus = "Not active"
            }
            deviceLastConnection = devices[i].lastConnection
            nodes.push({
                id: deviceId,
                label: "Device n°" + deviceId + "\n" + deviceIp,
                image: DIR + "laptop.svg",
                shape: "image",
                group: "computer",
                opacity: 1,
            });
            edges.push({ from: "thirdRange", to: deviceId, length: EDGE_LENGTH_SUB });
            createModal()
        }
    }

    // create a network
    var container = document.getElementById("mynetwork");
    var data = {
        nodes: nodes,
        edges: edges,
    };
    var options = {
        groups: {
            computer: {
                opacity: 0.3,
            },
        },
        interaction: {
            hover: true,
            navigationButtons: true,
            keyboard: true,
        },
    };
    network = new vis.Network(container, data, options);
    network.on('click', function (properties) {
        if (properties.nodes != "") {
            $("#modal" + properties.nodes).modal("show")
        }
    });
    // network.on('nodeHover', function(properties){
    //     alert("hoverEdge");
    // }
    // );
}

function createModal() {
    $("#modals").append(`
            <div class="modal fade" id="modal`+ deviceId + `">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title"><b>Device `+ deviceIp + `</b></h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <p>Status : `+ deviceStatus + `</p>
                            <p>Last seen : `+ deviceLastConnection + `</p>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-primary" onclick="window.open('/admin/device/`+ deviceId + `');">See more <img src="/static/icons/eye-fill.svg" alt="" width="20" height="20"></button>
                        </div>
                    </div>
                </div>
            </div>
            `)
}

function createPastaModal() {
    var pastaInfo = getPastaIP()
    $("#modals").append(`
            <div class="modal fade" id="modal-1">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title"><b>PASTA-Box</b></h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <p>IP address : `+ pastaInfo.ipAddr + `</p>
                            <p>Hostname : `+ pastaInfo.hostname + `</p>
                            <p>Gateway : `+ pastaInfo.gateway + `</p>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-primary" onclick="window.location.replace('/admin/settings/system/');">Go to settings <img src="/static/icons/gear-wide-white.svg" alt="" width="20" height="20"></button>
                        </div>
                    </div>
                </div>
            </div>
            `)
}

function getPastaIP() {
    var res = " "
    $.ajax({
        method: "GET",
        url: '/api/devices/pasta-info',
        async: false,
        success: function (response) {
            res = response
        },
        error: function (error) {
            console.log(error);
        }
    });
    return res
}
