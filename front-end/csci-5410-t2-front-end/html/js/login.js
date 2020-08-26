var Lambda_function_login = 'https://pxujril4k3.execute-api.us-east-1.amazonaws.com/prod/login';
var GCP_twofa = 'https://us-central1-weatherbot-oyoe.cloudfunctions.net/auth';

function twofa() {
    var question = $('#question').val();
    var answer = $('#answer').val();
    var email = $('#email').val();
    console.log(question, answer)
    var data = JSON.stringify({
        "question": question,
        "answer": answer,
        "email": email
    })
    var config = {
        "url": GCP_twofa,
        "method": "POST",
        "timeout": 0,
        "headers": {
            "Content-Type": "application/json"
        },
        "data": data,
    };
    $.ajax(config).done(function (response) {
        localStorage.setItem('current_user', email);
        window.location.href = "index.html"
    }).fail(function (error) {
        console.log(error)
        if (error.responseJSON.error) {
            alert(error.responseJSON.error);
        }
        window.location.href = "login.html"
    });
}
function login() {
    var email = $('#email').val();
    var password = $('#password').val();
    if (email.length < 1 || password.length < 1) {
        alert('Form contains empty fields!')
    } else {
        console.log(email, password)
        var data = JSON.stringify({
            "email": email,
            "password": password
        })
        var config = {
            "url": Lambda_function_login,
            "method": "POST",
            dataType: "json",
            "timeout": 0,
            "headers": {
                "Content-Type": "application/json"
            },
            "data": data,
        };
        $.ajax(config).done(function (response) {
            if (response.statusCode == 200) {
                // window.location.href = "index.html"
                var body = JSON.parse(response.body)
                var email = body.user.email
                var question = body.user.question
                console.log(email, question)
                var str = `<div class="text-center">
                        <h1 class="h4 text-gray-900 mb-4">Please answer the security question.</h1>
                    </div>
                    <form class="user">
                        <div class="form-group">
                            <input type="text" style="visibility: hidden" class="form-control form-control-user" id="email" aria-describedby="emailHelp"
                            value="${email}" disabled>
                        </div>
                        <div class="form-group">
                            <input type="text" class="form-control form-control-user" id="question" aria-describedby="questionHelp"
                            value="${question}" disabled>
                        </div>
                        <div class="form-group">
                            <input type="text" class="form-control form-control-user" id="answer"
                            placeholder="Your Answer">
                        </div>
                        <button onclick="twofa();" type="button" class="btn btn-success btn-user btn-block">Submit</button>
                    </form>
                `
                console.log(str);
                $('#parentDiv').html(str);
            } else {
                alert('Incorrect credentials!')
            }
        }).fail(function (error) {
            alert('Login failed!')
            console.log(error)

        });
    }
}
