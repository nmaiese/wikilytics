$('input#name').attr('data-role','tagsinput')
$("input#name").val();

$('#data-form').on('keyup keypress', function(e) {
  var keyCode = e.keyCode || e.which;
  if (keyCode === 13) {
    e.preventDefault();
    return false;
  }
});


function datePickerSet(start, end) {
  $( function() {
      $( ".datepicker" ).datepicker();
  } );

  $('input#datarangepicker').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
  $('input#datarangepicker').daterangepicker({
    startDate: start,
    endDate: end,
    maxDate: end,
    minDate: '05/01/2015',
    ranges: {
     'Today': [moment(), moment()],
     'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
     'Last 7 Days': [moment().subtract(6, 'days'), moment()],
     'Last 30 Days': [moment().subtract(29, 'days'), moment()],
     'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')],
     'Last Year': [moment().subtract(364, 'days'), moment().subtract(1, 'days')]
    }
  }, datePickerSet);
}

function addAutocomplete(){

 $('.bootstrap-tagsinput').children('input').autocomplete({
  source: function (request, response) {
    var term = request.term;
    var restUrl = 'https://it.wikipedia.org/w/api.php?action=query&list=search&srsearch='+term+'&format=json';

    $.ajax( {
      url: restUrl,
      jsonp: "callback",
      dataType: 'jsonp',
      data: {
        action: "query",
        list: "search",
        srsearch: request.term,
        format: "json"
      },
      xhrFields: { withCredentials: true },
      success: function(data) {
        response($.map(data.query.search, function (item) {
          return {
            label: item.title,
            value: item.title
          }
        }))
      }

    });
  }})
}

function composeLinechartTooltip(d){
  return "<strong>" + d.layer.replace(/_/g," ") + "</strong> <br/> " +
   numberFormat(d.data.value) + "<br/>" +
   formatDate(d.data.key)

}

function composeBarchartTooltip(d){
  return "<strong>" + d.layer.replace(/_/g," ") + "</strong> <br/> " +
   numberFormat(d.y) + "<br/>" +
   formatDate(d.data.key)
}

function formatDate(data){
  d3Date = d3.time.format("%d/%m/%Y")
  return d3Date(data)
}


function removeSpecial(word){
    return word.replace(/[^A-Z0-9]/ig, "")
}


function fromDataToCharts(data, query){
  $( document ).ready(function() {
    addAutocomplete();
    if(data && data != "None" && data != [] && data != '[]') {
      renderDashboardCharts(data, query);
    }
  });
  $(window).resize(function(){
    setChartWidth();
    dc.renderAll();
  });
  addArticlesDesc()
}

function rangesEqual(range1, range2) {
  if (!range1 && !range2) {
      return true;
  }
  else if (!range1 || !range2) {
      return false;
  }
  else if (range1.length === 0 && range2.length === 0) {
      return true;
  }
  else if (range1[0].valueOf() === range2[0].valueOf() &&
      range1[1].valueOf() === range2[1].valueOf()) {
      return true;
  }
  return false;
}

function applyRangeChart(rangeChart, chartlist){
  rangeChart.focusCharts = function(charts) {
    if (!arguments.length) {
      return this._focusCharts;
    }
    this._focusCharts = chartlist; // only needed to support the getter above
    this.on('filtered', function(range_chart) {
      if (!range_chart.filter()) {
        dc.events.trigger(function() {
          chartlist.forEach(function(focus_chart) {
            if (focus_chart.anchorName() != "community-goal-chart" && focus_chart.anchorName() != "engagement-goal-chart"){
              focus_chart.x().domain(focus_chart.xOriginalDomain());
            }
          });
        });
      }
      else chartlist.forEach(function(focus_chart) {
        if (focus_chart.anchorName() == "community-goal-chart") {
          focus_chart.needleValue(dateDim.top(1)[0].community)
          .redraw();
        }
        if (focus_chart.anchorName() == "engagement-goal-chart") {
          focus_chart.needleValue(getEngagementSum(fbEngagementDim))
          .redraw();
        }
        if (!rangesEqual(range_chart.filter(), focus_chart.filter()) && focus_chart.anchorName() != "community-goal-chart" && focus_chart.anchorName() != "engagement-goal-chart") {
          dc.events.trigger(function() {
            focus_chart.focus(range_chart.filter());
          });
        }
      });
    });
    return this;
  };
  rangeChart.focusCharts(chartlist);
}

function addArticlesDesc(){
    var i = 0
    articles_desc.forEach(function(d){
        $link = $('<a href="'+d['url']+'" target="_blank"></a>')
        if (i >= 3){ $col= $('<div class="col-md-6"></div>')}
        else{ $col = $('<div class="col-md-4"></div>')}
        if (i==0 | i==3){ $row = $('<div class="row"></div>') }
        title = '<h4>'+d['title']+'</h4>'
        $article = $('<div class="article"></div>')
        image = '<img src="'+d['image'].replace("//","https://")+'" />'
        desc = '<p>'+d['description']+'</p>'
        i++

        $('#wikipedia-results').append($row.append($col.append($link.append($article.append(title, image, desc)))))
    })
}








