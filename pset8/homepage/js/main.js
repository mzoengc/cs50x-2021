$(function () {
    // load child html
    $("header").load("html/_header.html");
    $("footer").load("html/_footer.html");

    // Animation
    $("main").fadeOut(300, function() {
        $("#about").load("html/_about.html");
        $("#projects").load("html/_projects.html");
        $("main").fadeIn(1000);
    });

    // Change active nav link
    $.get("html/_header.html", function() {
        if (window.location.pathname == '/index.html') {
            $("#nav_index").addClass("active");
            $('#nav_index').prop('aria-current', "page");
        } else if (window.location.pathname == '/about.html') {
            $("#nav_about").addClass("active");
            $('#nav_about').prop('aria-current', "page");
            $("#about").addClass("main-container");
        } else if (window.location.pathname == '/projects.html') {
            $("#nav_projects").addClass("active");
            $('#nav_projects').prop('aria-current', "page");
            $("#projects").addClass("main-container");
        } else if (window.location.pathname == '/videos.html') {
            $("#nav_videos").addClass("active");
            $('#nav_videos').prop('aria-current', "page");
        }
    });
});