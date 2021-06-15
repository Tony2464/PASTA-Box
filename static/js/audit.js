var auditMode = 0;

function updateMode(value) {

    window.auditMode = value;

}

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

    let changeButton = document.getElementById('changeModeButton');
    let buttonMode2 = document.getElementById('buttonMode2');
    let buttonMode3 = document.getElementById('buttonMode3');

    if (auditMode != 1) {
        console.log(auditMode);
        changeButton.style.display = "block";
        buttonMode2.style.display = "none";
        buttonMode3.style.display = "none";

    } else {

        changeButton.style.display = "none";
        buttonMode2.style.display = "none";
        buttonMode3.style.display = "none";

    }

}

function loadSemiAutoMode() {

    let description = document.getElementById('des2');
    description.style.display = "block";
    disableDescriptions(1);

    let changeButton = document.getElementById('changeModeButton');
    let buttonMode2 = document.getElementById('buttonMode2');
    let buttonMode3 = document.getElementById('buttonMode3');

    if (auditMode != 2) {

        changeButton.style.display = "block";
        buttonMode2.style.display = "none";
        buttonMode3.style.display = "none";

    } else {

        changeButton.style.display = "none";
        buttonMode2.style.display = "block";
        buttonMode3.style.display = "none";

    }

}

function loadManualMode() {

    let description = document.getElementById('des3');
    description.style.display = "block";
    disableDescriptions(2);

    let changeButton = document.getElementById('changeModeButton');
    let buttonMode2 = document.getElementById('buttonMode2');
    let buttonMode3 = document.getElementById('buttonMode3');

    if (auditMode != 3) {

        changeButton.style.display = "block";
        buttonMode2.style.display = "none";
        buttonMode3.style.display = "none";

    } else {

        changeButton.style.display = "none";
        buttonMode2.style.display = "none";
        buttonMode3.style.display = "block";

    }


}

function disableDescriptions(exception) {

    let descriptions = document.getElementsByClassName('description');
    for (let index = 0; index < descriptions.length; index++) {
        if (exception != index) descriptions[index].style.display = "none";

    }

}