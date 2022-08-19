$(function(){

    // Datatable
    // $("#RecordTable").DataTable({
    //   "paging": true,
    //   "lengthChange": false,
    //   "searching": false,
    //   "autoWidth": false,
    //   "responsive": true,
    //   "aaSorting": [],
    //   "info" : false,
    //   "fnDrawCallback": function(oSettings) {
    //         if ($('#RecordTable tbody tr').length <= 11) {
    //             $('#RecordTable_wrapper div.dataTables_paginate').hide()
    //         }
    //     },
    //     "dom": '<"top"i>rt<"bottom"flp><"clear">'
    // });

    // $('#id_start_date_time,#id_end_date_time').datetimepicker({
    //     autoclose: true,
    //     todayBtn: true,
    //     format: "yyyy-mm-dd HH:ii",
    //     startDate: new Date(),
    // });
    // $('#id_date_of_birth').attr('autocomplete','off').datepicker({
    //     startView: 0,
    //     todayBtn: "linked",
    //     keyboardNavigation: false,
    //     forceParse: false,
    //     autoclose: true,
    //     changeMonth: true,
    //     changeYear: true,
    //     dateFormat: "yy-mm-dd",
    //     startDate: new Date(),
    // });

    $('.input-daterange').attr('autocomplete','off').datepicker({
        keyboardNavigation: false,
        forceParse: false,
        autoclose: true
    });

    $('.cls_filter').on('change', function() {
        $('#id-filter-form').submit();
    });
    $('.page-size').on('change', function() {
        $('input[name=page_size]').val($(this).val());
        $('#id-filter-form').submit();
    });

    $('.clear-filter').click(function() {
      var form = $('#id-filter-form');
      $('[name][type!=hidden]', form).val('').attr('disabled', true).trigger("chosen:updated");
      form.submit();
    });

    $(document).on('click', '.attendance-button', function(){
        url = $(this).data('url');
        data = {
                'action' : $(this).data('action'),
                'csrfmiddlewaretoken' : $(this).data('csrfmiddlewaretoken'),
            }
        $.post(url, data, function(response){
            if(response.success){
                $('attendance').html(response.data);
            } else {
                toastr.error(response.msg);
                if (response.data){
                    $('attendance').html(response.data);
                }
            }
        });
    });

    $(document).on('click', '.delete-notification', function(){
        obj = $(this)
        action = $(this).data('action');
        $.get(action, {}, function(response){
            obj.closest('li').remove();
            count = $('notificationcount').html();
            $('notificationcount').html(parseInt(count) - 1);
        });
    });

    $(document).on('click', '.page-link', function(e){
        e.preventDefault();
        page = $(this).attr('href').replace('?page=', '');
        $('input[name=page]').val(page)
        $('#id-filter-form').submit();
    });

    $(document).on('click', '.delete_record', function(){

        url = $(this).data('url');
        id = $(this).data('id')

        $.get(url, function(response){
          document.getElementById('form_html').innerHTML = response
          $('#DeleteRecordModel').modal('show');
        })
    });

});

function password_show_hide(id) {
    var obj = document.getElementById(id);
    var show_eye = document.getElementById(id+"_show_eye");
    var hide_eye = document.getElementById(id+"_hide_eye");
    hide_eye.classList.remove("d-none");
    if (obj.type === "password") {
        obj.type = "text";
        show_eye.style.display = "none";
        hide_eye.style.display = "block";
    } else {
        obj.type = "password";
        show_eye.style.display = "block";
        hide_eye.style.display = "none";
    }
}
