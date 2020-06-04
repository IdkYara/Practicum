function openAside() {
    //  $("aside").width("250px");
    $("aside").animate({
        width: "250px"
    }, 500, function () {
        $("#aside-content").show();
        $("#aside-open").hide();
        $("#aside-close").show();

    });
}

function closeAside() {
    $("#aside-content").hide();

    $("aside").animate({
        width: "20px"
    }, 500, function () {
        $("#aside-open").show();
        $("#aside-close").hide();
    });
}
