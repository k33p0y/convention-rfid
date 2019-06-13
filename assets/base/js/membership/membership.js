$(function (){
    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            datatype: 'json',
            beforeSend: function (){
                // show modal
                $("#modal-membership").modal("show");
            },
            success: function (data) {
                // append patient form to modal
                $("#modal-membership .modal-content").html(data.html_form);
            },
            error: function (xhr, status, error) {
                $("#modal-membership").modal("hide");
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
                    $("#modal-membership").modal("hide");
    
                    // Success alert
                    Swal.fire({
                        // position: 'top-end',
                        type: 'success',
                        title: 'Membership type saved!',
                        showConfirmButton: false,
                        timer: 2000
                    });
    
                    // reload datatable
                    $('#table-membership').DataTable().ajax.reload();
                }
                else {
                    // show forms errors in modal
                    $("#modal-membership .modal-content").html(data.html_form);
                }
            },
            error: function (xhr, status, error) {
                $("#modal-membership").modal("hide");
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

    // Create membership
    $(".js-create-membership").click(loadForm);
    $("#modal-membership").on("submit", ".js-membership-create-form", saveForm);

    // Update membership
    $("#table-membership").on("click", ".js-update-membership", loadForm);
    $("#modal-membership").on("submit", ".js-membership-update-form", saveForm);
});