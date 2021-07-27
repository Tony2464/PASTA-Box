function deleteAlert(id) {

    var req = new XMLHttpRequest();
    req.onreadystatechange = function () {
        if (req.readyState == 4) {
            if (req.status == 200) {

                document.getElementById("alert" + id).remove();
                displaySuccess("Alert deleted successfully !");

            } else {

                console.log(req.responseText); //debugging
                displayError("Oups, server error :(");

            }

        }
    }

    req.open('POST', '/admin/security/alert/delete');
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send("id=" + id);

}