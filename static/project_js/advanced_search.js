$(document).ready(function () {
    $('#search_awb').submit(function (event) {

        var search_box_value = $('#nav-search-input').val();
        if (search_box_value.trim() == '') {
            event.preventDefault();
            alert('search box value cannot be empty');
        }

    });

});