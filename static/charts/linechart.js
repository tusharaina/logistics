function linechart_continous(arg_object) {
    chart = new Highcharts.Chart({
        chart: {
            renderTo: 'graph',
            zoomType: 'x',
            type: 'line'
        },
        title: {
            text: arg_object['title']
        },
        subtitle: {
            text: arg_object['subtitle']
        },
        xAxis: {
            type: 'datetime',

            dateTimeLabelFormats: { // don't display the dummy year
                hour: '%H:%M',
                day: '%e. %b',
                week: '%e. %b',
                month: '%b', //month formatted as month only
                year: '%Y'

            }
        },
        yAxis: {
            title: {
                text: arg_object['y_title']
            }

        },
        tooltip: {

            formatter: function () {
                return '<b>' + this.series.name + '</b><br/>' +
                    Highcharts.dateFormat('%e. %b', this.x) + ': ' + this.y + arg_object['y_unit'];
            }
        },

        series: arg_object.series
    });

}

function lineplot(arg_object) { //used for circuits and energy consumed
    /*accepts object as parameter
     object attributes are
     1-timestamps(array)
     2-total_data_list
     3-min_y
     4-max_y
     5-y-axis_name
     6-series_name
     7-y-axis_text
     8-x-axis_text
     9-y-min
     10-y-max
     */
//    var data = json_timestamp_to_javascript_and_chart_data(arg_object['timestamps'],arg_object['data_list']);
//    alert(data);

    return sec_plotter(arg_object);
//    var data_objects =[];                            //TODO UNCOMMENT IF NEEDED contains lineplot continous type chart parsing of data
//    var index = 0;
//    var time =datetimeparser(arg_object.start);
//var series = [];
//    var starttime = Date.UTC(time.year,time.month,time.day,time.hour);
//    if(arg_object['data_list_count']==1){
//    var data = arg_object['data_list'][0];
//        series=[{
//                pointInterval:3600*1000,
//            pointStart:starttime,
//            name: arg_object['series_name'][0],
//            data: data
//        }];}
//    else if(arg_object['data_list_count']>1){
//       for(var l=0;l<arg_object['data_list_count'];l++){
//           series.push({pointInterval:24*3600*1000,
//               pointStart:starttime,
//               name: arg_object['series_name'][l],
//               data:arg_object['data_list'][l]
//
//           });
//       }
//    }
//arg_object.series = series;
//linechart_continous(arg_object);

}

function sec_lineparser_for_circuits(arg_object) {
    var series = [];
    for (var i = 0; i < arg_object.data_list_count; i++) {

        var data_arr = json_timestamp_to_javascript_and_chart_data(arg_object.timestamps, arg_object.data_list[i], true);

        series.push({data: data_arr,
            name: arg_object.series_name[i],
            dataGrouping: {
                enabled: true
            }
        });
    }
    return series;

}
function sec_plotter(arg_object) {
    var series = sec_lineparser_for_circuits(arg_object);
    arg_object.series = series;

    linechart_continous(arg_object);
}


function linechart_discreet_time(arg_object) {
    chart = new Highcharts.Chart({
        chart: {
            renderTo: 'graph',
            type: 'spline',
            zoomType: 'x'
        },
        rangeSelector: {
            buttons: [
                {
                    type: 'day',
                    count: 1,
                    text: 'Day'
                },
                {
                    type: 'all',
                    count: 1,
                    text: 'All'
                }
            ],
            selected: 1

        },
        title: {
            text: arg_object.title
        },
        subtitle: {
            text: arg_object['subtitle']
        },
        xAxis: {
            type: 'datetime',
            minRange: 3600 * 1000,
            dateTimeLabelFormats: {
                hour: '%H:%M',
                day: '%e. %b',
                month: '%e. %b'
            },
            title: {
                text: arg_object.x_title
            }
        },
        yAxis: {
            title: {
                text: arg_object.y_title
            },
            min: 0
        },
        tooltip: {
            formatter: function () {
                if (arg_object.type == 'peak_power') {
                    return '<b>' + " " + this.series.name + " " + '</b><br/>' +
                        Highcharts.dateFormat('%e. %b', this.x) + " " + ':' + arg_object.tooltip_list_name + " " + arg_object.tooltip_list[this.point.myIndex] + arg_object.tooltip_list_unit;
                }
                else {
                    return '<b>' + this.series.name + '</b><br/>' +
                        Highcharts.dateFormat('%e. %b', this.x) + ': ' + this.y + arg_object.y_unit;
                }
            }
        },

        series: arg_object.series
    });
}


function async_chart(arg_object) {


    window.chart = new Highcharts.StockChart({
        chart: {
            renderTo: 'graph',
            type: 'spline',
            zoomType: 'x',
//                events:{
//                    selection:function(){
//                        var extremes = chart.xAxis[0].getExtremes();
//                        var datamin = chart.series[0].data[0][0];//this is first time for which data exists
//                        var datamax = extremes.dataMax;
//                        chart.xAxis[0].setExtremes(datamin,datamax);
//
//                    }
//                }
            events: {
                redraw: function () {
                    this.xAxis.startOnTick = true;
                }
            }
        },

        navigator: {
            enabled: false
        },

        title: {
            text: arg_object.title
        },

        subtitle: {
            text: arg_object.subtitle
        },
        yAxis: {
            title: {
                text: arg_object.y_title
            },
            startOnTick: true

        },

        rangeSelector: {
            enabled: false
//                buttons: [{
//                    type: 'hour',
//                    count: 1,
//                    text: '1h'
//                }, {
//                    type: 'day',
//                    count: 1,
//                    text: '1d'
//                }, {
//                    type: 'month',
//                    count: 1,
//                    text: '1m'
//                }, {
//                    type: 'year',
//                    count: 1,
//                    text: '1y'
//                }, {
//                    type: 'all',
//                    text: 'All'
//                }],
//
//                selected : 4 // all
        },

        xAxis: {
            type: 'datetime',
            events: {
                afterSetExtremes: afterSetExtremes
            },
            title: {
                text: arg_object.x_title},
            minRange: 3600 * 1000,
////                // one hour
            startOnTick: true
        },


        series: arg_object.series
//                data : data,
//                dataGrouping: {
//                    enabled: false
//                }

    });

}
function afterSetExtremes(e) {
    var series = null;
    var range = e.max - e.min; //inmilliseconds
    var min = e.min;
    var max = e.max;
    var delta = max - min;
    if (delta / (1000 * 3600) <= 1) {

        return;
    }
    if (window.Objectsholder.graph_type[0] == 'CIRCUITS') {
        chart.showLoading('Loading data from server...');
        $.getJSON('http://127.0.0.1:8000/graph/?data_type=' + window.Objectsholder.primary_click + '&durations=' + range.toString() + '&duration_resolution=not_fixed&graph_type=' + window.Objectsholder.graph_type[0] + '&start=' + (min).toString() + '&end=' + (max).toString()
            + '&type=' + window.Objectsholder.graph_type[1] +
            '&' + window.Objectsholder.graph_type[2][0] + '=' + window.Objectsholder.graph_type[2][1], function (data) {
            $.each(data, function (key, val) {

                if (key == 'objects') {
                    if (val == 'None') {

                        chart.hideLoading();
                        return;
                        //last resort is chart redraw
                    }
                    var arg_object = {};
                    if (window.Objectsholder.graph_type[1] == 'indivisual') {

                        arg_object = dataparser_indivisual(key, val);
                        series = sec_lineparser_for_circuits(arg_object); //series is an array of objects with keys objects and name
                        for (var i = 0; i < chart.series.length; i++) {
                            chart.series[i].setData(series[i].data);

                        }
                        chart.xAxis.startOnTick = true;
                        chart.redraw();
                        chart.hideLoading();
                    }
                    else if (window.Objectsholder.graph_type[1] == 'function') {

                        arg_object = dataparser_function(key, val);

                        series = sec_lineparser_for_circuits(arg_object);

                        //series is an array of objects with keys objects and name
                        for (var i = 0; i < chart.series.length; i++) {
                            chart.series[i].setData(series[i].data);
                        }
                        chart.xAxis.startOnTick = true;
                        chart.redraw();
                        chart.hideLoading();

                    }
                    else if (window.Objectsholder.graph_type[1] == 'room') {

                        arg_object = dataparser_room(key, val);
                        series = sec_lineparser_for_circuits(arg_object); //series is an array of objects with keys objects and name
                        for (var i = 0; i < chart.series.length; i++) {
                            chart.series[i].setData(series[i].data);
                        }
                        chart.xAxis.startOnTick = true;

                    }

                    chart.redraw();
                    chart.hideLoading();
                }
            });

        });
    }

}


function lineplot_discreet_time_peak(arg_object) {

    var series = [];
    var data_obj = {};
    data_obj.name = arg_object.series_name;
    data_obj.data = [];

    data_obj.data = json_timestamp_to_javascript_and_chart_data(arg_object.timestamps, arg_object.data_list, false);

    if (arg_object['type'] == 'peak_power') {
        data_obj.data = prepare(data_obj.data);
    }
    series.push(data_obj);
    arg_object.series = series;

    linechart_discreet_time(arg_object);
}

function datetimeparser(data) {
    var datetime = {};
    var broken = data.split("-");

    datetime["year"] = parseInt(broken[0]);
    datetime["month"] = parseInt(broken[1]);//
    var shattered = broken[2].split(":");
    datetime["minute"] = parseInt(shattered[1]);
    datetime["second"] = parseInt(shattered[2]);
    var fines = shattered[0].split('T');

    if (fines[0][0] == '0') {

        fines[0] = fines[0].slice(1);

    }
    if (fines[1][0] == '0') {
        fines[1] = fines[1].slice(1);
    }
    //08 and 09 are getting converted into 0,0
    datetime['day'] = parseInt(fines[0]);
    datetime['hour'] = parseInt(fines[1]);

    return datetime;
}


function json_timestamp_to_javascript_and_chart_data(timestamp_array, data_list, get_timestamp_hour) { //returns data array of type [[time,data][time,data][time,data]]
    var data = [];
    for (var i = 0; i < timestamp_array.length; i++) {  ///months are zero based

        var jdatetime = datetimeparser(timestamp_array[i]);
        jdatetime.month = jdatetime.month - 1;
//         alert(Date.UTC(2012,jdatetime["month"],jdatetime["day"],jdatetime.hour));
        if (get_timestamp_hour)
            data.push([Date.UTC(jdatetime["year"], jdatetime["month"], jdatetime["day"], jdatetime.hour), data_list[i]]);
        else
            data.push([Date.UTC(jdatetime["year"], jdatetime["month"], jdatetime["day"]), data_list[i]]);
    }

    return data;
}

function prepare(dataArray) {
    return dataArray.map(function (item, index) {
        return {x: item[0], y: item[1], myIndex: index};
    });
}