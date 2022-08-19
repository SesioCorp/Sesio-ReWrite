$(function(){

  /******************* Form Step JS  *******************/
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
          $target.show();
          $target.find('input:eq(0)').focus();
      }
  });

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
      // for (var i = 0; i < curInputs.length; i++) {
      //     if (!curInputs[i].validity.valid || curInputs[i].value == '') {
      //         isValid = false;
      //         $(curInputs[i]).addClass("is-invalid");
      //     }
      // }
      if (isValid) nextStepWizard.removeClass('disabled').trigger('click');
  });

  $('div.setup-panel div a.btn-success').trigger('click');

  /******************* Form Step JS End  *******************/

  /*************

    Input Filed validation, fetch and render the child question JS

  ****************/

  $('input').on('change', function(){
    question_id = parseInt($(this).attr('id').split("_")[2])
    preventivemaintainence_id = parseInt($(this).attr('preventivemaintainence'))
    asset_id = parseInt($(this).attr('assets'))
  });

  // Render child question on select change
  $(document).on('change', 'select', function(){
    obj = $(this);
    parent_answer_arr = obj.attr('fail_condtion_answer').toLocaleLowerCase().split(',');

    if(parent_answer_arr.includes(obj.val().toLocaleLowerCase())){
      append_obj(obj);
    } else {
      child_get_attr = "[parent_id=id_parent_"+obj.attr('id').split('_')[2]+"]"
      child_ele = $(child_get_attr)
      comment_element = document.getElementById(obj.attr('name')+"_"+obj.attr('device_id'));
      if(comment_element){
        comment_element.remove()
        comment_question_id = comment_element.getAttribute('comment_question_id').split('_')[2]
          post_data = {
            'csrfmiddlewaretoken': '{{ csrf_token }}',
            'pk':comment_question_id,
            'preventivemaintainence_id':obj.attr('preventivemaintainence_id'),
            'answer':obj.val(),
          }
          // $.post('{% url "inspection:question-delete-ajax" %}', post_data, function(response){
          //   console.log(response)
          // });
      }
      else{
        ques_id = "id_question_"+obj.attr('comment_question_id')
        ques_ele = document.getElementById(ques_id)
        if(ques_ele){
          ques_ele.parentElement.remove()
          post_data = {
            'csrfmiddlewaretoken': '{{ csrf_token }}',
            'pk':obj.attr('comment_question_id'),
            'preventivemaintainence_id':obj.attr('preventivemaintainence_id'),
            'answer':obj.val(),
          }
          // $.post('{% url "inspection:question-delete-ajax" %}', post_data, function(response){
          //   console.log(response)
          // });
        }
      }

      if(child_ele){
        child_ele.parent().remove()
      }
    }
  });

  // Render child question on radio change
  $(document).on('change', 'radio', function(){
    obj = $(this);
    parent_answer_arr = obj.attr('fail_condtion_answer').toLocaleLowerCase().split(',');

    if(parent_answer_arr.includes(obj.val().toLocaleLowerCase())){
      append_obj(obj);
    } else {
      child_get_attr = "[parent_id=id_parent_"+obj.attr('id').split('_')[2]+"]"
      child_ele = $(child_get_attr)
      comment_element = document.getElementById(obj.attr('name')+"_"+obj.attr('device_id'));
      if(comment_element){
        comment_element.remove()
        comment_question_id = comment_element.getAttribute('comment_question_id').split('_')[2]
          post_data = {
            'csrfmiddlewaretoken': '{{ csrf_token }}',
            'pk':comment_question_id,
            'preventivemaintainence_id':obj.attr('preventivemaintainence_id'),
            'answer':obj.val(),
          }
          $.post('{% url "inspection:question-delete-ajax" %}', post_data, function(response){
            console.log(response)
          });
      }
      else{
        ques_id = "id_question_"+obj.attr('comment_question_id')
        ques_ele = document.getElementById(ques_id)
        if(ques_ele){
          ques_ele.parentElement.remove()
          post_data = {
            'csrfmiddlewaretoken': '{{ csrf_token }}',
            'pk':obj.attr('comment_question_id'),
            'preventivemaintainence_id':obj.attr('preventivemaintainence_id'),
            'answer':obj.val(),
          }
          // $.post('{% url "inspection:question-delete-ajax" %}', post_data, function(response){
          //   console.log(response)
          // });
        }
      }

      if(child_ele){
        child_ele.parent().remove()
      }
    }
  });

  $("input[type='number']").on('input', function(){
    obj = $(this);
    ele = document.getElementById($(this).attr('id'));
    question_id = parseInt($(this).attr('id').split("_")[2]);
    // url = "{% url 'inspection:question-data' 0 %}".replace('/0/', "/"+question_id+"/");
    data = {"value": obj.val()}

    $.get(url, data, function(response){
      is_element_available = document.getElementsByClassName('warning-codes')
      if(response.status == 'fail'){
        if(is_element_available.length > 0){
          is_element_available[0].remove()
          warning_ele = document.createElement('div');
          warning_ele.className = "text-warning warning-codes";
          warning_ele.innerHTML = response.warning;
          ele.after(warning_ele);
          append_obj(obj)
        }
        else{
          warning_ele = document.createElement('div');
          warning_ele.className = "text-warning warning-codes";
          warning_ele.innerHTML = response.warning;
          ele.after(warning_ele);
          append_obj(obj)
        }
      }
      else{
        is_element_available = document.getElementsByClassName('warning-codes')
        is_element_available.length > 0 ? is_element_available[0].remove() : ''
        child_get_attr = "[parent_id=id_parent_"+obj.attr('id').split('_')[2]+"]"

        comment_element = document.getElementById(obj.attr('name')+"_"+obj.attr('device_id'));
        if(comment_element){
          comment_element.remove()
          comment_question_id = comment_element.getAttribute('comment_question_id').split('_')[2]
          post_data = {
            'csrfmiddlewaretoken': '{{ csrf_token }}',
            'pk':comment_question_id
          }
          $.post('{% url "inspection:question-delete-ajax" %}', post_data, function(response){
            console.log(response)
          });
        }
        else{
          ques_id = "id_question_"+obj.attr('comment_question_id')
          ques_ele = document.getElementById(ques_id)
          if(ques_ele){
            ques_ele.parentElement.remove()
            post_data = {
              'csrfmiddlewaretoken': '{{ csrf_token }}',
              'pk':obj.attr('comment_question_id')
            }
            $.post('{% url "inspection:question-delete-ajax" %}', post_data, function(response){
              console.log(response)
            });
          }

        }

        child_ele = $(child_get_attr)
        if(child_ele){
          child_ele.parent().remove()
        }
      }
    });
  });

  // Render the comment in comments category
  function append_obj(obj){
      child_get_attr = "[parent_id=id_parent_"+obj.attr('id').split('_')[2]+"]"
      child_ele = $(child_get_attr)
      if (child_ele.length==0) {
        id_attr = obj.attr('id')
        question_id = parseInt(obj.attr('id').split("_")[2]);
        inspection_uuid = obj.attr('inspection_uuid');
        device_name = obj.attr('device_name');
        device_id = parseInt(obj.attr('device_id'));
        step = '{{step}}';
        kwargs = {
          'question_id': question_id,
          'answer': obj.val(),
          'inspection_uuid': inspection_uuid,
          'device_name': device_name,
          'device_id': device_id,
          'step': step,
        };

        if (parseInt(step) > 0){
          url = "{% url 'inspection:inspection-question-answer-form-step' uuid='str' pk=0 step=0%}".replace('/str/0/0/', "/"+inspection_uuid+"/"+device_id+"/"+step+"/");
        }
        else {
          url = "{% url 'inspection:inspection-question-answer-form' uuid='str' pk=0 %}".replace('/str/0/', "/"+inspection_uuid+"/"+device_id+"/");
        }

        $.get(url, kwargs, function(response){
          ele = document.createElement('div');
          ele.innerHTML = response;
          parent_element =  document.getElementById(id_attr);
          parent_element.parentElement.after(ele);

          post_data = {
            'csrfmiddlewaretoken': '{{ csrf_token }}',
            "entity" : obj.attr('entity_id'),
            "device" : device_id,
            "category" :  obj.attr('comment_category_id'),
            "question_text" :  "Fail comments for "+obj.attr('question_text'),
            "answer_type" : "text",
            'parent' : question_id,
            'question_set_id' : obj.attr('question_set_id')
          }

          $.post('{% url "inspection:question-create-ajax" %}', post_data, function(response){
            last_step =  document.getElementById(obj.parent().parent().data('step_last'));
            last_step_element = last_step.getElementsByClassName('card-body');
            new_div_elemet = document.createElement('div');
            new_div_elemet.setAttribute("id", obj.attr('name')+"_"+obj.attr('device_id'));
            new_div_elemet.innerHTML = response
            last_step_element[0].append(new_div_elemet)
            new_div_elemet.setAttribute('comment_question_id', new_div_elemet.firstElementChild.getAttribute('id'));
          });
          // Apeend comments fr question at last category

        });

      }
  }

  /************* End  ****************/


  $('.save_and_exit').click(function(e){
    $('#question_answer_form').append('<input type="hidden" name="save_and_exit" value="true" />')
    $('#question_answer_form').submit()
  });


});
