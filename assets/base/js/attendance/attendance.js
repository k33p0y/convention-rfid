$(function (){
    // focus cursor on search textbox
    $('.search-textbox', this).focus()
    
    // real-time date and time
    setInterval(function() {
        var momentNow = moment();
        $('#convention_current_date').html(momentNow.format('YYYY MMMM DD') + ' '
                            + momentNow.format('dddd')
                             .substring(0,3));
        $('#convention_current_time').html(momentNow.format('hh:mm:ss A'));
    }, 100);

    var checkAttendance = function(e){
        e.preventDefault();
        var search_textbox = $('.search-textbox', this).val()
        
        // clear search box
        $('.search-textbox', this).val('')
        $('.search-textbox', this).focus()

        $.ajax({
            url: 'create-or-update/attendance/',
            type: 'post',
            data: {
                rfid: search_textbox,
            },
            beforeSend: function(){

            },
            success: function(response){
                // check if participant is registered to the convention
                if (response.rfid){
                    // if convention is OPEN
                    if (response.convention_is_open){
                        Swal.fire({type: 'success', title: `Welcome ${response.participant.fname} ${response.participant.lname}!`, showConfirmButton: false, timer: 3500});
                    // if convention is CLOSE
                    } else {
                        Swal.fire({type: 'success', title: `Thank you for coming ${response.participant.fname} ${response.participant.lname}!`, showConfirmButton: false, timer: 3500});
                    }
                // participant is not registered to the convention
                } else {
                    Swal.fire({type: 'error', title: 'Oops...! Card number not found!', showConfirmButton: false, timer: 3500});
                }
            },
            error: function(xhr, status, error){
                Swal.fire({type: 'error', title: 'Oops...', text: error, })
            },

        })
        return false;
    };
    
    $(".navbar-search-rfid-form").on("submit", checkAttendance)

})