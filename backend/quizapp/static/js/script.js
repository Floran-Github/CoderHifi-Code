function getanswer() {
  var useranswer = [];
  var ele = document.getElementsByTagName("input");

  check = false
  for (i = 0; i < ele.length; i++) {
    if ((ele[i].type = "radio")) {
      if (ele[i].checked) {
        useranswer.push(ele[i].value);
        check = true
      }
    }
    if(i%4 === 0 && i !== 0){
      if(check === true){
        check = false
      }
      else{
        useranswer.push('')
      }
    }
  }
  return useranswer;
}

console.log("data in");
console.log(JSON.parse(document.getElementById('quiz').textContent));

$("#save_ans").click(function () {
  var tasks = getanswer();
  console.log("yo");
  console.log(tasks);
  
  $.ajax({
    type: "POST",
    url: "/quiz/check",
    data: { 
      "ans[]": tasks,
      "quizlevel": JSON.parse(document.getElementById('quiz').textContent),
    },
    success: function (data) {
      if (data.status == "fail") {
        alert(data.msg);
      } else if (data.status == "success") {
        console.log('uo')
        console.log(typeof(data))
        console.log(data);
        result(data.result,data.teststatus,data.mark,data.totalmark)
        // window.location.href='/sale';//refresh current page.
      }
    },
  });
});
function result(dataList,status,mark,total){
  document.getElementById('save_ans').style.display = 'none';
  document.getElementById('retake').style.display = 'block';
  document.getElementById('goback').style.display = 'block';
  document.getElementById('mark').style.display = 'block';
  document.getElementById('mark').innerHTML = `Marks obtained ${mark} out of ${total}`;
  document.getElementById('status').style.display = 'block';
  document.getElementById('status').innerHTML = `Status : ${status}`;

  var ele = document.getElementsByTagName("input");
  for (i = 1; i < ele.length; i++) {
    if ((ele[i].type = "radio")) {
      ele[i].disabled = true
    }
  }

  for(i = 0; i < dataList.length; i++){
    var questionEle = document.getElementsByClassName('question_sec');
    if (dataList[i] === 0){
      questionEle[i].style.border = '1px solid #FF0800'
      questionEle[i].style.background = '#EA3C53'
      
    } else {
      questionEle[i].style.border = '1px solid #00FF00'
      questionEle[i].style.background = '#32CD32'

    }
  }

}

$("#retake").click(() => { location.reload() })
