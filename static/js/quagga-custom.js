$('#barcodeUploadFile').on('click', function(){
    debugger
    console.log('Scanner Starting..................')
    scanner()
});

function scanner(){
    Quagga.init({
        inputStream: {
            name: "Live",
            type: "LiveStream",
            target: document.querySelector('#scanner-container')
        },
        decoder: {
            readers: [
                'code_128_reader',
            ]
        }
        }, function (err) {
            if (err) {
                console.log(err);
                // setResult(err);
                err = err.toString();
                if (err.search("NotFoundError")) {
                    print('No camera found. The user is probably in an office environment.\n Redirect to previous orders or show a background image of sorts.')
                } else if (err.search("NotAllowedError")) {
                    print('The user has blocked the permission request.\n We should ask them again just to be sure or redirect them.')
                } else {
                    // Some other error.
                }
                return;
            }
        // Hide the preview before it's fully initialised.
        $('#scanner-container').show();
        // setResult("Initialization finished. Ready to start");
        console.log("Initialization finished. Ready to start");
        Quagga.start();
        // initializeQuaggaFeedback();
    });

    Quagga.onDetected(function(result) {
        var code = result.codeResult.code;
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        $.ajax({
            url: "{% url 'dashboard:scan-ajax-view' %}",
            type: "POST",
            data: { 'code': parseInt(code) },
            dataType: "json",
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            success: function (response) {
                if (response.assets != null) {
                    window.location.href = 'asset/information/' + '?' + parseInt(code)
                }
                else {
                    $('#ajaxModal').modal('toggle')
                }
            }
        })

    });
}

$('#scanner-off').on('click', function(){
    console.log('Scanner Starting..................')
    Quagga.stop()
    const myNode = document.getElementById("scanner-container");
    myNode.innerHTML = '';
});
