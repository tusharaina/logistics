$(document).ready(function () {
    plotgraphs();
});

function plotgraphs() {
    $.get(location.href + '?type=charts&graph_type=branch_incoming', function (data) {
        if (data.invalid_request) {
            alert(data);
        }
        else {
            pieplot(data, 'manifest_graph');
        }
//            location.reload();
    });
//     $.get(location.href+'?type=charts&graph_type=branch_drs',function(data){
//            if(data.invalid_request){
//                alert(data);
//            }
//            else{
//                pieplot(data, 'drs_graph');
//            }
////            location.reload();
//        });
}