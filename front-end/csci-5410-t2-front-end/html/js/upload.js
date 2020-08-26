function fileUpload() {
    var form = new FormData();
    var fileInput = document.getElementById("uploadfile");
    form.append("file", fileInput.files[0], fileInput.files[0].name);
    var settings = {
        "url": "https://safe-hamlet-70720.herokuapp.com/https://user-file-management-oydegtoyga-uc.a.run.app/upload",
        "method": "POST",
        "timeout": 0,
        "headers": {},
        "processData": false,
        "mimeType": "multipart/form-data",
        "contentType": false,
        "data": form
    };
    $.ajax(settings).done(function (response) {
        var response = JSON.parse(response);
        alert(response.message)
        var file_name = response.filename
        var hit_this = "https://us-east4-weatherbot-oyoe.cloudfunctions.net/getUserFiles"
        var email = localStorage.getItem('current_user')
        var data = JSON.stringify({
            "email": email,
            "is_upload": 1,
            "file_name": file_name
        });
        var settings = {
            "url": hit_this,
            "method": "POST",
            "timeout": 0,
            "headers": {
                "Content-Type": "application/json"
            },
            "data": data
        };
        $.ajax(settings).done(function (response) {
            console.log(response)
            window.location.reload();
        }).fail(function (error) {
            console.log(error);
        });
    }).fail(function (error) {
        console.log(error);
    });
}