$(function (){
    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            datatype: 'json',
            beforeSend: function (){
                // show modal
                $("#modal-convention").modal("show");
            },
            success: function (data) {
                // append patient form to modal
                $("#modal-convention .modal-content").html(data.html_form);
            },
            error: function (xhr, status, error) {
                $("#modal-convention").modal("hide");
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
                    $("#modal-convention").modal("hide");
    
                    // Success alert
                    Swal.fire({
                        // position: 'top-end',
                        type: 'success',
                        title: 'Convention saved!',
                        showConfirmButton: false,
                        timer: 2000
                    });
    
                    // reload datatable
                    $('#table-convention').DataTable().ajax.reload();
                }
                else {
                    // show forms errors in modal
                    $("#modal-convention .modal-content").html(data.html_form);
                }
            },
            error: function (xhr, status, error) {
                $("#modal-convention").modal("hide");
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

    var loadOpenCloseConventionModal = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            datatype: 'json',
            beforeSend: function (){
                // show modal
                $("#modal-convention-open-close").modal("show");
            },
            success: function (data) {
                $("#modal-convention-open-close .modal-content").html(data.html_form);
            },
            error: function (xhr, status, error) {
                $("#modal-convention").modal("hide");
                Swal.fire({
                    type: 'error',
                    title: 'Oops...',
                    text: error,
                    // footer: '<a href>Why do I have this issue?</a>'
                })
            }
        });
    };

    var openCloseConvention = function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#modal-convention-open-close").modal("hide");
    
                    // Success alert
                    Swal.fire({
                        // position: 'top-end',
                        type: 'success',
                        title: 'Convention updated!',
                        showConfirmButton: false,
                        timer: 2000
                    });
    
                    // reload datatable
                    $('#table-convention').DataTable().ajax.reload();
                }
            },
            error: function (xhr, status, error) {
                $("#modal-convention-open-close").modal("hide");
                Swal.fire({
                    type: 'error',
                    title: 'Oops...',
                    text: error,
                    // footer: '<a href>Why do I have this issue?</a>'
                })
            }
        });
        return false;
    }
    var t = function (){
        console.log('test');
    }

    // Create convention
    $(".js-create-convention").click(loadForm);
    $("#modal-convention").on("submit", ".js-convention-create-form", saveForm);

    // Update convention
    $("#table-convention").on("click", ".js-update-convention", loadForm);
    $("#modal-convention").on("submit", ".js-convention-update-form", saveForm);

    // Toggle open/close convention
    $("#table-convention").on("click", ".js-open-close-convention", loadOpenCloseConventionModal);
    $("#modal-convention-open-close").on("submit", ".js-convention-toggle-open-close-form", openCloseConvention)
    
});