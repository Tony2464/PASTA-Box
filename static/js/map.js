var nodes = null;
var edges = null;
var network = null;

var DIR = "/static/icons/";
var EDGE_LENGTH_MAIN = 200;
var EDGE_LENGTH_SUB = 200;

// Called when the Visualization API is loaded.
function draw() {
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
    });
    nodes.push({
        id: 2,
        label: "Network",
        image: DIR + "hdd-network.svg",
        shape: "image",
    });
    nodes.push({
        id: 3,
        label: "Network",
        image: DIR + "hdd-network.svg",
        shape: "image",
    });
    edges.push({ from: 1, to: 2, length: EDGE_LENGTH_MAIN, color: { color: "red" } });
    edges.push({ from: 1, to: 3, length: EDGE_LENGTH_MAIN, color: { color: "red" } });

    for (var i = 4; i <= 7; i++) {
        nodes.push({
            id: i,
            label: "Computer",
            image: DIR + "laptop.svg",
            shape: "image",
            group: "computer",
            opacity: 1,
        });
        edges.push({ from: 2, to: i, length: EDGE_LENGTH_SUB });
    }

    nodes.push({
        id: 101,
        label: "Printer",
        image: DIR + "printer.svg",
        shape: "image",
    });
    edges.push({ from: 2, to: 101, length: EDGE_LENGTH_SUB });

    nodes.push({
        id: 102,
        label: "Laptop",
        image: DIR + "laptop.svg",
        shape: "image",
    });
    edges.push({ from: 3, to: 102, length: EDGE_LENGTH_SUB });

    for (var i = 200; i <= 210; i++) {
        nodes.push({
            id: i,
            label: "Laptop",
            image: DIR + "laptop.svg",
            shape: "image",
        });
        edges.push({ from: 3, to: i, length: EDGE_LENGTH_SUB });
    }

    // create a network
    var container = document.getElementById("mynetwork");
    var data = {
        nodes: nodes,
        edges: edges,
    };
    var options = {
        nodes: {
            opacity: .5
        },
        groups: {
            computer: {
                opacity: 0.3,
            },
        },
    };
    network = new vis.Network(container, data, options);
    network.on('click', function (properties) {
        if (properties.nodes != "")
            alert('clicked node ' + properties.nodes);
    });
}