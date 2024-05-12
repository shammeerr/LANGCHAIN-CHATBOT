$(document).ready(function() {
    // Toggle between day and night mode
    $("#day-mode-btn").click(function() {
        $("#theme-style").attr("href", "day-mode.css");
    });

    $("#night-mode-btn").click(function() {
        $("#theme-style").attr("href", "night-mode.css");
    });

    // Your existing code goes here...
    // ...
});
