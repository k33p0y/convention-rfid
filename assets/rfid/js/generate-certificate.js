$(function (){

    var rfid_num = '';
    $(document).keypress(function(event){
        get_rfid_num()
    });

    function get_rfid_num(){
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if (event.keyCode >= 48 && event.keyCode <= 57){
            // console.log(event.which);
            // console.log(String.fromCharCode(event.keyCode))
            rfid_num += String.fromCharCode(event.keyCode)
        }
        // if (event.keyCode >= 65 && event.keyCode <= 90)
        if (rfid_num){
            if(keycode == '13'){
                get_participant_json();
                // console.log(rfid_num);
                rfid_num = '';
            }
        }
    }

    function generate_certificate(participant_name){
        var doc = new jsPDF('landscape', 'pt', 'letter');

        // border
        doc.setLineWidth(10);
        doc.setDrawColor(40,56,71);
        doc.rect(20, 20, doc.internal.pageSize.width - 40, doc.internal.pageSize.height - 40, 'S');

        // TITLE
        doc.setFont("times");
        doc.setFontStyle("bold");
        doc.setFontSize(32);
        doc.setTextColor(242, 102, 58);
        doc.text('CERTIFICATE OF ATTENDANCE', 390, 100, 'center');

        // 'This is to recognize'
        doc.setFontSize(15);
        doc.setFont('courier');
        doc.setFontStyle("normal");
        doc.setTextColor(0);
        doc.text('This is to recognize', 390, 150, 'center');

        // NAME
        var name = participant_name
        // doc.splitTextToSize(string, length)
        lines = doc.splitTextToSize(name, 205)
        doc.setFont("times");
        doc.setFontStyle("bold");
        doc.setFontSize(60);
        doc.setTextColor(242, 102, 58);
        doc.text(lines, 390, 230, 'center');

        // 'Event date and venue'
        var text = `for attending the Test Convention this January 1st, 2019 at Marco Polo Davao`;
    
        text_lines = doc.splitTextToSize(text, 1200)
        doc.setFontSize(15);
        doc.setFont('courier');
        doc.setFontStyle("normal");
        doc.setTextColor(0);
        doc.text(text_lines, 390, 330, 'center');

        // draw two horizontal lines
        doc.setDrawColor(40,56,71); // draw red lines
        doc.setLineWidth(3);
        // doc.line(startX, startY, endX, endY)
        doc.line(110, 430, 310, 430) // left
        doc.line(465, 430, 665, 430) // right

        // draw two circles
        doc.setFillColor(40,56,71);
        // doc.circle(X, Y, size, type)
        doc.circle(390, 450, 60, 'F'); // outer circle
        doc.setLineWidth(1);
        doc.setDrawColor(255, 255, 255);
        doc.setFillColor(0);
        doc.circle(390, 450, 54, 'S'); // inner circle

        // signatories
        doc.setFont("courier");
        doc.setFontStyle("bold");
        doc.setFontSize(12);
        doc.setTextColor(242, 102, 58);
        doc.text('RONNEL V. LANABAN', 210, 445, {align: 'center'}); // left side name
        doc.text('JOSE P. RIZAL', 568, 445, {align: 'center'}); // right side name

        // Designation
        doc.setFont("courier");
        doc.setFontStyle("normal");
        doc.setFontSize(10);
        doc.setTextColor(0);
        doc.text('Social Media Manager', 210, 460, {align: 'center'}); // left side designation
        doc.text('Marketing Manager', 568, 460, {align: 'center'}); // right side designation

        // window.open(doc.output('bloburl'), '_blank');
        doc.autoPrint();
        doc.output('dataurlnewwindow');
    }

    function get_participant_json() {
        var convention_id = $('#convention_id').val()
        $.ajax({
            url: `/convention/${convention_id}/${rfid_num}/json/`,
            type: 'get',
            datatype: 'json',
            beforeSend: function() {
                
            },
            success: function(response) {
                if (response.participant_exist) {
                    // get participant full name
                    // var fullname = '';
                    // var fname = process_name(response.participant_first_name)
                    // var lname = process_name(response.participant_last_name)
                    // var middle_initial = process_name(response.participant_middle_name)
                    // if (middle_initial) {
                    //     middle_initial = middle_initial.slice(0, 1) + '.';
                    //     fullname = fname + ' ' + middle_initial + ' ' + lname
                    // } else fullname = fname + ' ' + lname;
                    
                    // // get start and end date
                    // var start_date = moment(response.convention_start_date).format('MMMM Do YYYY')
                    // var end_date = '';
                    // if (response.convention_end_date) {
                    //     end_date = moment(response.convention_end_date).format('MMMM Do YYYY');
                    // }

                    // // get convention name
                    // var convention_name = process_name(response.convention_name)

                    // // get venue
                    // var venue = process_name(response.venue)
                    
                    generate_certificate(response.participant_name)

                    // console.log(response)
                } else {
                    Swal.fire({
                        type: 'error',
                        title: 'Oops...',
                        text: 'Something went wrong! Seems like you are not registered to this convention.',
                        timer: 2000,
                    })
                }
            },
            error: function(xhr, status, error) {
                Swal.fire({
                    type: 'error',
                    title: 'Oops...',
                    text: error,
                    // footer: '<a href>Why do I have this issue?</a>'
                })
            }
        })
    }
});