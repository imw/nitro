$(document).ready(function() {
    console.log("test")
    $(chart_id).highcharts({
        chart: chart,
        title: title,
        xAxis: xAxis,
        yAxis: yAxis,
        series: series
    });
});

