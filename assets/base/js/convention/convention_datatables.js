$(document).ready(function() {
    var dt_table = $('#table-convention').DataTable({
        language: dt_language,  // global variable defined in html
        order: [[ 5, "desc" ]],
        lengthMenu: [[25, 50, 100, 200], [25, 50, 100, 200]],
        columnDefs: [
            {
                orderable: true,
                searchable: true,
                className: "center",
                targets: [0, 1, 2, 3, 4, 5]
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
        processing: true,
        serverSide: true,
        stateSave: true,
        // JSON url
        ajax: CONVENTION_LIST_JSON_URL
    });
});