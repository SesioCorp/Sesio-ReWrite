 function selectBarcodeType(selectedTypeUrl, selectedTypeTitle) {
        $('#barcodeTypeDdl').val(selectedTypeUrl);
        $('#barcodeTypeDdl').html(selectedTypeTitle);
    }

    function selectQuality(index) {
        $('#recognizeQualityContainer>button').removeClass("selected");
        $('#recognizeQualityContainer>button:nth-child(' + index + ')').addClass("selected");
    }

    function selectCamera(btnIndex) {
        $('#inputTypesContainer>.btn').removeClass("selected");
        $('#inputTypesContainer>.btn:nth-child(' + btnIndex + ')').addClass("selected");

        if ('mediaDevices' in navigator) {
            if (btnIndex == 3/*camera*/) {
                startWebcam();
            } else {
                stopWebcam();
            }
        }
    }

    function makeErrorMessage(xhr) {
        let message = null;
        if (xhr.status == 0) {
            message = `Connection error: ${xhr.statusText}`;
        } else {
            message = `${xhr.statusText} ${xhr.status}: ${xhr.responseText}`;
        }

        return message;
    }

    async function postBarcodeRecognize(postData) {
        let result = await new Promise((resolve, reject) => {
            $.ajax({
                type: "POST",
                url: apiOrigin() + "barcode/recognize/apiRequestRecognize",
                contentType: false,
                processData: false,
                data: postData
            })
            .done(function (result) {
                resolve(result);
            })
            .fail(function (jqXHR) {
                reject(new Error(makeErrorMessage(jqXHR)));
            })
        });

        if (!result.success) {
            throw new Error(result.errorMsg);
        }

        return result.recognizeResultToken;
    };

    async function waitSec(seconds) {
        return new Promise(resolve => setTimeout(resolve, 1000 * seconds));
    };

    function getWaitTimeSec(curAttempt) {
        if (curAttempt === 0) {
            // To prevent too fast laser animation flicker
            return 0.5;
        }
        if (curAttempt < 10) {
            return 0.5;
        }
        return 2;
    };

    async function tryGetResult(token) {
        return new Promise((resolve, reject) => {
            $.ajax({
                type: 'GET',
                url: apiOrigin() + "barcode\/recognize/recognizeresult/" + token + "?timestamp=" + Date.now(),
            })
            .done(function (result) {
                resolve(result);
            })
            .fail(function (jqXHR) {
                const err = new Error(makeErrorMessage(jqXHR));
                err.status = jqXHR.status;
                reject(err);
            });
        });
    }


    RecognitonStarted = null;
    function recognizeBarcode() {
        if (!window.FormData) {
            // FormData is not supported
            GaSendEvent({
                'eventCategory': 'Barcode',
                'eventAction': 'OldBrowser',
                'eventLabel': navigator.userAgent,
                nonInteraction: true
            });
            showToast("Something went wrong! Please try again.", $("#inputTypesContainer"));

            return;
        }

        var barcodetypeUrl = $('#barcodeTypeDdl').val();
        var quality = $('#recognizeQualityContainer>button.selected').val();

        var fileBase64 = document.getElementById("imgToRecognize").src;

        if (!fileBase64) {
            GaSendEvent({
                'eventCategory': 'Barcode',
                'eventAction': 'ImageNotLoaded',
                nonInteraction: true
            });
            showToast("Please upload barcode image.", $("#inputTypesContainer"));

            return;
        }

        GaSendEvent({
            'eventCategory': 'Barcode',
            'eventAction': 'Recognize',
            'eventLabel': 'Q:' + quality,
            'eventValue': fileBase64.length
        });

        var data = new FormData();
        data.append("type", barcodetypeUrl);
        data.append("quality", quality);
        data.append("fileBase64", fileBase64);
        showStateRecognizing();
        RecognitonStarted = Date.now();
        $.ajax({
            type: "POST",
            url: apiOrigin() + "barcode/recognize/recognizebarcode?culture=en",
            contentType: false,
            processData: false,
            data: data
        }).done(function (result) {
            if (!result.success) {
                GaSendEvent({
                    'eventCategory': 'Barcode',
                    'eventAction': 'NotRecognized',
                    'eventLabel': result.errorMsg,
                    'eventValue': (Date.now() - RecognitonStarted) / 1000,
                    nonInteraction: true,
                    transport: 'beacon'
                });
                setStateUnsuccessfulRecognition(result.errorMsg);
            } else {
                GaSendEvent({
                    'eventCategory': 'Barcode',
                    'eventAction': 'Recognized',
                    'eventLabel': 'Q:'+ quality +' Got:'+ result.foundBarcodesCount,
                    'eventValue': (Date.now() - RecognitonStarted) / 1000,
                    nonInteraction: true,
                    transport: 'beacon'
                });
                if (result.foundBarcodesCount > 0) {
                    setStateRecognized(result.html);
                } else {
                    setStateNoBarcodesRecognized(result.html);
                }
            }
        }).fail(function (jqXHR) {
            const message = makeErrorMessage(jqXHR);
            GaSendEvent({
                'eventCategory': 'Barcode',
                'eventAction': 'ServerError',
                'eventLabel': message,
                'eventValue': jqXHR.status,
                nonInteraction: true,
                transport: 'beacon'
            });
            setStateServerError(message);
        }).always(function () {
            $("#laser-scan").hide();
            RecognitonStarted = null;
        });
    }

    function getCurrentQuality() {
        return parseInt($('#recognizeQualityContainer>button.selected').val(), 10);
    }

    function navigateTo(hash) {
        if (window.location.hash === hash) {
            return;
        }

        window.location.hash = hash;

        var gaPage = window.location.pathname + window.location.hash;
        if ('ga' in window) {
            try {
                window.ga('set', 'page', gaPage);
                window.ga('send', 'pageview');
            } catch (err) {}
        }
    }

    window.onpopstate = function() {
        cancelAsyncRecognitionProcess();
        if (window.location.hash !== "" && window.location.hash !== "#" && !window.location.hash.startsWith("#/")) {
            return;
        }

        if (!$("#imgToRecognize").attr("src")) {
            // When user returns to page, image could be destroyed
            resetState();
            return;
        }

        if (window.location.hash.startsWith("#/settings")) {
            if (window.location.hash === "#/settings/better") {
                showToast("Select the type of barcode for better recognition", $("#barcodeTypeDdl"));
            }
            showStateImageLoaded();
            return;
        }

        if (window.location.hash === "#/recognized") {
            if ($("#recognitionResult").html()) {
                showStateRecognized();
            } else {
                resetState();
            }
            return;
        }

        if (window.location.hash === "#/nobarcodes") {
            if ($("#errorMessage").html()) {
                showStateUnsuccessfulRecognition();
            } else {
                showStateNoBarcodes();
            }
            return;
        }

        if (window.location.hash === "#/error") {
            if ($("#errorMessage").html()) {
                showStateServerError();
            } else {
                resetState();
            }
            return;
        }

        showStateStart();
    };

    function resetState() {
        navigateTo("");
    }

    function setStateImageLoaded(imgSrc, fileName) {
        document.getElementById("imgToRecognize").src = imgSrc;
        document.getElementById("imgToRecognize").dataset.fileName = fileName;
        $("#errorMessage").html("");
        $("#recognitionResult").html("");
        navigateTo("#/settings");
    }

    function setStateRecognized(htmlSuccessful) {
        $("#errorMessage").html("");
        $("#recognitionResult").html(htmlSuccessful);
        navigateTo("#/recognized");
    }

    function setStateNoBarcodesRecognized(htmlNoBarcodes) {
        $("#errorMessage").html("");
        $("#recognitionResult").html(htmlNoBarcodes);
        navigateTo("#/nobarcodes");
    }

    function setStateUnsuccessfulRecognition(htmlUnsuccessful) {
        $("#errorMessage").html(htmlUnsuccessful);
        $("#recognitionResult").html(htmlUnsuccessful);
        navigateTo("#/nobarcodes");
    }

    WindowIsAboutToUnload = null;
    function setStateServerError(errorText) {
        if (WindowIsAboutToUnload) {
            console.debug("Ignoring error:", errorText);
            return;
        }
        $('#errorMessage').text(errorText);
        $('#recognitionResult').text('Oops! An error has occurred.');
        navigateTo("#/error");
    }

    function cancelAsyncRecognitionProcess() {
        $("#laser-scan").hide();
        AsyncRecognitionStarted = null;
    }


    function showStateStart() {
        $("#inputTypesContainer").show();
        $("#drop-zone").show();

        $("#anotherImage").hide();
        $("#image-container").hide();
        $("#settings").hide();
        $("#recognitionResult").hide();
        $("#changeSettings").hide();
        $("#tryBetterQuality").hide();

        window.scrollTo(0, 0);
    }

    function showStateImageLoaded() {
        $("#inputTypesContainer").hide();
        $("#drop-zone").hide();

        $("#anotherImage").show();
        $("#image-container").show();
        $("#settings").show();

        $("#recognitionResult").hide();
        $("#changeSettings").hide();
        $("#tryBetterQuality").hide();
        setTimeout(() => UniversalScrollIntoViewBottom(document.getElementById("ToS")), 500);
    }

    function showStateRecognizing() {
        /// Temporary state available only from showStateImageLoaded
        $("#anotherImage").hide();
        $("#settings").hide();

        $("#laser-scan").show();
        setTimeout(() => UniversalScrollIntoViewBottom(document.getElementById("imgToRecognize")), 0);
    }

    function showStateRecognized() {
        $("#inputTypesContainer").hide();

        $("#anotherImage").show();
        $("#settings").hide();

        $("#recognitionResult").show();
        $("#changeSettings").show();
        $("#tryBetterQuality").hide();
        setTimeout(() => UniversalScrollIntoViewBottom(document.getElementById("changeSettings")), 0);
    }

    function showStateNoBarcodes() {
        $("#inputTypesContainer").hide();
        $("#anotherImage").show();
        $("#settings").hide();

        $("#recognitionResult").show();

        if (getCurrentQuality() < 3) {
            $("#changeSettings").hide();
            $("#tryBetterQuality").show();
            setTimeout(() => UniversalScrollIntoViewBottom(document.getElementById("tryBetterQuality")), 0);
        } else {
            // The best qaulity already selected
            $("#changeSettings").show();
            $("#tryBetterQuality").hide();
            setTimeout(() => UniversalScrollIntoViewBottom(document.getElementById("changeSettings")), 0);
        }
    }

    function showStateUnsuccessfulRecognition() {
        $("#inputTypesContainer").hide();
        $("#drop-zone").hide();
        $("#anotherImage").show();
        $("#settings").hide();

        $("#recognitionResult").show();
        $("#changeSettings").hide();
        $("#tryBetterQuality").hide();

        $("#reportErrorModal").modal("show");
    }

    function showStateServerError() {
        $("#inputTypesContainer").hide();
        $("#drop-zone").hide();
        $("#anotherImage").show();
        $("#settings").hide();

        $("#recognitionResult").show();
        $("#changeSettings").show();
        $("#tryBetterQuality").hide();

        setTimeout(() => UniversalScrollIntoViewBottom(document.getElementById("changeSettings")), 0);

        $("#reportErrorModal").modal("show");
    }

    function anotherImage() {
        navigateTo("");
    }

    function changeSettings() {
        navigateTo("#/settings");
    }

    function tryBetterQuality() {
        var currentQuality = getCurrentQuality();
        if (currentQuality < 3) {
            selectQuality(currentQuality + 1);
        }

        navigateTo("#/settings/better");
    }

    function fallbackFromCameraToCaptureImage() {
        var captureFileInput = document.getElementById('barcodeCaptureFile');
        captureFileInput.disabled = false;
        captureFileInput.labels.forEach((l) => l.removeAttribute("onclick"));
    }

    $(document).ready(function () {
        if (!'mediaDevices' in navigator) {
            // Fallback to old capture API
            fallbackFromCameraToCaptureImage();
        }
        if (isMobile()) {
            // Use native capture interface on mobile devices
            fallbackFromCameraToCaptureImage();
            $("#drop-zone").hide();
        }

        $("#barcodeUploadFile").change(function (e) {
            if (e.target.files.length > 0) {
                var file = e.target.files[0];
                GaSendEvent({
                    'eventCategory': 'Barcode',
                    'eventAction': 'UploadFile',
                    'eventLabel': 'FileSize',
                    'eventValue': file.size
                });
                drawFile(file, e, file.name);
            }
        });
        $("#barcodeCaptureFile").change(function (e) {
            if (e.target.files.length > 0) {
                var file = e.target.files[0];
                GaSendEvent({
                    'eventCategory': 'Barcode',
                    'eventAction': 'CaptureFile',
                    'eventLabel': 'FileSize',
                    'eventValue': file.size
                });
                drawFile(file, e, 'image.png');
            }
        });


        document.addEventListener("visibilitychange", function() {
            if (RecognitonStarted == null || document.visibilityState === 'visible') {
                return;
            }

            GaSendEvent({
                'eventCategory': 'Barcode',
                'eventAction': 'VisibilityChangedWhileRecognition',
                'eventLabel': document.visibilityState,
                'eventValue': (Date.now() - RecognitonStarted) / 1000,
                nonInteraction: true,
                transport: 'beacon'
            });
        });

        document.addEventListener("beforeunload", function(event) {
            WindowIsAboutToUnload = true;
        });

        window.onpopstate();
    });

    function isMobile() {
        let check = false;
        (function (a) { if (/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(a) || /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0, 4))) check = true; })(navigator.userAgent || navigator.vendor || window.opera);
        return check;
    }

    function drawFile(file, inputChangeEvent, fileName) {
        if (FileReader && file) {
            var fr = new FileReader();
            fr.onload = function () {
                $("#videoDiv").hide();
                setStateImageLoaded(fr.result, fileName);
                if (inputChangeEvent) {
                    inputChangeEvent.target.value = '';
                }
            }
            fr.readAsDataURL(file);
        }
    }

    var video;

    function startWebcam() {
        if (!video) {
            video = document.getElementById('video');
        }
        document.getElementById("imgToRecognize").src = "";
        document.getElementById("imgToRecognize").dataset.fileName = "";
        $("#image-container").hide();

        if ('mediaDevices' in navigator) {
            navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" }, audio: false })
                .then((stream) => {
                    video.srcObject = stream;
                    $("#videoDiv").show();
                    video.play();
                    setTimeout(() => UniversalScrollIntoViewBottom(document.querySelector("#videoDiv button")), 0);
                })
                .catch(function (err) {
                    console.log(err);
                    selectCamera(1);
                    // Fallback to capture image API
                    fallbackFromCameraToCaptureImage();
                });
        } else {
            console.log("getUserMedia not supported");
        }
    }

    function stopWebcam() {
        if (video && video.srcObject) {
            video.srcObject.getVideoTracks().forEach(track => track.stop());
        }
        $("#videoDiv").hide();
        $("#drop-zone").show();
    }

    function snapshot() {
        GaSendEvent({
            'eventCategory': 'Barcode',
            'eventAction': 'Snapshot'
        });
        var canvas = document.createElement("canvas");
        canvas.width = video.clientWidth;
        canvas.height = video.clientHeight;
        canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
        stopWebcam();
        setStateImageLoaded(canvas.toDataURL(), 'image.png');
    }

    function copyToClipboard(textareaId) {
        var text = document.getElementById(textareaId);
        text.select();
        document.execCommand('copy');
        showToast("Text copied to clipboard", $("#recognitionResult"));
    }

    function isFilesAcceptable(files) {
        if (!files || !files.length || files.length <= 0) {
            return false;
        }

        return /^image\/(bmp|gif|jpeg|png)$/.test(files[0].type);
    }

    var DragEnterLeaveCounter = 0;

    function ondragenter_handler(event) {
        event.stopPropagation();
        event.preventDefault();
        DragEnterLeaveCounter++;

        if (DragEnterLeaveCounter <= 1) {
            $("#drop-here").show();
        }
    }

    function ondragleave_handler(event) {
        event.stopPropagation();
        event.preventDefault();
        DragEnterLeaveCounter--;

        if (DragEnterLeaveCounter === 0) {
            reset_drag();
        }
    }

    function reset_drag() {
        DragEnterLeaveCounter = 0;
        $("#drop-here").hide();
    }

    function ondragover_handler(event) {
        event.stopPropagation();
        event.preventDefault();

        if (!event || !event.dataTransfer) {
            return;
        }
        event.dataTransfer.dropEffect = isFilesAcceptable(event.dataTransfer.items) ? 'copy' : 'none';
    }

    function ondrop_handler(event) {
        event.stopPropagation();
        event.preventDefault();

        if (!event || !event.dataTransfer) {
            return;
        }

        if (!isFilesAcceptable(event.dataTransfer.files)) {
            return;
        }

        var firstFile = event.dataTransfer.files[0];
        GaSendEvent({
            'eventCategory': 'Barcode',
            'eventAction': 'DroppedFile',
            'eventLabel': 'FileSize',
            'eventValue': firstFile.size
        });
        drawFile(firstFile, null, firstFile.name);
        reset_drag();
    }
