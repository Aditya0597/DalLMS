function analyze() {
    var settings = {
        "url": "https://safe-hamlet-70720.herokuapp.com/https://aavhv0mecc.execute-api.us-east-1.amazonaws.com/default/lmsUserChatSentimentAnalysis",
        "method": "GET",
        "timeout": 0,
        "headers": { "Content-Type": "application/json" }
    };
    $.ajax(settings).done(function (response) {
        if (response.statusCode) {
            newDiv = `<p>Nothing to analyze</p>`
            $('#dummyDiv').html(newDiv)
        } else {
            var json_resp = JSON.stringify(response)
            var parsed_response = JSON.parse(json_resp)
            var overall_sentiment = parsed_response[0].sentiment_analysis.Sentiment
            var sentiment_score = parsed_response[0].sentiment_analysis.SentimentScore
            var Positive = sentiment_score.Positive
            var Negative = sentiment_score.Negative
            var Neutral = sentiment_score.Neutral
            var Mixed = sentiment_score.Mixed
            console.log(overall_sentiment)
            console.log(Positive, Negative, Neutral, Mixed)
            newDiv = `
            <div class="card shadow mb-4">
                <div class="card-body" id="dummyDiv">
                    <div class="table-responsive">
                        <table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">
                            <thead>
                                <tr>
                                    <th>Score: Positive</th>
                                    <th>Score: Negative</th>
                                    <th>Score: Neutral</th>
                                    <th>Score: Mixed</th>
                                    <th>Overall Sentiment</th>
                                </tr>
                            </thead>
                            <tbody >
                                <tr>
                                    <td>${Positive}</td>
                                    <td>${Negative}</td>
                                    <td>${Neutral}</td>
                                    <td>${Mixed}</td>
                                    <td>${overall_sentiment}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>`;
            $('#dummyDiv').html(newDiv)
        }
    });
}
