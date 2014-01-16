function pieplot(arg_object, div_id) {
//    var getColor = [
//
//   '#2f7ed8',
//   '#0d233a',
//   '#8bbc21',
//   '#910000',
//   '#1aadce',
//   '#492970',
//   '#f28f43',
//   '#77a1e5',
//   '#c42525',
//   '#a6c96a',
//        '#CCFF99',
//        '#CC00CC',
//        '#990033',
//        '#009933',
//        '#003300',
//        '#FFFF99',
//        '#003366',
//        '#FF9933'
//
//];
    var chart;
    var data = [];                                            //upto here
    for (var i = 0; i < arg_object.data_list.length; i++) {
        data.push({name: arg_object.series_name[i], y: arg_object.data_list[i]});
    }


    chart = new Highcharts.Chart(
        {
            tooltip: {
                percentageDecimals: 1,

                pointFormat: 'value: {point.y}<br/>percentage <b>{point.percentage:.1f}%</b>'
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: false
                    },
                    showInLegend: true,
                    colorByPoint: true
                }

            },

            series: [
                {
                    type: "pie",
                    sliced: true,
                    data: data,
                    pointWidth: 15,
                    color: "#C6D9E7",
                    borderColor: "#8BB6D9",
                    shadow: true
                }
            ],
            title: {
                text: arg_object.title
            },
            legend: {
                layout: "horizontal",
                style: {
                    left: "auto",
                    bottom: "auto",
                    right: "auto",
                    top: "auto"
                }
            },
            chart: {
                renderTo: div_id
            },
            credits: {
                enabled: false
            }
        }
    );

}