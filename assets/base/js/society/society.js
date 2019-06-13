$(function (){
    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            datatype: 'json',
            beforeSend: function (){
                // show modal
                $("#modal-society").modal("show");
            },
            success: function (data) {
                // append patient form to modal
                $("#modal-society .modal-content").html(data.html_form);
            },
            error: function (xhr, status, error) {
                $("#modal-society").modal("hide");
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
                    $("#modal-society").modal("hide");
    
                    // Success alert
                    Swal.fire({
                        // position: 'top-end',
                        type: 'success',
                        title: 'Society saved!',
                        showConfirmButton: false,
                        timer: 2000
                    });
    
                    // reload datatable
                    $('#table-society').DataTable().ajax.reload();
                }
                else {
                    // show forms errors in modal
                    $("#modal-society .modal-content").html(data.html_form);
                }
            },
            error: function (xhr, status, error) {
                $("#modal-society").modal("hide");
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

    // Create society
    $(".js-create-society").click(loadForm);
    $("#modal-society").on("submit", ".js-society-create-form", saveForm);

    // Update society
    $("#table-society").on("click", ".js-update-society", loadForm);
    $("#modal-society").on("submit", ".js-society-update-form", saveForm);
});