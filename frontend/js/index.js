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
function MaintoggleTheme() { 
            // Obtains an array of all <link> 
            // elements. 
            // Select your element using indexing. 
            var theme = document.getElementsByTagName('link')[5]; 
  
            // Change the value of href attribute  
            // to change the css sheet. 
            if (theme.getAttribute('href') == 'css/boy-theme.css') { 
                theme.setAttribute('href', 'css/girls-theme.css'); 
            } else { 
                theme.setAttribute('href', 'css/boy-theme.css'); 
            } 
        }


$(document).ready(function() {
    $(".menu-toggle").on("click", function() {
      $(".nav").toggleClass("showing");
      $(".nav ul").toggleClass("showing");
    });
  
    $(".post-wrapper").slick({
      dots: true,
      infinite: false,
      speed: 300,
      slidesToShow: 3,
      slidesToScroll: 1,
      nextArrow: $(".next"),
      prevArrow: $(".prev"),
      responsive: [
        {
          breakpoint: 1024,
          settings: {
            slidesToShow: 3,
            slidesToScroll: 3,
            infinite: true,
            dots: true
          }
        },
        {
          breakpoint: 600,
          settings: {
            slidesToShow: 2,
            slidesToScroll: 2
          }
        },
        {
          breakpoint: 480,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1
          }
        }
        // You can unslick at a given breakpoint now by adding:
        // settings: "unslick"
        // instead of a settings object
      ]
    });
  });
  
  ClassicEditor.create(document.querySelector("#body"), {
    toolbar: [
      "heading",
      "|",
      "bold",
      "italic",
      "link",
      "bulletedList",
      "numberedList",
      "blockQuote"
    ],
    heading: {
      options: [
        { model: "paragraph", title: "Paragraph", class: "ck-heading_paragraph" },
        {
          model: "heading1",
          view: "h1",
          title: "Heading 1",
          class: "ck-heading_heading1"
        },
        {
          model: "heading2",
          view: "h2",
          title: "Heading 2",
          class: "ck-heading_heading2"
        }
      ]
    }
  }).catch(error => {
    console.log(error);
  });
          
$('.responsive').slick({
    dots: true,
    infinite: false,
    speed: 300,
    slidesToShow: 4,
    slidesToScroll: 4,
    responsive: [
        {
        breakpoint: 1024,
        settings: {
            slidesToShow: 3,
            slidesToScroll: 3,
            infinite: true,
            dots: true
        }
        },
        {
        breakpoint: 600,
        settings: {
            slidesToShow: 2,
            slidesToScroll: 2
        }
        },
        {
        breakpoint: 480,
        settings: {
            slidesToShow: 1,
            slidesToScroll: 1
        }
        }
        // You can unslick at a given breakpoint now by adding:
        // settings: "unslick"
        // instead of a settings object
    ]
    });