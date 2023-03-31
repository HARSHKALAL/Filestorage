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

function ajaxGetRequest(token, url, successCallback) {
    $.ajax({
        type: "GET",
        headers: { "Authorization": `Token ${token}` },
        url: url,
        success: successCallback,
    });
}

function ajaxPostAuthenticationRequest(token, url, data, successCallback) {
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": "{{csrf_token}}", "Authorization": `Token ${token}` },
        url: url,
        data: data,
        success: successCallback,
    });
}
