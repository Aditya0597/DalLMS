var GCP_function = 'https://us-central1-weatherbot-oyoe.cloudfunctions.net/reguser';
function register() {
    var name = $('#name').val();
    var email = $('#email').val();
    var password = $('#password').val();
    var gender = $('#gender').val();
    var instituteName = $('#instituteName').val();
    var role = $('#role').val();
    var question = $('#question').val();
    var answer = $('#answer').val();
    console.log(name, email, password, gender, instituteName, role, question, answer)
    var data = JSON.stringify({
        "email": email,
        "name": name,
        "password": password,
        "gender": gender,
        "instituteName": instituteName,
        "role": role,
        "question": question,
        "answer": answer
    })
    var config = {
        "url": GCP_function,
        "method": "POST",
        "timeout": 0,
        "headers": {
            "Content-Type": "application/json"
        },
        "data": data,
    };
    $.ajax(config).done(function (response) {
        alert(response.message);
        window.location.href = "login.html"
    }).fail(function (error) {
        if (error.responseJSON.message) {
            alert(error.responseJSON.message);

        } else {
            alert(error.responseJSON.error);
        }
    });
}
