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

    function generate_id(fullname, prc_num){
        var doc = new jsPDF({
            orientation: 'landscape',
            unit: 'mm',
            // format: [85.598, 53.975] * 3
            format: [256.794,  161.925],
        });

        doc.setFont("courier");
        doc.setFontStyle("bold");
        doc.setFontSize(10);
        doc.setTextColor(0);
        doc.text(fullname, 8, 40); // fullname
        doc.text(prc_num, 8, 45); // PRC Number

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
                    generate_id(response.participant_name, response.prc_num)
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