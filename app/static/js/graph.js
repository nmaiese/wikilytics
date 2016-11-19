function formatCrossifilter(data){

    var dateFormat = d3.time.format('%Y%m%d');



    data.forEach(function (d) {

      var date = d.timestamp.substr(0,8);
      d.timestamp = dateFormat.parse(date);

      d.views = +d.views;
    });

    ndx = crossfilter(data);
    return ndx;
}


function createDimension(ndx, dimension){
  ndxDim = ndx.dimension(function(d){
    return d[dimension];
  })
  return ndxDim;
}



function renderDashboardCharts(data){

    var ndx = formatCrossifilter(data);

    var dateDim = createDimension(ndx, "timestamp");
    var viewsDim = createDimension(ndx, "views");

    var minDate = dateDim.bottom(1)[0].timestamp;
    var maxDate = dateDim.top(1)[0].timestamp;


    var viewsByDate = dateDim.group().reduceSum(function(d) {
        return d.views;
    });



    //Define values (to be used in charts)

    //Inizializate Charts
    var viewsLineChart = dc.lineChart('#views-line-chart');

    var viewsBarChart = dc.barChart('#views-bar-chart');

//    Add Basic Attribute for line charts
    linechartAttribute(viewsLineChart);
    barchartAttribute(viewsBarChart);

    viewsLineChart
      .x(d3.time.scale().domain([minDate, maxDate]))
      .dimension(dateDim)
      .group(viewsByDate, 'Views by day')
      .rangeChart(viewsBarChart);

    viewsBarChart
      .x(d3.time.scale().domain([minDate, maxDate]))
      .dimension(dateDim)
      .group(viewsByDate, "Views by day");

    dc.renderAll();
}



function linechartAttribute(linechart){
  linechart
  .width($('.col-md-12').width())
  .height(280)
  .margins({
      top: 15,
      right: 50,
      bottom: 40,
      left: 60
  })
  .round(d3.time.day.round)
  .xUnits(d3.time.months)
  .brushOn(false)
  .elasticY(true)
  .renderArea(true)
  .mouseZoomable(false)
  .renderHorizontalGridLines(true)
  .transitionDuration(1000)
  .yAxis().tickFormat(d3.format(".2s"));
}

function barchartAttribute(barchart){
  barchart
  .width($('.col-md-12').width())
  .height(100)
  .margins({
      top: 15,
      right: 50,
      bottom: 40,
      left: 60
  })
  .centerBar(true)
  .xUnits(d3.time.days)
  .yAxis().ticks(0);

}
