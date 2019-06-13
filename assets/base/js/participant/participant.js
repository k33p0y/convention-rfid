$(function (){
    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            datatype: 'json',
            beforeSend: function (){
                // show modal
                $("#modal-participant").modal("show");
            },
            success: function (data) {
                // append patient form to modal
                $("#modal-participant .modal-content").html(data.html_form);
            },
            error: function (xhr, status, error) {
                $("#modal-participant").modal("hide");
                Swal.fire({
                    type: 'error',
                    title: 'Oops...',
                    text: error,
                    // footer: '<a href>Why do I have this issue?</a>'
                })
            }
        });
    };

    var saveForm = function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#modal-participant").modal("hide");
    
                    // Success alert
                    Swal.fire({
                        // position: 'top-end',
                        type: 'success',
                        title: 'Participant saved!',
                        showConfirmButton: false,
                        timer: 2000
                    });
    
                    // reload datatable
                    $('#table-participant').DataTable().ajax.reload();
                }
                else {
                    // show forms errors in modal
                    $("#modal-participant .modal-content").html(data.html_form);
                }
            },
            error: function (xhr, status, error) {
                $("#modal-participant").modal("hide");
                Swal.fire({
                    type: 'error',
                    title: 'Oops...',
                    text: error,
                    // footer: '<a href>Why do I have this issue?</a>'
                })
            }
        });
        return false;
    };

    // Create participant
    $(".js-create-participant").click(loadForm);
    $("#modal-participant").on("submit", ".js-participant-create-form", saveForm);

    // Update participant
    $("#table-participant").on("click", ".js-update-participant", loadForm);
    $("#modal-participant").on("submit", ".js-participant-update-form", saveForm);
});