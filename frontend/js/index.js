function showComment(button_id) {
    var x = document.getElementById("comment"+button_id);
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}

function toggleTheme() { 
            // Obtains an array of all <link> 
            // elements. 
            // Select your element using indexing. 
            var theme = document.getElementsByTagName('link')[4]; 
  
            // Change the value of href attribute  
            // to change the css sheet. 
            if (theme.getAttribute('href') == 'css/boy-theme.css') { 
                theme.setAttribute('href', 'css/girls-theme.css'); 
            } else { 
                theme.setAttribute('href', 'css/boy-theme.css'); 
            } 
        } 