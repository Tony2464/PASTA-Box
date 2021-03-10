function enableInput(id) {

    let input = document.getElementById(id);
    input.disabled = false;

}

function disableInput(id) {


    let input = document.getElementById(id);
    input.disabled = true;

}

function displayError(error) {

    flushAlerts();
    let divAlert = document.createElement('div');
    let danger = document.createElement('strong');
    const target = document.querySelector('#errorAnchor');

    danger.innerHTML = "Error ! "
    divAlert.className = "alert alert-danger";
    target.parentNode.insertBefore(divAlert, target.nextSibling);
    divAlert.appendChild(danger);
    divAlert.innerHTML += error;

}

function flushAlerts() {

    let alerts = document.getElementsByClassName('alert');
    if (alerts != null)
        for (let i = 0; i < alerts.length; i++)
            alerts[i].remove();

}