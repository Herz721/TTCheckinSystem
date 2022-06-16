function submitInfo() {
    console.log($('#device').val())
    $.ajax({
        type: "get",
        url: "/result",
        data: {
            "name": $('#name').val(),
            "device": $('#device').val(),
            "dev_name":$('#device_name').val()
        },
        success: function(data) {}
    });
    return false;
}

function feedback() {
    // Validate registeration
    let device = document.querySelector("#device").value;
    let name = document.querySelector("#device_name").value;
    const devices = new Set(["phone", "pad", "pc", "other"]);
    if (!name) {
        alert("Missing Name");
        return app.send_static_file("index.html");
    } else if (!devices.has(device)) {
        alert("Missing Device");
        return app.send_static_file("index.html");
    }
    // Confirm registeration
    alert("Hello, " + name + "! You've successfully registered! ");
}