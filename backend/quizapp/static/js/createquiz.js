var index = 1
createSection()

function createSection(){
    console.log('youyo')
    var mainDiv = document.createElement('div')
    mainDiv.classList.add('row')
    mainDiv.classList.add('maindiv')
    
    question_tag = document.createElement('h5')
    question_tag.innerText = 'Question '
    mainDiv.appendChild(question_tag)
    var textareaDiv = document.createElement('div')
    textareaDiv.classList.add('row')
    
    var textarea = document.createElement('textarea')
    textarea.placeholder = 'Enter the question here'
    textarea.required = true
    textareaDiv.appendChild(textarea)

    var answerDiv = document.createElement('div')
    answerDiv.classList.add('row')
    var answer_tag = document.createElement('h5')
    answer_tag.innerText = 'Answers '
    answerDiv.appendChild(answer_tag)
    
    for(i = 0 ; i < 4; i++){
        
        var answer1Div = document.createElement('div')
        answer1Div.classList.add('col-md-6')
        answer1Div.classList.add('col-12')
        
        var ansDiv = document.createElement('div')
        ansDiv.classList.add('row')
        
        var checkDiv = document.createElement('div')
        checkDiv.classList.add('col-1')
        var inputDiv = document.createElement('div')
        inputDiv.classList.add('col-10')
        
        var ansCheck = document.createElement('input')
        ansCheck.setAttribute("type", "radio")
        ansCheck.id = `${i+1}${index}`
        ansCheck.classList.add('check')
        ansCheck.name = 'check'+index

        var ansText = document.createElement('input')
        ansText.setAttribute("type", "text")
        ansText.required = true
        ansText.classList.add('ans')
        ansText.validity.valid
        ansText.placeholder = 'Enter the answer here'
        ansText.id = `ans${i+1}${index}`

        checkDiv.appendChild(ansCheck)
        inputDiv.appendChild(ansText)
        ansDiv.appendChild(checkDiv)
        ansDiv.appendChild(inputDiv)
        answer1Div.appendChild(ansDiv)

        answerDiv.appendChild(answer1Div)
    }

    var marksDiv = document.createElement('div')
    marksDiv.classList.add('row')
    marksDiv.classList.add('marks')

    var textDiv = document.createElement('div')
    textDiv.classList.add('col-1')
    var h5 = document.createElement('h5')
    h5.innerText = 'Marks '
    textDiv.appendChild(h5)
    
    var marksInpDiv = document.createElement('div')
    marksInpDiv.classList.add('col-4')
    var marksInpt = document.createElement('input')
    marksInpt.setAttribute("type","number")
    marksInpDiv.appendChild(marksInpt)

    marksDiv.appendChild(textDiv)
    marksDiv.appendChild(marksInpDiv)


    mainDiv.appendChild(textareaDiv)
    mainDiv.appendChild(answerDiv)
    mainDiv.appendChild(marksDiv)

    document.getElementsByClassName('quiz')[0].appendChild(mainDiv)
    index += 1

}

$('input[type="checkbox"]').on('change', function() {
    $('input[name="' + this.name + '"]').not(this).prop('checked', false);
});

function checkForm(){
    var textEle = document.querySelectorAll('textarea')
    var inputELe = document.querySelectorAll('input')
    if(document.getElementById('module').value === 'none'){
        alert('select the module')
        return false
    }
    for(i = 0; i < textEle.length;i++){
        if(textEle[i].value === ''){
            alert('textarea empty please fill the form correctly')
            return false
        }
    }
    for(i =0; i < inputELe.length; i++){
        if(inputELe[i].type === 'text'  && inputELe[i].value === ''){
            alert('answer empty please fill the form correctly')
            return false

        }
        if(inputELe[i].type === 'number' && inputELe[i].value === ''){
            alert('marks not given please fill the form correctly')
            return false

        }
    }
    var numberOfCheckedRadio = $('input:radio:checked').length
    if(textEle.length !== numberOfCheckedRadio ){
        alert('You forgot to select correct answer. please remember to select one radio button in each section')
        return false

    }

    return true

}

function readData(){
    if (checkForm()){

        questions = []
        answerOption = []
        correctAnswer = []
        marks = []
        
        var textEle = document.querySelectorAll('textarea')
        var inputELe = document.querySelectorAll('input')
        
        for(i = 0; i < textEle.length;i++){
            questions.push(textEle[i].value)
        }

        for(i =0; i < inputELe.length; i++){
            if(inputELe[i].type === "radio" && inputELe[i].checked){
                var id = inputELe[i].id
                var correct = document.getElementById('ans'+id)
                correctAnswer.push(correct.value)
            }
            if(inputELe[i].type === 'text'){
                answerOption.push(inputELe[i].value)
            }
            if(inputELe[i].type === 'number'){
                marks.push(inputELe[i].value)
            }
        }


        console.log(questions)
        console.log(answerOption)
        console.log(correctAnswer)
        var id = JSON.parse(document.getElementById('id').textContent)

        $.ajax({
            type: "POST",
            url: "/quiz/create",
            data: { 
                "questions[]": questions,
                "correctans[]": correctAnswer,
                "answer[]": answerOption,
                "marks[]": marks,
                "module":document.getElementById('module').value
            },
            success: function (data) {
                if (data.status == "fail") {
                alert(data.msg);
                } else if (data.status == "success") {
                console.log('uo')
                console.log(typeof(data))
                console.log(data);
                window.location.href=`/quiz/detail/${id}`;
                }
            },
            });
    }
}