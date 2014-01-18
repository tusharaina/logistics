function barplot(barobj) {
    /*data needed by barplot inside barobj are
     1-main title
     2-main subtitle
     3-x-axis categories which will be a array of strings
     4- y-axis title
     5-series name
     6-and final series data
     */
    var chart;

    chart = new Highcharts.Chart({
        chart: {
            renderTo: 'graph',
            type: 'column'
        },
        title: {
            text: barobj["title"] //changeable
        },
        subtitle: {
            text: barobj["subtitle"] //changeable
        },
        xAxis: {
            categories: barobj["categories"], //changeable
            title: {text: barobj.x_title}
        },
        yAxis: {
            min: 0,
            title: {
                text: barobj["y_title"]
            }
        },
        legend: {
            layout: 'vertical',
            backgroundColor: '#FFFFFF',
            align: 'left',
            verticalAlign: 'top',
            x: 100,
            y: 70,
            floating: true,
            shadow: true
        },
        tooltip: {
            formatter: function () {
                return '' +
                    this.x + ': ' + this.y + barobj['y_unit'];
            }
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [
            {
                name: barobj["x_title"],
                data: barobj["series_data"]  //changeable(actual data array)

            }
        ]
    });
}