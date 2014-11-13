$(document).ready(function() {
    $('#likes').click(function(){
    var genreid;
    catid = $(this).attr("data-genreid");
    $.get('/mytube/like_genre/', {genre_id: genreid}, function(data){
        $('#like_count').html(data);
        $('#likes').hide();
       });
    });

    $('#suggestion').keyup(function(){
            var query;
            query = $(this).val();
            $.get('/mytube/suggest_category/', {suggestion: query}, function(data){
             $('#cats').html(data);
            });
    });


});