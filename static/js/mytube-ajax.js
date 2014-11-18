$(document).ready(function() {
    $('#likes').click(function(){
    var genreid;
    catid = $(this).attr("data-genreid");
    $.get('/mytube/like_genre/', {genre_id: genreid}, function(data){
        $('#like_count').html(data);
        $('#likes').hide();
       });
    });

    /*$('#suggestion').keyup(function(){
            var query;
            query = $(this).val();
            $.get('/mytube/search_movie/', {suggestion: query}, function(data){
             $('#cats').html(data);
            });
    });*/

    $('#search').click(function(){
        var sel = document.getElementById('genre');
        var genre_id;
        genre_id = sel.options[sel.selectedIndex].value;
        var movie_title;
        movie_title = $('#title').val();
        var movie_pg;
        movie_pg = $('#pg').val();
        $.get('/mytube/search_movie/', {genre: genre_id, title: movie_title, pg: movie_pg}, function(data){
            $('#movies').html(data);
        });
    });

    $('.bxslider').bxSlider();

});