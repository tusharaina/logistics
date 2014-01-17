/**
 * Created by technomaniac on 27/11/13.
 */
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});


function ajaxloader(element) {
    $(element).html('<img src="/static/img/loader.gif" id="ajaxLoader">');
    var height = element.height();
    var width = $('body').width();
    var pos = element.position();

    $('#ajaxLoader').css({
        top: height / 2 + pos.top,
        left: width / 2,
        position: 'absolute'
    });
}

function closeLoader() {
    $('#ajaxLoader').hide();
}

//function getUrlVars() {
//    var vars = {};
//    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function (m, key, value) {
//        vars[key] = value;
//    });
//    return vars;
//}

//$('li').live('hover', function () {
//
//    $(this).attr('class', 'open');
//
//});
$(document).ready(function () {
    $('#start_date input').datepicker({
        dateFormat: 'yy-mm-dd'
    });
    $('#end_date input').datepicker({
        dateFormat: 'yy-mm-dd'
    });
    $('#id_scheduling_time').timepicker();
    $('#id_scheduling_time').val('');

    if ($('#select_branch').length) {
        $.ajax({
            type: 'POST',
            url: '/internal/branch/get_all',
            cache: true,
            success: function (response) {
                $('#select_branch').html(response);
            }
        });
    }
    if ($("#create_mts_form #table").length) {
        $.ajax({
            type: 'POST',
            url: 'get_tbs',
            data: {from_branch: $(this).val()},
//            beforeSend: function () {
//                ajaxloader($('#create_mts_form #table'));
//            },
            success: function (response) {
                $("#create_mts_form #table").html(response);
                //closeLoader();
            }
        });
    }
    if ($("#drs_awb_table").length) {
        get_drs_awbs('pincode');
    }
    if ($("#dto_awb_table").length) {
        $.ajax({
            type: 'POST',
            url: '/transit/dto/get_awbs',
            cache: true,
//            beforeSend: function () {
//                ajaxloader($('#dto_awb_table'));
//            },
            success: function (response) {
                $("#dto_awb_table").html(response);
                //closeLoader();
            }
        });
    }
    call_count_functions();

    $("#warehouse_pincode").autocomplete({
        source: "/zoning/pincode/search",
        minLength: 1,
        focus: function (event, ui) {
            $(this).val(ui.item.label);
            return false;
        },
        select: function (event, ui) {
            $('#hidden_pincode').val(ui.item.value);
            $(this).val(ui.item.label);
            return false;
        }
    });
});

function get_drs_awbs(sort, element) {
    if ($(this).attr('id') == sort) {
        sort = '-' + sort;
        $(this).attr('id', sort);
    } else {
        $(this).attr('id', sort);
    }
    $.ajax({
        type: 'GET',
        url: '/transit/drs/get_awbs',
        cache: true,
        data: {
            sort: sort
        },
        beforeSend: function () {
            ajaxloader($('#drs_awb_table'));
        },
        success: function (response) {
            $("#drs_awb_table").html(response);
            closeLoader();
        }
    });
}

setInterval(function () {
    call_count_functions();
}, 60000);

function call_count_functions() {
    get_count('awb', 'incoming', '');
    get_count('awb', 'outgoing', '');
    get_count('awb', 'incoming', 'COD');
    get_count('awb', 'incoming', 'PRE');
    get_count('awb', 'incoming', 'REV');
    get_count('awb', 'outgoing', 'COD');
    get_count('awb', 'outgoing', 'PRE');
    get_count('awb', 'outgoing', 'REV');
    get_count('tb', 'incoming', '');
    get_count('tb', 'outgoing', '');
    get_count('mts', 'incoming', '');
    get_count('mts', 'outgoing', '');
    get_count('drs', '', '');
    get_count('dto', '', '');
}

function get_count(model, type, category) {
    if ($("#get_count_" + model + "_" + type + category).length) {
        $.ajax({
            type: 'GET',
            url: '/transit/get_count',
            data: {
                'model': model,
                'type': type,
                'category': category
            },
            cache: true,
            success: function (response) {
                $("#get_count_" + model + "_" + type + category).html(response);
            }
        });
    }
}

$('#select_branch #id_branch').live('change', function () {
    $.ajax({
        type: 'POST',
        url: '/user/set_branch',
        cache: true,
        data: {
            branch: $(this).val()
        },
        success: function (response) {
            $(this).val(response);
//            if (window.location.origin) {
            window.location.reload();
            history.go(0);
//            }
        }
    });
});

function get_message() {
    $.ajax({
        type: 'GET',
        url: '/user/get_message',
        cache: true,
        beforeSend: function () {
            if ($('#get_message').html() != '') {
                $('#get_message').fadeOut(100);
            }
        },
        success: function (response) {
            $('#get_message').html(response).fadeIn(100);
        }
    });
}

$("#create_tb_form #id_delivery_branch").change(function () {
    $.ajax({
        type: 'POST',
        url: 'get_awbs',
        cache: true,
        data: {delivery_branch: $(this).val()},
//        beforeSend: function () {
//            if ($("#awb_table").html() != '')
//                $("#awb_table").html('');
//        },
        success: function (response) {
            $("#awb_table").html(response);
        }
    });
});

function get_selected(element) {
    var selected = $(element).find(':checkbox:checked').map(function () {
        return this.id;
    }).get();

    return selected;
}

$("#create_tb_form").submit(function (e) {
    var awbs = $('#tb_in_scanning_table tbody tr :hidden').map(function () {
        return this.value;
    }).get();
    if (awbs != '') {
        $.ajax({
            type: 'POST',
            url: '/transit/tb/create_tb',
            cache: true,
            data: {
                origin_branch: $('#id_origin_branch').val(),
                delivery_branch: $('#id_delivery_branch').val(),
                awbs: JSON.stringify(awbs)
            },
            success: function (response) {
                if (response == 'True') {
                    window.location = '/transit/tb/outgoing';
                } else {
                    alert(0);
                }
            }
        });
    } else {
        alert("Please in-scan shipments")
    }
    e.preventDefault();
    return false;
});

$('#tb_in_scanning_table tbody tr td:first-child input').live('change', function () {
    $('#awb_alert').fadeOut(400, function () {
        $(this).remove();
    });
    var awb = $(this).val();
    $(this).val('');
    if (awb != '') {
        $.ajax({
            type: 'POST',
            url: '/transit/tb/in_scanning',
            cache: true,
            data: {
                awb: awb,
                delivery_branch: $("#create_tb_form #id_delivery_branch").val()
            },
            success: function (response) {
                $('#tb_in_scanning_table tbody tr:first-child').clone().insertAfter('#tb_in_scanning_table tbody tr:first-child');
                $('#tb_in_scanning_table tbody tr:nth-child(2)').html(response);
                $('#tb_in_scanning_table tbody tr:first-child td:first-child input').focus();
                get_message()
//                $('#tb_in_scanning_table #awb_alert').clone().insertBefore('.widget-main').fadeIn(400);
//                $('#tb_in_scanning_table #awb_alert').fadeOut(400, function () {
//                    $(this).remove();
//                });
            }
        });
    }
})
;


$("#create_mts_form").submit(function (e) {
    var tbs = $('#create_mts_form table td :checkbox:checked').map(function () {
        return this.id;
    }).get();
    if (tbs != '') {
        $.ajax({
            type: 'POST',
            url: 'create_mts',
            cache: true,
            data: {
                from_branch: $('#id_from_branch').val(),
                to_branch: $('#id_to_branch').val(),
                type: $('#id_type').val(),
                tbs: JSON.stringify(tbs)
            },
            success: function (response) {
                if (response == 'True') {
                    window.location = '/transit/mts/outgoing';
                } else {
                    alert('error');
                }
            }
        });
    } else {
        alert('Please select atlease one TB');
    }
    e.preventDefault();
    return false;
});


$("#create_drs_form").submit(function (e) {
    var fl = $('#drs_in_scanning_table tbody tr :hidden').map(function () {
        return this.value;
    }).get();
    var rl = get_selected("#reverse_awb_table tbody");
    if (fl == '' && rl == '') {
        alert("Please In-scanned Forward shipments or select Reverse Pickups");
    } else {
        $.ajax({
            type: 'POST',
            url: 'create_drs',
            cache: true,
            data: {
                fe: $('#id_fe').val(),
                vehicle: $('#id_vehicle').val(),
                fl: JSON.stringify(fl),
                rl: JSON.stringify(rl)
            },
            success: function (response) {
                if (response == 'True') {
                    window.location = '/transit/drs';
                } else {
                    alert(response);
                }
            }
        });
    }
    e.preventDefault();
    return false;
});

$("#create_dto_form").submit(function () {
    var awbs = $('#dto_in_scanning_table tbody tr :hidden').map(function () {
        return this.value;
    }).get();
    if (awbs != '') {
        $.ajax({
            type: 'POST',
            url: '/transit/dto/create_dto',
            cache: true,
            data: {
                fe: $('#id_fe').val(),
                vehicle: $('#id_vehicle').val(),
                awbs: JSON.stringify(awbs)
            },
            success: function (response) {
                if (response == 'True') {
                    window.location = '/transit/dto';
                } else {
                    alert('error');
                }
            }
        });
    } else {
        alert("Please in scanned shipments")
    }
    return false;
});

$('#dto_in_scanning_table tbody tr input[type="text"]').live('change', function (e) {
//    if (e.which == 13) {
    var awb = $(this).closest('tr').attr('id');
    var type = $(this).attr('name');
    var val = $(this).val();
    $.ajax({
        type: 'POST',
        url: '/transit/awb/field_update',
        cache: true,
        data: {
            awb: awb,
            field: type,
            val: val
        },
        success: function (response) {
            get_message();
        }
    });
    // }
});

$('#manifest_in_scanning_table tbody tr td:first-child input').live('change', function () {
//    $('#awb_alert').fadeOut(400, function () {
//        $(this).remove();
//    });
    var awb = $(this).val();
    $(this).val('');
    if (awb != '') {
        $.ajax({
            type: 'POST',
            url: '/transit/awb/in_scanning',
            cache: true,
            data: {
                awb: awb
            },
            success: function (response) {
                //alert(response);
                $('#manifest_in_scanning_table tbody tr:first-child').clone().insertAfter('#manifest_in_scanning_table tbody tr:first-child');
                $('#manifest_in_scanning_table tbody tr:nth-child(2)').html(response);
                $('#manifest_in_scanning_table tbody tr:first-child td:first-child input').focus();
                get_message();
            }
        });
    }
});

$('#drs_in_scanning_table tbody tr td:first-child input').live('change', function () {
    var awb = $(this).val();
    $(this).val('');
    if (awb != '') {
        $.ajax({
            type: 'POST',
            url: '/transit/drs/create',
            cache: true,
            data: {
                awb: awb
            },
            success: function (response) {
                //alert(response);
                if (response != '') {
                    $('#drs_in_scanning_table tbody tr:first-child').clone().insertAfter('#drs_in_scanning_table tbody tr:first-child');
                    $('#drs_in_scanning_table tbody tr:nth-child(2)').html(response);
                    $('#drs_in_scanning_table tbody tr:first-child td:first-child input').focus();
                    get_message();
                } else {
                    get_message();
                }
//                var alert = $('#awb_status_alert').clone();
//                $('#awb_status_alert').hide();
//                $(alert).insertBefore('#manifest_in_scanning_table').show('medium');
            }
        });
    }
});

$('#dto_in_scanning #awb_in_scan').live('change', function () {
    var awb = $(this).val();
    $(this).val('');
    if (awb != '') {
        $.ajax({
            type: 'POST',
            url: '/transit/dto/create',
            cache: true,
            data: {
                awb: awb
            },
            success: function (response) {
                //alert(response);
                if (response != '') {
                    $('#dto_in_scanning_table').show();
                    $(response).insertBefore('#dto_in_scanning_table tbody tr:first-child');
                    get_message();
                } else {
                    get_message();
                }
//                var alert = $('#awb_status_alert').clone();
//                $('#awb_status_alert').hide();
//                $(alert).insertBefore('#manifest_in_scanning_table').show('medium');
            }
        });
    }
});


$('.select_all').live('change', function () {
    if ($(this).is(":checked")) {
        $(this).closest('table').find('tbody :checkbox').attr('checked', true);
    } else {
        $(this).closest('table').find('tbody :checkbox').attr('checked', false);
    }
});

$('#get_awb_invoice').click(function () {
    var awbs = JSON.stringify(get_selected($('table tbody')));
    if (awbs != '[]') {
        window.open('/transit/awb/print_invoice_sheet?awbs=' + awbs, 'Invoice Printing')
    } else {
        alert("Please select atleast one AWB")
    }
    return false;
});

$('#editMTS').live('click', function () {
    var status = '<select id="updateMTSStatus" >';
    status += '<option selected value="" ></option>';
    //status += '<option value="U">Un-Delivered</option>';
    status += '<option value="D">Received</option>';
    // status += '<option value="R">Red Alert</option>';
    status += '</select>';
    $(this).closest('tr').find('.status').html(status);
});

$('#editDRS').live('click', function () {
    var status = '<select id="updateDRSStatus" >';
    status += '<option selected value="" style="display: none"></option>';
    status += '<option value="O">Open</option>';
    status += '<option value="C">Closed</option>';
    status += '</select>';
    $(this).closest('tr').find('.status').html(status);
});


$('#updateMTSStatus').live('change', function () {
    var element = $(this);
    if (confirm("Are you sure want to change the status ?")) {
        $.ajax({
            type: 'POST',
            url: '/transit/mts/update_status',
            cache: true,
            data: {
                mts_id: $(element).closest('tr').find('.mts_id').text(),
                status: $(element).val()
            },
            success: function (response) {
                $(element).closest('td').html(response);
            }
        });
    }
});


$('#updateDRSStatus').live('change', function () {
    var element = $(this);
    if (confirm("Are you sure want to change the status ?")) {
        $.ajax({
            type: 'POST',
            url: '/transit/drs/update_status',
            cache: true,
            data: {
                drs_id: $(element).closest('tr').find('.id').text(),
                status: $(element).val()
            },
            success: function (response) {
                $(element).closest('td').html(response);
            }
        });
    }
});


$("#drs_status_update_form").submit(function () {
    status = $('#drs_status_update_form #awb_status').val();
    if (status == 'DEL') {
        var i = 0;
        $('#awb_status_update_table tbody tr').each(function () {
            if ($(this).find(':checkbox').is(':checked')) {
                if ($(this).find('#status').text() == 'Dispatched') {
                    if ($(this).find('#type').text() == 'COD') {
                        if ($(this).find('#collected_amount').val() < $(this).find('#expected_amount').text()) {
                            $(this).find('#collected_amount').focus().attr('class', 'input-small red');
                            i++;
                        }
                    }
                } else if ($(this).find('#status').text() == 'Cancelled') {
                    alert('Cannot Delivered Cancelled Shipments. Create another DRS.');
                    return false;
                } else if ($(this).find('#status').text() == 'Delivered') {
                    alert('Already Updated');
                    return false;
                }
            }
        });
        if (i > 0) {
            alert('Please enter collected amount for delivered shipments');
            return false;
        }
    } else if (status == 'CAN') {
        var c = 0;
        $('#awb_status_update_table tbody tr').each(function () {
            if ($(this).find('#status').text() != 'Pending for Delivery') {
                $(this).find('input:last').focus().attr('class', 'input-small red');
                c++;
            }
        });
        if (c > 0) {
            alert('Please in-scan cancelled shipments');
            return false;
        }
    } else if (status == 'ISC') {
        var d = 0;
        $('#awb_status_update_table tbody tr').each(function () {
            if ($(this).find('#status').text() == 'Pending for Pickup') {
                $(this).find('input:last').focus().attr('class', 'input-small red');
                d++;
            }
        });
        if (d > 0) {
            alert('Please in-scan reverse picked-up shipments');
            return false;
        }
    }
    var awbs = get_selected($('#awb_status_update_table tbody'));

    var collected_amts = $('#awb_status_update_table tbody').find(':checkbox:checked').map(function () {
        return $(this).closest('tr').find('#collected_amount').val();
    }).get();

    if (awbs != '') {
        $.ajax({
            type: 'POST',
            url: '/transit/drs/awb_status_update',
            cache: true,
            data: {
                awb_status: status,
                collected_amts: JSON.stringify(collected_amts),
                awbs: JSON.stringify(awbs)
            },
            success: function (response) {
                //alert(response);
                location.reload();
            }
        });
    } else {
        alert("Please select atleast one AWB")
    }
    return false;
});

$("#dto_status_update_form").submit(function () {
    var awbs = get_selected($('#awb_status_update_table tbody'));

    if (awbs != '') {
        $.ajax({
            type: 'POST',
            url: '/transit/dto/awb_status_update',
            cache: true,
            data: {
                awb_status: $('#dto_status_update_form #awb_status').val(),
                awbs: JSON.stringify(awbs)
            },
            success: function (response) {
                //alert(response);
                location.reload();
            }
        });
    } else {
        alert("Please select atleast one AWB")
    }
    return false;
});

$('#drs_print_sheet').click(function () {
    var awbs = JSON.stringify(get_selected($('#awb_status_update_table tbody')));
    if (awbs != '[]') {
        window.open('/transit/drs/get_print_sheet?awbs=' + awbs, 'DRS Printing')
    } else {
        alert("Please select atleast one AWB")
    }
    return false;
});

$('#dto_print_sheet').click(function () {
    var awbs = JSON.stringify(get_selected($('#awb_status_update_table tbody')));
    if (awbs != '[]') {
        window.open('/transit/dto/get_print_sheet?awbs=' + awbs, 'DRS Printing')
    } else {
        alert("Please select atleast one AWB")
    }
    return false;
});


//$('#awb_status_update_form select').live('change', function () {
//    if ($(this).val() == 'CAN') {
//        if ($('#awb_status_update_table thead tr th').length == 10) {
//            $('<th>In-Scan</th>').insertAfter('#awb_status_update_table thead th:last');
//            $('#awb_status_update_table tbody tr').each(function () {
//                $('<td><input type="text" class="input-small" onchange="updateAWBStatus(this)"></td>').insertAfter($(this).find('td:last'));
//            });
//        }
//    } else {
//        if ($('#awb_status_update_table thead tr th').length > 10) {
//            $('#awb_status_update_table thead tr th:last').remove();
//            $('#awb_status_update_table tbody tr').each(function () {
//                $(this).find('td:last').remove();
//            });
//        }
//    }
//});

function inScanDRSAWB(element) {
    $.ajax({
        type: 'POST',
        url: '/transit/drs/awb_cancel_scan',
        cache: true,
        data: {
            id: $(element).closest('tr').attr('id'),
            awb: $(element).val()
        },
        success: function (response) {
            if (response != '') {
                $(element).closest('tr').find('select').val(response);
                get_message();
            } else {
                get_message();
            }
        }
    });
}

$('#collected_amount').live('keypress', function (e) {
    var element = $(this);
    if (element.closest('tr').find('#type').html() == 'COD') {
        if (e.which == 13) {
            if (element.val() < element.closest('tr').find('#expected_amount').html()) {
                alert('Please enter correct amount');
            } else {
                if (confirm('Are you sure want to change status to delivered ?')) {
                    $.ajax({
                        type: 'POST',
                        url: '/transit/drs/drs_awb_status_update',
                        cache: true,
                        data: {
                            awb: element.closest('tr').attr('id'),
                            status: 'DEL',
                            coll_amt: $(this).val()
                        },
                        success: function (response) {
                            if (response == 'True') {
                                element.closest('tr').find('select').val('DEL');
                                element.closest('tr').find('select').attr('disabled', 'disabled');
                                get_message();
                            }
                        }
                    });
                }
            }
        }
    }
});

function updateDRSAWBStatus(element) {
    if ($(element).closest('tr').find('#collected_amount').length) {
        var coll_amt = $(element).closest('tr').find('#collected_amount').val()
    } else {
        coll_amt = ''
    }
    if ($(element).val() == 'DEL' &&
        $(element).closest('tr').find('#collected_amount').val() < $(element).closest('tr').find('#expected_amount').html() &&
        $(element).closest('tr').find('#type').html() == 'COD') {
        alert('Please enter collected amount');
        $(element).closest('tr').find('#collected_amount').focus();
    } else if ($(element).val() != 'DEL' &&
        $(element).closest('tr').find('#in_scan').val() != $(element).closest('tr').find('#awb').html()
        && $(element).closest('tr').find('#type').html() != 'Reverse Pickup') {
        alert('Please In-Scan Shipment first');
        $(element).closest('tr').find('#in_scan').focus();
    } else {
        if (confirm('Are you sure want to change status ?')) {
            $.ajax({
                type: 'POST',
                url: '/transit/drs/drs_awb_status_update',
                cache: true,
                data: {
                    awb: $(element).closest('tr').attr('id'),
                    status: $(element).val(),
                    coll_amt: coll_amt
                },
                success: function (response) {
                    if (response == 'True') {
                        $(element).closest('tr').find('select').attr('disabled', 'disabled');
                        get_message();
                    }
                }
            });
        }
    }
}

function generate_mis() {
    var awbs = JSON.stringify(get_selected($('table tbody')));
    if (awbs != '') {
        window.open('/transit/awb/mis/download?awbs=' + awbs, 'MIS Download')
    } else {
        alert("Please select atleast one AWB")
    }
    return false;
}

$('#awb_report_cc_form select').on('change', function () {
    $.ajax({
        type: 'GET',
        url: '/transit/awb/report_cc',
        cache: true,
        beforeSend: function () {
            ajaxloader($('#awb_table_cc'));
        },
        data: {
            client: $('#awb_report_cc_form #client').val(),
            status: $('#awb_report_cc_form #status').val(),
            start_date: $('#awb_report_cc_form #start_date input').val(),
            end_date: $('#awb_report_cc_form #end_date input').val()
        },
        success: function (response) {
            $('#awb_table_cc').html(response);
        }
    });
});

$('#awb_report_cc_form input').on('change', function () {
    $.ajax({
        type: 'GET',
        url: '/transit/awb/report_cc',
        cache: true,
        beforeSend: function () {
            ajaxloader($('#awb_table_cc'));
        },
        data: {
            client: $('#awb_report_cc_form #client').val(),
            status: $('#awb_report_cc_form #status').val(),
            start_date: $('#awb_report_cc_form #start_date input').val(),
            end_date: $('#awb_report_cc_form #end_date input').val()
        },
        success: function (response) {
            $('#awb_table_cc').html(response);
            closeLoader();
        }
    });
});


$('#awb_table_cc #status').live('change', function () {
    var awb = $(this).closest('tr').attr('id');
    var status = $(this).closest('tr').find('#status').val();
    if (status == 'SCH') {
        $(this).closest('tr').find('#reason_' + awb).datepicker({
            dateFormat: 'yy-mm-dd'
        }).focus();
    } else {
        $(this).closest('tr').find('#reason_' + awb).datepicker('destroy');
    }
});


$('#awb_table_cc button').live('click', function () {
    var awb = $(this).closest('tr').attr('id');
    var status = $(this).closest('tr').find('#status').val();
    var remark = $(this).closest('tr').find('#remark').val();
    var reason = $(this).closest('tr').find('#reason_' + awb).val();
    if (status == 'SCH' && reason == '') {
        alert('Please choose scheduled date');
        $(this).closest('tr').find('#reason_' + awb).focus();
    } else if (remark == 'Other' && reason == '') {
        alert('Please enter a reason');
        $(this).closest('tr').find('#reason_' + awb).focus();
    } else if (remark == '') {
        alert('Please select a remark');
        $(this).closest('tr').find('#remark').focus();
    } else {
        $.ajax({
            type: 'POST',
            url: '/transit/awb/update_by_cc',
            cache: true,
            data: {
                awb: awb,
                status: status,
                remark: remark,
                reason: reason
            },
            success: function (response) {
                get_message();
            }
        });
        $(this).closest('tr').fadeOut('slow');
    }
});
