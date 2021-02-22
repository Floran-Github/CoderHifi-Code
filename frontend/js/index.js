function showComment(button_id) {
    var x = document.getElementById("comment"+button_id);
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}

