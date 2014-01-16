$(document).ready(function () {
    $('a.reports').click(function () {
        var text = $(this).text();
        text = text.trim();
        if (text == 'Generic') {
            $.get('http://' + location.host + '/reports/generic', function (data) {

                $('.page-content').html(data);
            });
        }
        else if (text == 'Cash Report') {
            $.get('http://' + location.host + '/reports/cash-report', function (data) {
                $('.page-content').html(data);
            });
        }

    });

});