function fromDataToCharts(data, query){
    $( document ).ready(function() {


        if(data && data != "None" && data != [] && data != '[]') {

            data = data.replace(/l&#39;/g,'l_')
            data = data.replace(/d&#39;/g,'d_')
            data = data.replace(/D&#39;/g,'D_')
            data = data.replace(/l&#39;/g,'L_')
            data = data.replace(/u&#39;/g,'"')
            data = data.replace(/&#39;/g,'"')
            data = data.replace(/u&#34;/g,'"')
            data = data.replace(/&#34;/g,'"')
            data = data.replace(/[\])[(]/g, '')
            data = '['+data+']'

            json = JSON.parse(data)
            renderDashboardCharts(json, query);
        }

    });
    $(window).resize(function(){
      setChartWidth();
      dc.renderAll();
    });
}



function datePickerSet(start, end) {

    $( function() {
        $( ".datepicker" ).datepicker();
    } );

    $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
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
