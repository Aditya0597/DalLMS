log_out_function = "https://us-central1-weatherbot-oyoe.cloudfunctions.net/getOnline"
function logout() {
    var data = JSON.stringify({
        "email": localStorage.getItem('current_user'),
        "is_logout": 1
    });
    console.log(data)
    console.log("USER: " + data)
    var config = {
        "url": log_out_function,
        "method": "POST",
        "timeout": 0,
        "headers": {
            "Content-Type": "application/json"
        },
        "data": data,
    };
    $.ajax(config).done(function (response) {
        console.log(response)
        if (response.statusCode == 200) {
            localStorage.clear();
            window.location.href = 'login.html'
        } else {
            alert("Couldn't logout!")
        }
    })
}