function setChartWidth(){
  $('.resizable-chart').each(function(){
    $(this).width($(this).parent().width());
  })   
}
