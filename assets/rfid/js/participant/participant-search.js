$(function (){
    // initialize DataTable
    $('#table-convention').DataTable({
        order: [[2, 'desc']],
    });
    // create DataTable
    function createDataTable(lname, fname, mname, prc_number, conventions){
        // destroy current DataTable
        $('#table-convention').DataTable().destroy();

        // display participant full name
        $('#div-searchbar').after(`
            <div class="alert alert-success alert-dismissible fade show col-12 mt-3 mb-0" role="alert">
                <strong>${lname.toUpperCase()}, ${fname.toUpperCase()} ${mname.toUpperCase()}</strong>
                <button id="btn-alert-close" type="button" class="close" data-dismiss="alert" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
        `)

        // clear DataTable rows on click
        $('#btn-alert-close').on('click', function(){
            $('#table-convention').DataTable().clear().draw();   
        });
        
        // reinitialize DataTable with rows from json response
        $('#table-convention').DataTable({
            order: [[2, 'desc']],
            searching: true,
            // processing: true,
            // serverSide: true,
            // stateSave: true,
            data: conventions,
            columns: [
                { data: "name" },
                { data: "venue" },
                { data: "date_start" },
            ]
        })
    }

    // get participant json
    function getParticipantJson(prc_num){
        $.ajax({
            url: `/participant/search/${prc_num}/`,
            type: 'get',
            datatype: 'json',
            success: function(response){
                var lname = response.participant_lname
                var fname = response.participant_fname
                var mname = response.participant_mname
                var prc_number = response.participant_prc_num

                // console.log(response.conventions)
                if (response.participant_exist){
                    // call createDataTable()
                    var conventions = response.conventions
                    createDataTable(lname, fname, mname, prc_number, conventions)

                } else {
                    Swal.fire({
                        // position: 'top-end',
                        type: 'error',
                        title: 'Oops... No record found in database!',
                        showConfirmButton: false,
                        timer: 2000
                    });
                }
            },
            error: function(xhr, status, error){
                Swal.fire({
                    type: 'error',
                    title: 'Oops...',
                    text: error,
                })
            },
        })
    }

    // get PRC number
    var getPrcNum = function(){
        var prc_num = $('#input-searchbar').val();

        if (prc_num) {
            $('#input-searchbar').val('')

            // call getParticipantJson()
            getParticipantJson(prc_num)
        }
    }

    // call getPrcNum on click
    $('#btn-search-participant').on('click', getPrcNum)
})