function submitInfo() {
    $.ajax({
        type: "get",
        url: "/result",
        data: {
            "name": $('#name').val(),
            "equipment": $('#equipment').val()
        },
        success: function(data) {

        }
    });
    return false;
}