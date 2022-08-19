$(function(){

    var navListItems = $('div.setup-panel div a'),
        allWells = $('.setup-content'),
        allNextBtn = $('.nextBtn');
        allPrevBtn = $('.prevBtn');

    allWells.hide();
    navListItems.click(function (e) {
        e.preventDefault();
        var $target = $($(this).attr('href')),
            $item = $(this);

        if (!$item.hasClass('disabled')) {
            navListItems.removeClass('btn-success').addClass('btn-default')
            $item.removeClass('btn-default').addClass('btn-success');
            allWells.hide();
            // if ($target.data('cat_name') == "No Flow Inspection | EP6"){
            //   device_inspection_id = $target.data('device_inspection_id');
            //   csrfmiddlewaretoken = "{{ csrf_token }}"
            //   data = {"csrfmiddlewaretoken":csrfmiddlewaretoken, 'device_inspection_id':device_inspection_id, "is_update": "False"}

            //   $.post("{% url 'inspection:inspection-device-kwargs-update' %}", data, function(response){
            //       update_time()
            //   });
            // }
            $target.show();
            $target.find('input:eq(0)').focus();
        }
    });
    // function update_time() {
    //   var currentDate = new Date(new Date().getTime() + 10*60000);
    //   var endTime = new Date(currentDate);
    //   $('#clockdiv').countdown(endTime, function(event) {
    //     $("#continue-step-4").attr("disabled", true);
    //     $(this).html(event.strftime('%M:%S'));
    //   }).on('finish.countdown', function(){
    //     device_inspection_id = $('#step-4').data('device_inspection_id');
    //     csrfmiddlewaretoken = "{{ csrf_token }}"
    //     data = {"csrfmiddlewaretoken":csrfmiddlewaretoken, 'device_inspection_id':device_inspection_id, "is_update": "True"}
    //     $.post("{% url 'inspection:inspection-device-kwargs-update' %}", data, function(response){
    //       $("#continue-step-4").attr("disabled", false);
    //     });

    //   });
    // }

    allNextBtn.click(function () {
        var curStep = $(this).closest(".setup-content"),
            curStepBtn = curStep.attr("id"),
            nextStepWizard = $('div.setup-panel div a[href="#' + curStepBtn + '"]').parent().next().children("a"),
            curInputs = curStep.find("input[type='text'], input[type='number'], input[type='url'], input[type='radio'], input[type='file'], select, textarea"),

            isValid = true;
        $("input").removeClass("is-invalid");
        var delay = 0;
        var offset = 150;
        for (var i = 0; i < curInputs.length; i++) {
            if (!curInputs[i].validity.valid || curInputs[i].value == ''){
              if (curInputs[i].closest('div').children[3] == null) {
                isValid = false;
                $(curInputs[i]).addClass("is-invalid");
                $('html, body').animate({scrollTop: $($(".is-invalid")[0]).offset().top - offset }, delay);
              }
            }
            else{
                if($(curInputs[i]).hasClass("is-invalid")){
                  $(curInputs[i]).removeClass("is-invalid");
                }
                $(curInputs[i]).addClass("is-valid");
            }
        }
        if (isValid) nextStepWizard.removeClass('disabled').trigger('click');
    });

    allPrevBtn.click(function () {

        var curStep = $(this).closest(".setup-content"),
            curStepBtn = curStep.attr("id"),
            nextStepWizard = $('div.setup-panel div a[href="#' + curStepBtn + '"]').parent().prev().children("a"),
            curInputs = curStep.find("input[type='text'],input[type='url'], input[type='number'], input[type='file'], input[type='radio'], select, textarea"),
            isValid = true;
        $("input").removeClass("is-invalid");
        if (isValid) nextStepWizard.removeClass('disabled').trigger('click');
    });

    $('div.setup-panel div a.btn-success').trigger('click');
  });
