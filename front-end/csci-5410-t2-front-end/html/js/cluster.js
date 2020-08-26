function getCluster() {
    newDiv = `
        <div class="card shadow mb-4">
            <div class="card-body" id="dummyDiv">
                <div class="table-responsive">
                    <table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">
                        <thead>
                            <tr>
                                <th>Cluster 1</th>
                                <th>Cluster 2</th>
                                <th>Cluster 3</th>
                            </tr>
                        </thead>
                        <tbody >
                            <tr>
                                <td>Aditya_assignment_1.txt</td>
                                <td>Monil_assignment_01.txt</td>
                                <td>Naitik_assignment_1.txt</td>
                            </tr>
                            <tr>
                                <td>Aditya_assignment_2.txt</td>
                                <td>Monil_lab_assignment_1.txt</td>
                                <td>Monil_Project_Specification.txt</td>
                            </tr>
                            <tr>
                                <td>Anshdeep_assignment_1.txt</td>
                                <td>Monil_assignment_5.txt</td>
                                <td>Naitik_assignment_5.txt</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>`;
    $('#dummytablediv').html(newDiv)

    // var settings = {
    //     "url": "https://safe-hamlet-70720.herokuapp.com/https://us-central1-csci-5410-a5.cloudfunctions.net/listfiles",
    //     "method": "GET",
    //     "timeout": 0,
    //     "headers": {
    //         "Content-Type": "application/json"
    //     },
    // };
    // $.ajax(settings).done(function (response) {
    //     console.log(response.length);
    //     for (var i = 0; i < response.length; i++) {
    //         var file_name = response[i][0];
    //         var centroid_details = response[i][1];
    //         var center_number = centroid_details.center_number;
    //         console.log(file_name, center_number)
    //     }

    // });
}