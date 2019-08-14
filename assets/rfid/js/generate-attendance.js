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
    var generate_attendance_pdf = function(json_object){
        // get all occupations
        let occupations = [...new Set(json_object.map(item => item.rfid__participant__occupation__name))];
        
        var doc = new jsPDF('portrait', 'pt', 'letter');

        doc.setProperties({
            title: convention_name,
        })
        doc.setFontStyle("normal");
        doc.text(convention_name, 15, 25);
        doc.setFontSize(10);
        
        for (i=0; i<occupations.length; i++){
            // filter json_object by occupation
            var filtered_json = json_object.filter(function(item){
                return item.rfid__participant__occupation__name==occupations[i];
            });
            
            if (!i) {
                doc.setFontStyle("normal");
                doc.setFontSize(10);
                doc.text(occupations[i], 15, 60);
                doc.autoTable({
                    body: filtered_json,
                    columns: [
                        // {header: 'ID', dataKey: 'id'},
                        {header: 'Lastname', dataKey: 'rfid__participant__lname'},
                        {header: 'Firstname', dataKey: 'rfid__participant__fname'},
                        {header: 'Middlename', dataKey: 'rfid__participant__mname'},
                        {header: 'PRC#', dataKey: 'rfid__participant__prc_num'},
                        {header: 'Check-in', dataKey: 'check_in'},
                        {header: 'Check-out', dataKey: 'check_out'},
                        {header: 'Date', dataKey: 'date_created'},
                    ],
                    margin: {top: 50, right: 15, bottom: 0, left: 15},
                    startY: 65,
                    styles: {overflow: 'ellipsize', cellWidth: 'wrap'},
                    columnStyles: {text: {cellWidth: 'auto'}}
                });
            }
            else {
                doc.text(occupations[i], 15, doc.autoTable.previous.finalY + 30);
                doc.autoTable({
                    body: filtered_json,
                    columns: [
                        // {header: 'ID', dataKey: 'id'},
                        {header: 'Lastname', dataKey: 'rfid__participant__lname'},
                        {header: 'Firstname', dataKey: 'rfid__participant__fname'},
                        {header: 'Middlename', dataKey: 'rfid__participant__mname'},
                        {header: 'PRC#', dataKey: 'rfid__participant__prc_num'},
                        {header: 'Check-in', dataKey: 'check_in'},
                        {header: 'Check-out', dataKey: 'check_out'},
                        {header: 'Date', dataKey: 'date_created'},
                    ],
                    margin: {top: 50, right: 15, bottom: 0, left: 15},
                    startY: doc.autoTable.previous.finalY + 35,
                    styles: {cellWidth: 'wrap', rowPageBreak: 'auto'},
                    columnStyles: {text: {cellWidth: 'auto'}}

                });
            }

            
        }
        
        window.open(doc.output('bloburl'))
    };

    var get_attendance_json = function() {
        
        $.ajax({
            url: `attendance/json/`,
            type: 'get',
            dataType: 'json',
            success: function(response){

                // sort attendance by date
                // var attendance_sorted_by_date = response.sort(sort_by_date)

                // add id and format check-in/check-out time
                // add_id_and_format_date(attendance_sorted_by_date)

                // generate pdf
                generate_attendance_pdf(response)
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