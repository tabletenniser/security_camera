$(document).ready(function(){
    $(".result").hover(function() {
        url = $(this).children('div.wordwrap').children('a.link').text()
        $("#preview_iframe").attr("src", url);
        $("#preview").css("display", "table-cell");
        $(".result").each(function() {
            $(this).css("background", "#EEEEFF")
        });
        $(this).css("background", "#CCCCEE")
    }, function() {
    });
    $("#result_container").hover(function() {
    },
    function() {
        // $("#preview_iframe").attr("src", '');
        // $("#preview").css("display", "none");
    })
});
