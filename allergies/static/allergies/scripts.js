function openLink(link) {
    if (link == "") {
        return false;
    } else if (link.includes(".pdf")) {
        document.getElementById("pdf-viewer").setAttribute("data", link);
        document.getElementById("alt_pdf_link").setAttribute("href", link);
        document.getElementById("pdf-div").style.visibility = "visible";
    } else {
        document.getElementById("pdf-div").style.visibility = "hidden";
        var popup = window.open(link, '_blank');
	    popupBlockerChecker.check(popup);
    }
    return false;
}

/*
function render_pdf(url) {
    var pdfjsLib = window['pdfjs-dist/build/pdf'];

    // The workerSrc property shall be specified.
    pdfjsLib.GlobalWorkerOptions.workerSrc = '//mozilla.github.io/pdf.js/build/pdf.worker.js';

    // Asynchronous download of PDF
    var loadingTask = pdfjsLib.getDocument(url);
    loadingTask.promise.then(function(pdf) {
        console.log('PDF loaded');
    
        // Fetch the first page
        var pageNumber = 1;
        pdf.getPage(pageNumber).then(function(page) {
            console.log('Page loaded');
            
            var scale = 1.5;
            var viewport = page.getViewport({scale: scale});

            // Prepare canvas using PDF page dimensions
            var canvas = document.getElementById('the-canvas');
            var context = canvas.getContext('2d');
            canvas.height = viewport.height;
            canvas.width = viewport.width;

            // Render PDF page into canvas context
            var renderContext = {
                canvasContext: context,
                viewport: viewport
            };
            var renderTask = page.render(renderContext);
            renderTask.promise.then(function () {
                console.log('Page rendered');
            });
        });
    }, function (reason) {
    // PDF loading error
    console.error(reason);
    });
}*/

$(document).ready(function() {
    setTimeout(function() {
        $(".notification").fadeOut(1500);
    }, 5000);
});

function recaptcha_callback_request() {
    $("#request_submit").removeAttr("disabled");
}

function recaptcha_callback_email() {
    $("#email_submit").removeAttr("disabled");
}

var popupBlockerChecker = {
	check: function(popup_window){
		var _scope = this;
		if (popup_window) {
			if(/chrome/.test(navigator.userAgent.toLowerCase())){
				setTimeout(function () {
					_scope._is_popup_blocked(_scope, popup_window);
				},200);
			}else{
				popup_window.onload = function (){
					_scope._is_popup_blocked(_scope, popup_window);
				};
			}
		}else{
			_scope._displayError();
		}
	},
	_is_popup_blocked: function(scope, popup_window){
		if ((popup_window.innerHeight > 0) == false){ scope._displayError(); }
	},
	_displayError: function(){
		alert("Popup blocker is enabled! Please add this site to your exception list to enable full functionality.");
	}
};

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

    // Configure typeahead
    /*
    $("#q").typeahead({
        hint: false,
        highlight: false,
        minLength: 1
    },
    {
        display: function(suggestion) { return null; },
        limit: 10,
        source: search,
        templates: {
            suggestion: Handlebars.compile(
                '<div>' +
                '{{restaurant_name}}' +
                '</div>'
            )
        }
    });*/

    /*$("#q").on("typeahead:selected", function(eventObject, suggestion, name) {

        // Open document user selects from typeahead
        var popup2 = window.open(suggestion.rest_link, '_blank');
		popupBlockerChecker.check(popup2);
    });*/

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
