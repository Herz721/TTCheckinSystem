function submitInfo() {
    console.log($('#device').val())
    $.ajax({
        type: "get",
        url: "/result",
        data: {
            "name": $('#name').val(),
            "device": $('#device').val()
        },
        success: function(data) {
        }
    });
    return false;
}