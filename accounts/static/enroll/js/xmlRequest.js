function ajaxPostRequest(url, data, errorCallback, successCallback) {
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": "{{csrf_token}}" },
        url: url,
        data: data,
        error: errorCallback,
        success: successCallback,
    });
}


function ajaxGetRequest(method, token, url, data, errorCallback, successCallback) {
    $.ajax({
        type: method,
        headers: { "X-CSRFToken": token },
        url: url,
        data: data,
        error: errorCallback,
        success: successCallback,
    });
}




