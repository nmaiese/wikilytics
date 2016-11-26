
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






// $('input#name').attr('data-role','tagsinput')
// $("input#name").val();

$("input#name").autocomplete({
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
                    console.log(item)
                    return{
                    label: item.title,
                    value: item.title
                  }

                }))
              }

        });
    }})

// $("input#name").autocomplete({
//             //lookup: countries,
//   serviceUrl:'https://it.wikipedia.org/w/api.php?action=query&list=search&format=json&srsearch=',
//   //tell the script where to send requests
//   type:'POST',
//    width: 450, //set width
//   //callback just to show it's working
//   onSelect: function (suggestion) {
//     $('#selection').html('You selected: ' + suggestion.value + ', ' + suggestion.data);
//   },
//   showNoSuggestionNotice: true,
//   noSuggestionNotice: 'Sorry, no matching results',

//   });




// $('input#name').autocomplete({
//     serviceUrl: 'https://it.wikipedia.org/w/api.php?action=query&list=search&format=json&srsearch=',
//     onSelect: function (suggestion) {
//       console.log(suggestion)
//         alert('You selected: ' + suggestion.value + ', ' + suggestion.data);
//     },
//     ajaxSettings: {
//           jsonp: "callback",
//           dataType: 'jsonp',
//           data: {
//             action: "query",
//             list: "search",
//             format: "json"
//           },

//       xhrFields: { withCredentials: true },
//     }

// });

