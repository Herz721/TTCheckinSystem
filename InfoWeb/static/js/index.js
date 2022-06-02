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

function feedback() 
    {
        // Validate registeration
        let name = document.querySelector("#name").value;
        let device = document.querySelector("#device").value;
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