var dateDim
var viewsByArticle

function formatCrossifilter(data){

    var dateFormat = d3.time.format('%Y%m%d');



    data.forEach(function (d) {

      var date = d.timestamp.substr(0,8);
      d.timestamp = dateFormat.parse(date);
      d.project = d.project.replace('.wikipedia', '');
      d.views = +d.views;
      d.article = d.article.replace(/_/g, ' ')
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

    dateDim = createDimension(ndx, "timestamp");
    var viewsDim = createDimension(ndx, "views");
    var langDim = createDimension(ndx, "project")
    var articleDim = createDimension(ndx, "article")

    var minDate = dateDim.bottom(1)[0].timestamp;
    var maxDate = dateDim.top(1)[0].timestamp;



    var viewsByDate = dateDim.group().reduceSum(function(d) {
      return d.views;
    });

    var viewsByLang = langDim.group().reduceSum(function(d){
      return d.views
    })

    viewsByArticle = articleDim.group().reduceSum(function(d){
      return d.views
    })



    // test = dateDim


    // var dayViewsByArticle = dateDim.group().reduce(      
    //   function (d, v) {
    //     (viewsByArticle.top(Infinity)).forEach(function(p){
    //       if (v.article == p.key){
    //         console.log(d)
    //         console.log(p.key.replace(" ","")+"_views")
    //         d.views = v.views

    //         d[p.key.replace(" ","")+"_views"] += v.views
    //         return d
    //       }
    //     })
    //   },

    //   function (d, v) {
    //     (viewsByArticle.top(Infinity)).forEach(function(p){
    //       if (v.article == p.key){
    //         d[p.key.replace(" ","")+"_views"] += v.views
    //         return d
    //       }
    //     })
    //   },

    //   function () {
    //     viewsByArticle.top(Infinity).forEach(function(p){
    //       returned = {} 
    //         returned += eval(p.key.replace(" ","")+":0")
    //       })
    //     return returned 
        
    //   }
    // );


    //Define values (to be used in charts)

    //Inizializate Charts

    var viewsLineChart = dc.lineChart('#views-line-chart');
    var viewsBarChart = dc.barChart('#views-bar-chart');
    var langPieChart = dc.pieChart('#langs-pie-chart');
    var articleRowChart = dc.rowChart('#article-row-chart');

//    Add Basic Attribute for line charts
    linechartAttribute(viewsLineChart);
    barchartAttribute(viewsBarChart);

    viewsLineChart
      .x(d3.time.scale().domain([minDate, maxDate]))
      .dimension(dateDim)
      .group(viewsByDate, 'Views by day')
      //.stack(dayViewsByArticle, function(d){console.log(d)})
      .rangeChart(viewsBarChart);

    viewsBarChart
      .x(d3.time.scale().domain([minDate, maxDate]))
      .dimension(dateDim)
      .group(viewsByDate, "Views by day");

    langPieChart
      .radius(120)
      .height(280)
      .dimension(langDim)
      .group(viewsByLang);

    articleRowChart
      .width(null)
      .height(280)
      .margins({
        top: 15,
        right: 50,
        bottom: 40,
        left: 60
      })
      .dimension(articleDim)
      .group(viewsByArticle)
      .elasticX(true);


    setChartWidth();
    dc.renderAll();
    
}



function linechartAttribute(linechart){
  linechart
  .width(null)
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
  .width(null)
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
