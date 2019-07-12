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
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if (event.keyCode >= 48 && event.keyCode <= 57){
            // console.log(event.which);
            // console.log(String.fromCharCode(event.keyCode))
            rfid_num += String.fromCharCode(event.keyCode)
        }
        // if (event.keyCode >= 65 && event.keyCode <= 90)

        if (rfid_num){
            if(keycode == '13'){
                alert(rfid_num);
                rfid_num = '';
            }
        }
    });
})  