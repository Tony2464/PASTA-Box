function changeAuditMode(mode) {

    switch (mode) {
        case 2:
            loadSemiAutoMode();
            break;

        case 3:
            loadManualMode();
            break;

        default:
            loadAutoMode();
            break;
    }
}

function loadAutoMode() {

    let description = document.getElementById('des1');
    description.style.display = "block";
    disableDescriptions(0);

}

function loadSemiAutoMode() {

    let description = document.getElementById('des2');
    description.style.display = "block";
    disableDescriptions(1);

}

function loadManualMode() {

    let description = document.getElementById('des3');
    description.style.display = "block";
    disableDescriptions(2);

}

function disableDescriptions(exception) {

    let descriptions = document.getElementsByClassName('description');
    for (let index = 0; index < descriptions.length; index++) {
        if (exception != index) descriptions[index].style.display = "none";

    }

}