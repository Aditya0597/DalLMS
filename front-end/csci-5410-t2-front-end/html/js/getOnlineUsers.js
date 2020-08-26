get_online_users_link = "https://us-central1-weatherbot-oyoe.cloudfunctions.net/getOnline";
function get_online_users() {
    var email = localStorage.getItem('current_user')
    var data = JSON.stringify({
        "email": email,
        "is_logout": 0
    });
    console.log(data)
    console.log("USER: " + data)
    var config = {
        "url": get_online_users_link,
        "method": "POST",
        "timeout": 0,
        "headers": {
            "Content-Type": "application/json"
        },
        "data": data,
    };
    $.ajax(config).done(function (response) {
        var online_users = response.result.active_users
        console.log(online_users)
        console.log(online_users.length)
        var i;
        var content = '';
        for (i = 0; i < online_users.length; i++) {
            var name = online_users[i]['name'];
            var email_fetched = online_users[i]['email'];
            var institute = online_users[i]['institute'];
            var role = online_users[i]['role'];
            if (email === email_fetched) {
                document.getElementById('usernamespan').innerText = "Welcome, " + name;
                localStorage.setItem('name', name);
            } else {
                var newdiv1 = `
                <div class="col-xl-3 col-md-6 mb-4">
                    <div class="card border-left-primary shadow h-100 py-2">
                        <div class="card-body">
                            <div class="row no-gutters align-items-center">
                                <div class="col mr-2">
                                    <div class="h5 mb-0 font-weight-bold text-primary text-uppercase mb-1">${name}
                                    </div>
                                    <div class="text-xs font-weight-bold text-gray-500 text-uppercase ">Institute: ${institute}
                                    </div>
                                    <div class="text-xs font-weight-bold text-gray-500 text-uppercase ">Role: ${role}
                                    </div>
                                </div>
                                <div class="col-auto">
                                    <i class="fas fa-user fa-2x text-gray-300"></i>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
                content += newdiv1;
            }
        }
        $('#parentOnlineUserDiv').html(content)
    })
}
    //     var resp = request_server(URL_3 + 'user/home', {}, "GET");
    //     var user_data = resp['result']
    //     var user_name = localStorage.getItem('current_user')
    //     if (resp['code'] == 200) {
    //         var i;
    //         var content = '';
    //         for (i = 0; i < user_data['active_users'].length; i++) {
    //             var name = user_data['active_users'][i]['name'];
    //             var topic = user_data['active_users'][i]['topic'];
    //             if (name === user_name) {

    //             } else {
    //                 var newdiv1 = `
    //             <div class="card">
    //             <img src="img_avatar.png" alt="Avatar" style="width:50%">
    //             <h4 id="username"><b>${name}</b></h4>
    //             <p id="topic">Topic: ${topic}</p>
    //         </div>
    //         `;
    //                 content += newdiv1;
    //             }
    //         }
    //         $('#content').html(content);
    //         // document.getElementById("status").innerHTML =;
    //         // document.getElementById("topic").innerHTML =;
    //     }
    // }