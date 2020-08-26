
function userFiles() {
    var email = localStorage.getItem('current_user')
    var data = JSON.stringify({
        "email": email,
        "is_upload": 0,
        "file_name": "dummy.txt"
    });
    console.log(data)
    var settings = {
        "url": "https://us-east4-weatherbot-oyoe.cloudfunctions.net/getUserFiles",
        "method": "POST",
        "timeout": 3000,
        "headers": {
            "Content-Type": "application/json"
        },
        "processData": false,
        "mimeType": "multipart/form-data",
        "contentType": false,
        "data": data
    };
    $.ajax(settings).done(function (response) {
        var response = JSON.parse(response)
        var i;
        var content = '';
        var result = response.result;
        for (i = 0; i < result.length; i++) {
            var file_name = result[i]['file_name'];
            var newdiv = `
                <tr>
                    <td>${file_name}</td>
                    <td><a href="https://user-file-management-oydegtoyga-uc.a.run.app/file/user?name=${file_name}" style="color:white;" id="${file_name}" class="btn btn-success"><i class="fa fa-download">Download</i></a></td>
                </tr>
            `;
            content += newdiv;

        }
        $('#parentTableDiv').html(content)
    }).fail(function (error) {
        console.log(error);
    });

}