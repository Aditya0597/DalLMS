
function chatHistory() {
    var settings = {
        "url": "https://user-file-management-oydegtoyga-uc.a.run.app/files/chat",
        "method": "GET",
        "timeout": 0,
        "headers": {}
    };

    $.ajax(settings).done(function (response) {
        if (response.files.length == 0) {
            content = `<p>No files to show</p>`
            $('#parentTableDivChat').html(content)
        } else {
            var files = response.files;
            for (var i = 0; i < files.length; i++) {
                var file_name = files[i];
                newDiv = `
                <tr>
                    <td>${file_name}</td>
                    <td><a href="https://user-file-management-oydegtoyga-uc.a.run.app/file/chat?name=${file_name}" style="color:white;" id="${file_name}" class="btn btn-success"><i class="fa fa-download">Download</i></a></td>
                </tr>`;
                content += newDiv;
            }
            $('#parentTableDivChat').html(content)
        }
    }).fail(function (error) {
        console.log(error);
    });

}