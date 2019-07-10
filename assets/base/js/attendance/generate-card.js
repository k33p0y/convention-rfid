$(function (){
    $('.search-textbox', this).focus()

    function process_name(obj) {
        // name to array
        var name = obj.trim().split(' ')

        // remove white spaces
        for (i=0; i<name.length; i++){
            var index = name.indexOf('')
            if (index > -1) name.splice(index, 1);
        }

        // capitalize first character
        for (i=0; i<name.length; i++) name[i] = name[i].toUpperCase()
        
        // name to string
        name = name.join(' ')

        return name
    }

    function generate_id(fullname, society, prc_num){
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

        window.open(doc.output('bloburl'), '_blank');
    }

    var get_participant_json = function (e) {
        e.preventDefault()
        var search_textbox = $('.search-textbox', this).val()
        var convention_id = $('#convention_id').val()
        
        // clear search box
        $('.search-textbox', this).val('')
        $('.search-textbox', this).focus()

        $.ajax({
            url: `/convention/${convention_id}/certificate/generate/${search_textbox}/`,
            type: 'get',
            datatype: 'json',
            beforeSend: function (){

            },
            success: function (response){
                if (response.rfid_exist){
                    var fullname = '';
                    var fname = process_name(response.participant_first_name)
                    var lname = process_name(response.participant_last_name)
                    var middle_initial = process_name(response.participant_middle_name)
                    if (middle_initial) {
                        middle_initial = middle_initial.slice(0, 1) + '.';
                        fullname = fname + ' ' + middle_initial + ' ' + lname
                    } else fullname = fname + ' ' + lname;
                    var prc_num = response.prc_num
                    var society = response.society.toUpperCase()

                    generate_id(fullname, society, prc_num)
                } else {
                    Swal.fire({
                        type: 'error',
                        title: 'Oops...',
                        text: 'Something went wrong! Seems like you are not registered to this convention.',
                        timer: 2000,
                    })
                }
            },
            error: function (xhr, status, error){
                Swal.fire({
                    type: 'error',
                    title: 'Oops...',
                    text: error,
                    // footer: '<a href>Why do I have this issue?</a>'
                })
            }
        })
    }

    $(".navbar-search-rfid-form").on("submit", get_participant_json)
})