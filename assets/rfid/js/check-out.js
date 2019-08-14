$(function (){
    // real-time date and time
    setInterval(function() {
        var momentNow = moment();
        $('#convention_current_date').html(momentNow.format('YYYY MMMM DD') + ' '
                            + momentNow.format('dddd')
                            .substring(0,3));
        $('#convention_current_time').html(momentNow.format('hh:mm:ss A'));
    }, 100);

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
                log_attendance(rfid_num);
                // console.log(rfid_num);
                rfid_num = '';
            }
        }
    }

    function log_attendance(rfid_num){
        var convention_id = $('#convention_id').val();
        $.ajax({
            url: `/convention/${convention_id}/${rfid_num}/check-out/`,
            type: 'get',
            datatype: 'json',
            success: function (response){
                // console.log(response.participant_exist);
                if (response.participant_exist) {
                    Swal.fire({
                        // position: 'top-end',
                        type: 'success',
                        title: `Thank you for coming ${response.participant_name}!`,
                        showConfirmButton: false,
                        timer: 2000
                    });
                }
                else {
                    Swal.fire({
                        // position: 'top-end',
                        type: 'error',
                        title: 'Oops... Seems like you are not registered to this convention!',
                        showConfirmButton: false,
                        timer: 2000
                    });
                }
            },
            error: function (xhr, status, error){
                Swal.fire({
                    type: 'error',
                    title: 'Oops...',
                    text: error,
                })
            }
        });
    }
})  