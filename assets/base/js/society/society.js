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

    // var archiveCategory = function () {
    //     var form = $(this);
    //     $.ajax({
    //         url: form.attr("action"),
    //         data: form.serialize(),
    //         type: form.attr("method"),
    //         dataType: 'json',
    //         success: function (data) {
    //             if (data.form_is_valid) {
    //                 $("#modal-category").modal("hide");
    
    //                 // Success alert
    //                 Swal.fire({
    //                     // position: 'top-end',
    //                     type: 'success',
    //                     title: 'Category archived!',
    //                     showConfirmButton: false,
    //                     timer: 2000
    //                 });
    
    //                 // reload datatable
    //                 $('#table-category').DataTable().ajax.reload();
    //             }
    //         },
    //         error: function (xhr, status, error) {
    //             $("#modal-category").modal("hide");
    //             Swal.fire({
    //                 type: 'error',
    //                 title: 'Oops...',
    //                 text: error,
    //                 // footer: '<a href>Why do I have this issue?</a>'
    //             })
    //         }
    //     });
    //     return false;
    // };

    // Create society
    $(".js-create-society").click(loadForm);
    $("#modal-society").on("submit", ".js-society-create-form", saveForm);

    // Update category
    // $("#table-category").on("click", ".js-update-category", loadForm);
    // $("#modal-category").on("submit", ".js-category-update-form", saveForm);

    // // Archive category
    // $("#table-category").on("click", ".js-archive-category", loadForm);
    // $("#modal-category").on("submit", ".js-category-archive-form", archiveCategory);
});