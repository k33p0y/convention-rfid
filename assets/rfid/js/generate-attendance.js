$(function() {
    var convention_name = $('#convention_name').val();

    // function to sort attendance by date
    function sort_by_date(a, b) {
        const date_createdA = a.date_created;
        const date_createdB = b.date_created;

        if (date_createdA < date_createdB) return -1;
        if (date_createdA > date_createdB) return 1;
        return 0;
    };

    // function to add id and format time check-in/check-out
    function add_id_and_format_date(arr) {
        for (i=0; i<arr.length; i++){
            // add id
            Object.assign(arr[i], {id: i+1});

            // format time
            if (arr[i].check_in) arr[i].check_in = moment(arr[i].check_in, 'HH:mm:ss').format('hh:mm A');
            if (arr[i].check_out) arr[i].check_out = moment(arr[i].check_out, 'HH:mm:ss').format('hh:mm A');
        }
    }

    // function to generate attendance as pdf
    var generate_attendance_pdf = function(object){
        attendance_array = object;
        var doc = new jsPDF('portrait', 'pt', 'letter');

        doc.setProperties({
            title: convention_name,
        })
        doc.text(convention_name, 15, 25);
        // doc.text(society_name, 15, 30);
        // doc.setFontSize(12);
        // doc.text('Society: ' + society_name, 15, 40);
        
        doc.autoTable({
            body: attendance_array,
            columns: [
                {header: 'ID', dataKey: 'id'},
                {header: 'Lastname', dataKey: 'rfid__participant__lname'},
                {header: 'Firstname', dataKey: 'rfid__participant__fname'},
                {header: 'Middlename', dataKey: 'rfid__participant__mname'},
                {header: 'PRC#', dataKey: 'rfid__participant__prc_num'},
                {header: 'Check-in', dataKey: 'check_in'},
                {header: 'Check-out', dataKey: 'check_out'},
                {header: 'Date', dataKey: 'date_created'},
            ],
            margin: {top: 50, right: 15, bottom: 0, left: 15},
            // theme: 'grid',
            // showFoot: 'everyPage',

            // margin: {top: 30}
        });

        window.open(doc.output('bloburl'))
    };

    var get_attendance_json = function() {
        
        $.ajax({
            url: `attendance/json/`,
            type: 'get',
            dataType: 'json',
            success: function(response){

                // sort attendance by date
                var attendance_sorted_by_date = response.sort(sort_by_date)

                // add id and format check-in/check-out time
                add_id_and_format_date(attendance_sorted_by_date)

                // generate pdf
                generate_attendance_pdf(attendance_sorted_by_date)
            },
            error: function(xhr, status, error){
                $("#modal-convention-open-close").modal("hide");
                Swal.fire({
                    type: 'error',
                    title: 'Oops...',
                    text: error,
                    // footer: '<a href>Why do I have this issue?</a>'
                })
            },
        })
    };

    $('#generate-attendance').on('click', get_attendance_json);
})