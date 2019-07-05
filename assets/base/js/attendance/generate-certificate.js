$(function (){
    // focus cursor on search textbox
    $('.search-textbox', this).focus()

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
        var text = 'for attending the Flat Earth Society Convention this 1st of November 2019 at Marco Polo Davao.'
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
        doc.text('RONNEL V. LANABAN', 155, 445);
        doc.text('ELIJAH D. TANCIO', 520, 445);

        // Designation
        doc.setFont("courier");
        doc.setFontStyle("normal");
        doc.setFontSize(10);
        doc.setTextColor(0);
        doc.text('Social Media Manager', 157, 460);
        doc.text('Marketing Manager', 525, 460);

        window.open(doc.output('bloburl'), '_blank');
    }

    var generate =  function(e) {
        e.preventDefault();
        var search_textbox = $('.search-textbox', this).val()
        
        // clear search box
        $('.search-textbox', this).val('')
        $('.search-textbox', this).focus()

        $.ajax({
            url: `generate/`,
            type: 'get',
            datatype: 'json',
            beforeSend: function() {
                
            },
            success: function(response) {
                // generate_certificate();
                generate_certificate(response.participant)
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

    // $('#generate-certificate').on('click', demoFromHTML)
    $(".navbar-search-rfid-form").on("submit", generate)
});