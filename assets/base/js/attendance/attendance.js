$(function (){
    // focus cursor on search textbox
    $('.search-textbox', this).focus()

    // get participants count, convention status, current attendees
    $(function (){
        get_participants_count();
    })
    
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
                        // test();
                    // if convention is CLOSE
                    } else {
                        Swal.fire({type: 'success', title: `Thank you for coming ${response.participant.fname} ${response.participant.lname}!`, showConfirmButton: false, timer: 3500});
                        // test();
                    }
                    // get_participants_count();
                // participant is not registered to the convention
                } else {
                    Swal.fire({type: 'error', title: 'Oops...! Card number not found!', showConfirmButton: false, timer: 3500});
                }
                get_participants_count();
            },
            error: function(xhr, status, error){
                Swal.fire({type: 'error', title: 'Oops...', text: error, })
            },

        })
        return false;
    };
    
    // get participants count, convention status, current attendees function
    var get_participants_count = function() {
        $.ajax({
            url: 'get-participants/count/',
            type: 'get',
            datatype: 'json',
            beforeSend: function(){

            },
            success: function(response){
                if (response.convention_is_open){
                    $('#convention_check_in').html('in')
                } else{
                    $('#convention_check_in').html('out')
                }
                $('#registered_participants').html(response.registered_participants);
                $('#checked_in_participants').html(response.checked_in_participants);
            },
            error: function(xhr, status, error){
                Swal.fire({type: 'error', title: 'Oops...', text: error, })
            },
        })
    }

    $(".navbar-search-rfid-form").on("submit", checkAttendance)
})