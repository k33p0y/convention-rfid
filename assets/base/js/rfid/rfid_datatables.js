$(function () {
    var uuid = $('#participant_uuid').val();

    $.ajax({
        url: '/convention/' + uuid + '/rfids/json/',
        type: 'get',
        datatype: 'json',
        success: function (response) {
            console.log(response);
            // var obj = {
            //     "data": response
            // }
            // console.log(obj)

            var dt_table = $('#table-rfid').DataTable({
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
        },
        error: function (xhr, status, error) {
            console.log(error)
        }
    })
})