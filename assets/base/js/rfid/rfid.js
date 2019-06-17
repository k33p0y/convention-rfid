$(function (){
    // load DataTable function
    function loadDataTable (response) {
        $('#table-rfid').DataTable({
            order: [[ 4, "desc" ]],
            // lengthMenu: [[25, 50, 100, 200], [25, 50, 100, 200]],
            columnDefs: [
                {
                    orderable: true,
                    searchable: true,
                    className: "center",
                    targets: [0, 1, 2, 3, 4]
                },
                {
                    orderable: false,
                    searchable: false,
                    // className: "center",
                    targets: [-1]
                },
                {
                    responsivePriority: 1, targets: 0
                },
                {
                    responsivePriority: 2, targets: -1
                }
            ],
            searching: true,
            // processing: true,
            // serverSide: true,
            // stateSave: true,
            // JSON url
            data: response,
            columns: [
                {title: 'RFID Number', data: 'rfid_num'},
                {title: 'Society', data: 'society__name'},
                {title: 'Membership', data: 'membership__name'},
                {title: 'Date created', data: 'date_created'},
                {title: 'Last updated', data: 'date_updated'},
                {title: 'Action', render: function ( data, type, row ) {
                    return `
                        <button class='btn btn-default m-0 p-0 js-update-society' data-url='/convention/rfid/${row.rfid_uuid}/update/' data-toggle='tooltip' title='Update'>
                            <i class='far fa-edit text-primary'></i>
                        </button>
                    `;
                } },
            ]
        });
    };

    // get participant uuid
    var uuid = $('#participant_uuid').val();

    $.ajax({
        url: '/convention/' + uuid + '/rfids/json/',
        type: 'get',
        datatype: 'json',
        success: function (response) {
            // load DataTable
            loadDataTable(response);
        },
        error: function (xhr, status, error) {
            console.log(error)
        }
    });

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            datatype: 'json',
            beforeSend: function (){
                // show modal
                $("#modal-rfid").modal("show");
            },
            success: function (response) {
                // append patient form to modal
                $("#modal-rfid .modal-content").html(response.html_form);
                $('#modal-rfid #participant_id').val(uuid)
            },
            error: function (xhr, status, error) {
                $("#modal-rfid").modal("hide");
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
            success: function (response) {
                if (response.form_is_valid) {
                    $("#modal-rfid").modal("hide");
    
                    // Success alert
                    Swal.fire({
                        // position: 'top-end',
                        type: 'success',
                        title: 'RFID saved!',
                        showConfirmButton: false,
                        timer: 2000
                    });
                    
                    // destroy DataTable
                    $('#table-rfid').DataTable().destroy();
                    
                    // reload DataTable
                    loadDataTable(response.rfids)
                }
                else {
                    // show forms errors in modal
                    $("#modal-rfid .modal-content").html(data.html_form);
                }
            },
            error: function (xhr, status, error) {
                $("#modal-rfid").modal("hide");
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
    $(".js-create-rfid").click(loadForm);
    $("#modal-rfid").on("submit", ".js-rfid-create-form", saveForm);

    // Update participant
    // $("#table-participant").on("click", ".js-update-participant", loadForm);
    // $("#modal-participant").on("submit", ".js-participant-update-form", saveForm);
});