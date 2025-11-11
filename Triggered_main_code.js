function triggerCloudFunctionFreshsalesRegional() {
  
  var cloudFunctionUrl = "https://test-fetch-manager-details-28472539111.us-central1.run.app";

  var payload = {
    spreadsheet_id: "1iZQ2EK1KZ71m1ox7vpQ9v1yaTRsciK6vXHR1ks5ceYk",
    sheet_name: "Freshsales Data" 
  };

  var options = {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify(payload),
    headers: {
      "Accept": "application/json"
    },
    muteHttpExceptions: true
  };

  Logger.log("Sending payload: " + JSON.stringify(payload));

  try {
    var response = UrlFetchApp.fetch(cloudFunctionUrl, options);
    var code = response.getResponseCode();
    var body = response.getContentText();

    Logger.log("Response code: " + code);
    Logger.log("Response body: " + body);
    
  } catch (err) {
    Logger.log("Error calling cloud function: " + err.message);
  }
}

