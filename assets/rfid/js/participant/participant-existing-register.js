$(function(){
    var convention_name = $('#convention_name').val();
    var rfid_num = '';

    // function to call get_rfid_num()
    $(document).keypress(function(event){
        get_rfid_num()
    });

    // get rfid number
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
                check_rfid_num(rfid_num);
                // console.log(rfid_num);
                rfid_num = '';
            }
        }
    }

    // check participant rfid card number
    function check_rfid_num(rfid){
        $.ajax({
            url: `/check/participant/${rfid}/`,
            type: 'get',
            datatype: 'json',
            // data: {
            //     'rfid_num': rfid
            // },
            success: function(response){
                if (response.rfid_exist){
                    
                    Swal.fire({
                        // position: 'top-end',
                        type: 'success',
                        title: `${response.participant_name} - PRC# ${response.participant_prc_num}`,
                        text: `Do you want to register to ${convention_name}?`,
                        showConfirmButton: true,
                        confirmButtonText: 'Register',
                    }).then(okay => {
                        if (okay) {
                            // call register_participant()
                            register_participant(response.rfid_num)
                        }
                    });
                    
                } else {
                    Swal.fire({
                        type: 'error',
                        title: 'Oops...',
                        text: ' Seems like your card is not registered!',
                        timer: 2000
                    })
                }
            },
            error: function(xhr, status, error){
                Swal.fire({
                    type: 'error',
                    title: 'Oops...',
                    text: error,
                })
            }
        })
    }

    // register participant
    function register_participant(rfid){
        $.ajax({
            url: `${rfid}/`,
            type: 'post',
            data: {
                'rfid_num': rfid
            },
            success: function(response){
                if (response.participant_exist){
                    Swal.fire({
                        type: 'success',
                        title: `${response.participant_name} registered to convention!`,
                        // text: `${response.participant_name}`,
                        timer: 2000
                    })
                } else{
                    Swal.fire({
                        type: 'error',
                        title: 'Oops...',
                        text: 'Seems like your card is not registered to this convention!',
                        timer: 2000
                    })
                }
            },
            error: function(xhr, status, error){
                Swal.fire({
                    type: 'error',
                    title: 'Oops...',
                    text: error,
                })
            }
        })
        
    }
})