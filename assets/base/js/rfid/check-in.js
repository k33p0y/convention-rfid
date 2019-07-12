$(function (){
    // real-time date and time
    setInterval(function() {
        var momentNow = moment();
        $('#convention_current_date').html(momentNow.format('YYYY MMMM DD') + ' '
                            + momentNow.format('dddd')
                            .substring(0,3));
        $('#convention_current_time').html(momentNow.format('hh:mm:ss A'));
    }, 100);
})