window.onload = initall;
var  saveBookButton ;
// function initall() {
//     saveBookButton=document.getElementById('save_ans')
//     saveBookButton.onclick = save_ans;
// }
// function save_ans() {
//   //   var ans = $("input:radio[name=name]:checked").val()
//   //   alert("answer submited go next")
//   //   var url = '/save_ans?ans='+ans
//   //   var req = new XMLHttpRequest();
//   //   req.onreadystatechange = function() {
//   //   if (this.readyState == 4 && this.status == 200) {
//   //   }
//   // };
//   // req.open("GET", url, true);
//   // req.send();

// }
function getanswer(){
  var useranswer = [];
  var ele = document.getElementsByTagName('input');

  for(i=0;i<ele.length;i++){
    if(ele[i].type="radio") { 
      if(ele[i].checked){        
        useranswer.push(ele[i].value)
      }
  } 

  }  
  return useranswer;
}
console.log('data in')

$('#save_ans').click(function() {
 
  var tasks = getanswer();
  console.log("yo");
  console.log(tasks);
  
  $.ajax({
      headers: { "X-CSRFToken": $.cookie("csrftoken") },
      type: 'POST',
      url: '/quiz/1',
      data: {'ans[]': tasks},
      success: function(data) {
          if(data.status == 'fail'){
              alert(data.msg)
          }else if(data.status == 'success'){
            console.log('madarcod')
              // window.location.href='/sale';//refresh current page.
          }
      },
  });                                                                                                                      xc                                                     `                                                                                                                                                                                                     `
});