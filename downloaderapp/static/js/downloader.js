//Prevent Resubmit page data
$(document).ready(function(){
    window.history.replaceState("","",window.location.href)
});