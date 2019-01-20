function recaptcha_callback_request() {
    $("#request_submit").removeAttr("disabled");
}

function recaptcha_callback_email() {
    $("#email_submit").removeAttr("disabled");
}

function search(query, syncResults, asyncResults)
{
    // Get places matching query (asynchronously)
    let parameters = {
        q: query
    };

    $.getJSON("../lookup", parameters, function(data, textStatus, jqXHR) {

        // Call typeahead's callback with search results (i.e., places)
        asyncResults(data);
    });
}

$(document).ready(function() {
    setTimeout(function() {
        $(".notification").fadeOut(1500);
    }, 5000);
    $("#rstrnt").change(function() {
        var link = $("#rstrnt option:selected").val();
        if (link == "") {
            return false;
        }
        else if (link.includes(".pdf")) {
            $("#pdf-viewer").attr("data", link + "?#view=FitH");
            $("#alt_pdf_link").attr("href", link + "?#view=FitH");
            $("#pdf-div").show();
        }
        else {
            $("#pdf-div").hide();
            var win = window.open(link, "_blank");
            win.focus();
        }
        return false;
    });
});
