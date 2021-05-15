
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

    nodes.push({
        id: 1,
        label: "PASTA-Box",
        image: "/static/img/favicon.png",
        shape: "image",
        opacity: 0.7,
        // chosen: { label: false, node: changeChosenNodeShadow },
        chosen: { label: true, node: changeChosenNodeSize },
    });

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
                edges.push({ from: 1, to: "firstRange", length: EDGE_LENGTH_MAIN, color: { color: "red" } });
                firstRange = true
            }
            // Add computers
            deviceId = devices[i].id
            deviceIp = devices[i].ipAddr
            nodes.push({
                id: deviceId,
                label: "Device\n" + deviceIp,
                image: DIR + "laptop.svg",
                shape: "image",
                group: "computer",
                opacity: 1,
            });
            edges.push({ from: "firstRange", to: deviceId, length: EDGE_LENGTH_SUB });
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
                edges.push({ from: 1, to: "secondRange", length: EDGE_LENGTH_MAIN, color: { color: "red" } });
                secondRange = true
            }
            // Add computers
            deviceId = devices[i].id
            deviceIp = devices[i].ipAddr
            nodes.push({
                id: deviceId,
                label: "Device\n" + deviceIp,
                image: DIR + "laptop.svg",
                shape: "image",
                group: "computer",
                opacity: 1,
            });
            edges.push({ from: "secondRange", to: deviceId, length: EDGE_LENGTH_SUB });
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
                edges.push({ from: 1, to: "thirdRange", length: EDGE_LENGTH_MAIN, color: { color: "red" } });
                thirdRange = true
            }
            // Add computers
            deviceId = devices[i].id
            deviceIp = devices[i].ipAddr
            nodes.push({
                id: deviceId,
                label: "Device\n" + deviceIp,
                image: DIR + "laptop.svg",
                shape: "image",
                group: "computer",
                opacity: 1,
            });
            edges.push({ from: "thirdRange", to: deviceId, length: EDGE_LENGTH_SUB });
        }
        // console.log(devices[i].ipAddr)
        // console.log(ipPrivateClass(devices[i].ipAddr))
    }

    // nodes.push({
    //     id: 2,
    //     label: "Network",
    //     image: DIR + "hdd-network.svg",
    //     shape: "image",
    // });
    // nodes.push({
    //     id: 3,
    //     label: "Network",
    //     image: DIR + "hdd-network.svg",
    //     shape: "image",
    // });
    // edges.push({ from: 1, to: 2, length: EDGE_LENGTH_MAIN, color: { color: "red" } });
    // edges.push({ from: 1, to: 3, length: EDGE_LENGTH_MAIN, color: { color: "red" } });

    // for (var i = 1000; i <= 1007; i++) {
    //     nodes.push({
    //         id: i,
    //         label: "Computer",
    //         image: DIR + "laptop.svg",
    //         shape: "image",
    //         group: "computer",
    //         opacity: 1,
    //     });
    //     edges.push({ from: 2, to: i, length: EDGE_LENGTH_SUB });
    // }

    // nodes.push({
    //     id: 101,
    //     label: "Printer",
    //     image: DIR + "printer.svg",
    //     shape: "image",
    // });
    // edges.push({ from: 2, to: 101, length: EDGE_LENGTH_SUB });

    // nodes.push({
    //     id: 102,
    //     label: "Laptop",
    //     image: DIR + "laptop.svg",
    //     shape: "image",
    // });
    // edges.push({ from: 3, to: 102, length: EDGE_LENGTH_SUB });

    // for (var i = 200; i <= 210; i++) {
    //     nodes.push({
    //         id: i,
    //         label: "Laptop",
    //         image: DIR + "laptop.svg",
    //         shape: "image",
    //     });
    //     edges.push({ from: 3, to: i, length: EDGE_LENGTH_SUB });
    // }

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
        },
    };
    network = new vis.Network(container, data, options);
    network.on('click', function (properties) {
        if (properties.nodes != "")
            alert('clicked node ' + properties.nodes);
    });
    // network.on('nodeHover', function(properties){
    //     alert("hoverEdge");
    // }
    // );
}
