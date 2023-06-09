
function showInterestsMenu(){
    const selectOption = document.getElementById("userIdenitiy");
    const toDisplay = document.getElementById("userInterest");
    selectOption.addEventListener("change", function(){
        if (this.value === "student"){
            toDisplay.style.display = "inline";
        }
        if (this.value === "plain" || this.value === "teacher"){
            toDisplay.style.display = "none";
        }
    });
}

function changeLandingForms(){
    [loginForm, registerForm] = [document.querySelector('.landing_form:first-child'), document.querySelector('.landing_form:nth-child(2)')]
    document.getElementById('gotoRegister').addEventListener('click', function(){
        // registerForm.style.display = 'flex'
        registerForm.style.animation = 'introduceElement 1s forwards'
        loginForm.style.animation = 'withdrawElement 1s forwards'
        setTimeout(function(){
            registerForm.style.display = 'flex'
            loginForm.style.display = 'none';
        }, 350)
        setTimeout(function(){
            registerForm.style.animation = ''
            loginForm.style.animation = ''
        }, 1500)
    })

    document.getElementById('returnToLoginPage').addEventListener('click', function(){
        loginForm.style.animation = 'restoreElement 1s forwards'
        registerForm.style.animation = 'withdrawIntroduced 1s forwards'
        setTimeout(function(){
            loginForm.style.display = 'flex';
            registerForm.style.display = 'none';
        }, 350)
        setTimeout(function(){
            registerForm.style.animation = ''
            loginForm.style.animation = ''
        }, 1500)
    })
}

function showAccountOptions(){
    var container = document.getElementById('1234567890')
    if (container.style.display == 'flex'){ container.style.display = 'none'; }
    else{ container.style.display = 'flex'; }
}

// function writeOnMainPage(i) {
//     var txt = "To borrow a phrase from an old friend...";
//     var speed = 50;
//     if (i < txt.length) {
//         document.getElementById("motto").innerHTML += txt.charAt(i);
//         setTimeout(function() { writeOnMainPage(i + 1); }, speed);
//     }
// }

function quotesOnMainPage(){
    var quotes = 
    ['First you learn then you remove the "L"', 
    "Work smarter, not harder!",
    "Live as if you were to die tomorrow.",
    "Learning never exhausts the mind.",
    "Don't watch the clock; do what it does. Keep going.",
    "The best way to predict the future is to create it.",
    "Live as if you were to die tomorrow.",
    'First you learn then you remove the "L"' ]
    let i = 0;
    function disp(){
        if (i < quotes.length){
            document.getElementById("quottes").innerHTML = quotes[i]
            i++
        }
        else{ i = 0; }    
    }
    setInterval(function(){disp()}, 3000);
}

function displayUPLDfileName(){
    document.getElementById('upload_course_img').addEventListener('change', (event)=>{
        document.getElementById('upload_course_img_lbl').textContent = event.target.files[0].name
    })
}

function shopCourseDescription(){
    var cDescr = document.getElementById('course_preview')
    document.addEventListener("keydown", function(event){
        if (event.code === 27 || event.which === 27){
            cDescr.style.visibility = 'hidden'
        }
    })
}

function fullFillCourseDescription(cID){
    var courseDetails;
    $.ajax({
        url: `http://localhost:7654/course_details?c_id=${cID}`,
        method: 'GET',
        success: function(data) {
            courseDetails = data['content'][0];
            document.getElementById('course_preview').style.visibility = 'visible'
            document.getElementById("course_name").innerText = courseDetails[0]
            document.getElementById("course_thumb").src = `data:image/png;base64,${courseDetails[1]}`
            document.getElementById("course_description").innerText = courseDetails[2]
            // for (req of courseDetails[3].split(',')){
            //     document.getElementById("course_requirements").innerHTML += `<li>${req}</li>`
            // }
            document.getElementById("course_requirements").innerHTML = courseDetails[3]
            document.getElementById("buy_btn").setAttribute('action', `/buy_course_${cID}`)
        },
        error: function(xhr, status, error) {
            console.log('Error:', error);
        }
    });
}

function highlightActiveCourse(){
    const buttons = document.getElementsByClassName("course_page_btn");
    for (let i = 0; i < buttons.length; i++) {
        buttons[i].addEventListener("click", function() {

            for (let i = 0; i < buttons.length; i++) {
                var button = buttons[i];
                if (button.classList.contains("highlighted_topic_btn")) {
                    button.classList.remove("highlighted_topic_btn");
                }
            }

            if (this.id != "tech_btn" || this.id != "tech_btn_student"){
                this.classList.add("highlighted_topic_btn");
            }
        });
    }
}

function showAddItem2CourseMenu(){
    const target = document.getElementById("tech_btn")
    const toMod = document.getElementById("add_menu")
    if (target){
        target.addEventListener("click", function(){
            toMod.style.visibility = "visible";
            toMod.style.opacity = "1";
            document.getElementById("course_pg_menu").style.opacity = 0.1
            document.getElementById("course_pg_content").style.opacity = 0.1
        })
        document.addEventListener("keydown", function(event){
            if (event.code === 27 || event.which === 27){ // deprecated but still needed!
                toMod.style.visibility = "hidden";
                toMod.style.opacity = "0";
                document.getElementById("course_pg_menu").style.opacity = '1'
                document.getElementById("course_pg_content").style.opacity = '1'
            }
        })
    }
}

function handleContentTypes() {
    const targets = [
      document.getElementById("_op_course_topic"),
      document.getElementById("_op_test"),
      document.getElementById("_op_video")
    ];
    const testFormDiv = document.getElementById("test_form_section");
    const addTopicDiv = document.getElementById('new_topic_form');
    const addVideoDiv = document.getElementById("video_topic");
    
    targets.forEach(function(target) {
      target.addEventListener('change', function() {
        if (this.checked) {
          targets.forEach(function(other) {
            if (other !== target) {
              other.checked = false;
            }
          });

          if (this.id === "_op_test") {
            testFormDiv.classList.remove('hidden_element');
            addTopicDiv.classList.add('hidden_element');
            addVideoDiv.classList.add('hidden_element');
          } else if (this.id === '_op_course_topic') {
            addTopicDiv.classList.remove('hidden_element');
            testFormDiv.classList.add('hidden_element');
            addVideoDiv.classList.add('hidden_element');
          } else if (this.id === '_op_video') {
            addVideoDiv.classList.remove('hidden_element');
            testFormDiv.classList.add('hidden_element');
            addTopicDiv.classList.add('hidden_element');
          }
        }
      });
    });
}

function addOnElement(localization_pack){
    const btns = [document.getElementById('add_quizz_question'), 
    document.getElementById('input_question'), 
    document.getElementById('add_upload_field'),
    document.getElementById('add_subtopic')
    // document.getElementById('add_variant')
    ]
    const qTarget = document.getElementById('questions_section')
    const tTarget = document.getElementById('topics_section')

    const btnGO = document.getElementById('creation_menu_btn_go')
    const btnGO1 = document.getElementById('creation_menu_btn_go1')

    var multiChoiceQuestion = 0, question = 0, question_answer = 0, individual_task_question = 0, subtopic = 0
    btns.forEach(function(btn){
        btn.addEventListener('click', function(){
            if(this.id === 'add_quizz_question'){
                if (multiChoiceQuestion > 29){
                    alert('Question limit achieved!')
                }
                else{
                    const newElement = document.createElement('div')
                    newElement.classList.add('test_element', 'flex_row', 'flex_centered')
                    newElement.innerHTML= `
                    <input type="text" name="multi_question_${multiChoiceQuestion}" placeholder="${ localization_pack['subtopic_question'] }" required>
                    <button id="add_variant" type="button" onclick="addVars(${multiChoiceQuestion})">+ ${ localization_pack['subtopic_multichoice_option'] } +</button>
                    <div class="flex_col flex_centered" style="gap: 0.5rem;" id="question_answer_vars">
                        <div class="flex_row flex_centered">
                            <input type="text" name="option_${multiChoiceQuestion}_0" placeholder="${ localization_pack['suptopic_multichoice_answer'] }" required>
                            <input type="checkbox" name="checkbox_${multiChoiceQuestion}_0">
                        </div>
                    </div>
                    `
                    qTarget.appendChild(newElement); multiChoiceQuestion++
                    btnGO.disabled = false; btnGO.classList.remove('disBtn')
                }
            }
            if (this.id === 'input_question'){
                if (question > 19){
                    alert('Question limit achieved!')
                }
                else{
                    const newElement = document.createElement('div')
                    newElement.classList.add('test_element', 'flex_row', 'flex_centered')
                    newElement.innerHTML= `
                    <input type="text" name="question_${question}" placeholder="${ localization_pack['subtopic_question'] }" required>
                    <input type="text" name="answer_${question_answer}" placeholder="${ localization_pack['subtopic_answer'] }">
                    `
                    qTarget.appendChild(newElement); question++; question_answer++;
                    btnGO.disabled = false; btnGO.classList.remove('disBtn');
                }
            }
            if (this.id === 'add_upload_field'){
                if (individual_task_question > 2){
                    alert('Task limit achieved!')
                }
                else{
                    const newElement = document.createElement('div')
                    newElement.classList.add('test_element', 'flex_row', 'flex_centered')
                    newElement.innerHTML= `
                    <input type="text" name="individual_task_${individual_task_question}" placeholder="${ localization_pack['subtopic_task'] }" required>
                    `
                    qTarget.appendChild(newElement); individual_task_question++
                    btnGO.disabled = false; btnGO.classList.remove('disBtn');
                }
            }
            if (this.id === 'add_subtopic'){
                const newElement = document.createElement('div')
                newElement.classList.add('topic_details', 'flex_col', 'flex_centered')
                newElement.innerHTML = `
                <input type="text" name="subtopic_${subtopic}" placeholder="${ localization_pack['subtopic_title'] }" required>
                <label for="subtopicIMG_${subtopic}" id="imgADDLbl_${subtopic}"><i class="fa fa-cloud-upload" aria-hidden="true"></i>   ${ localization_pack['upload_image'] }</label>
                <input type="file" name="subtopic_image_${subtopic}" id="subtopicIMG_${subtopic}" class="hidden_element" onchange="document.getElementById('imgADDLbl_${subtopic}').textContent = event.target.files[0].name">
                <textarea name="subtopic_content_${subtopic}" placeholder="${ localization_pack['subtopic_content'] }" maxlength="2500" required></textarea>
                `
                tTarget.appendChild(newElement); subtopic++
                btnGO1.disabled = false; btnGO1.classList.remove('disBtn');
            }
        })
    })
}

function loadTopicContent(topicID, user_type){
    var content;
    document.getElementById('subTopicContent').innerHTML = ''
    $.ajax({
        url: `http://localhost:7654/topic_content?topicId=${topicID}`,
        method: 'GET',
        success: function(data) {
            content = data['content'][0][0];
            content = JSON.parse(content)
            for (var element in content){
                var newElement = document.createElement('div')  
                if (typeof(content[element]) === 'object'){
                    newElement.innerHTML = `
                    <span class="subtopic_title">
                        ${element} 
                        ${user_type === "teacher" ? `
                            <i title="Edit this!" id="edit_this" class="fa" onclick="edit_subtopic(this.parentNode.parentNode)">&#xf044</i> 
                        ` : ''}
                    </span>
                    <hr>
                    <div class="flex_row" style="gap:2rem">
                        <span class="subtopic_content">${content[element][0]}</span>
                        <img class="topic_inner_img" src="data:image/png;base64, ${content[element][1]}">
                    </div>
                `
                } 
                else{
                    newElement.innerHTML = `
                    <span class="subtopic_title">
                        ${element} 
                        ${user_type === "teacher" ? `
                            <i title="Edit this!" class="fa" onclick="edit_subtopic(this.parentNode.parentNode)">&#xf044</i> 
                        ` : ''}
                    </span> 
                    <hr>
                    <span class="subtopic_content">${content[element]}</span>
                `
                }
                document.getElementById('subTopicContent').appendChild(newElement)
            }
            if (user_type === "teacher"){
                document.getElementById('subTopicContent').innerHTML += `<button class="deleteBtn" onclick="rmTopicContent(${topicID}, 'topic')">
                <i class="fa fa-trash"></i></button>`
            }
        },
        error: function(xhr, status, error) {
            console.log('Error:', error);
        }
    });
}

function loadVideoContent(vidID, user_type){
    document.getElementById('subTopicContent').innerHTML = ''
    var content;
    target = document.getElementById('subTopicContent')
    $.ajax({
        url: `http://localhost:7654/video_content?vidId=${vidID}`,
        method: 'GET',
        success: function(data) {
            content = data['content'][0]
            var newElement = document.createElement('div')
            newElement.classList.add('flex_col')
            newElement.innerHTML = `
            <video src="${content[1]}" type="video/mp4" controls>Coudn't load video =(</video>
            <hr>
            <span class="subtopic_content">${content[0]}</span>
            `
            target.appendChild(newElement)
            if (user_type === "teacher"){
                target.innerHTML += `<button class="deleteBtn" onclick="rmTopicContent(${vidID}, 'video')">
                <i class="fa fa-trash"></i></button>`
            }
        },
        error: function(xhr, status, error) {
            console.log('Error:', error);
        }
    });
}

function loadTaskContent(taskID, user_type){
    var content;
    document.getElementById('subTopicContent').innerHTML = ''
    var target_container = document.getElementById('subTopicContent')
    var created_form = document.createElement('form')
    created_form.classList.add('test_form')
    created_form.setAttribute('action', `/submit_task_solution_${taskID}`)
    created_form.setAttribute('method', 'POST')
    created_form.setAttribute("enctype", "multipart/form-data")
    $.ajax({
        url: `http://localhost:7654/task_content?taskId=${taskID}`,
        method: 'GET',
        success: function(data) {
            content = data['content'][0][0];
            content = JSON.parse(content)
            var question = 0; 
            for (var element in content){
                var variant = 0;
                if ( Array.isArray(content[element]) ){
                    var newElement = document.createElement('div')
                    newElement.classList.add('multichoice')
                    newElement.innerHTML += `
                    <span class="subtopic_title" >${element}</span>
                    <input type="hidden" name="question_${question}" value="${element}">
                    <hr>
                    `
                        for (var item in content[element]) {
                            newElement.innerHTML += `
                            <label> 
                                <input type="hidden" name="variant_${question}_${variant}"" value="${content[element][item].replace("_____isCorrect", "")}">
                                <input type="checkbox" name="check_${question}_${variant}">
                                ${content[element][item].replace("_____isCorrect", "")}
                            </label> 
                            `
                            variant++;
                        }
                    created_form.appendChild(newElement)
                }
                else if (content[element] === "Submission required"){
                    var newElement = document.createElement('div')
                    newElement.classList.add('upload_question')
                    newElement.innerHTML += `
                        <span class="subtopic_title">Individual task</span>
                        <hr>
                        <p class="subtopic_content"><b>Your task is:</b> ${element}</p> <br>
                        <input type="hidden" name="question_${question}" value="${element}">
                        <input type="file" name="file_${question}" id="taskSubmission_${question}">
                        <label for="taskSubmission_${question}" "><i class="fa fa-cloud-upload" aria-hidden="true"></i>   Upload your file here!</label>
                    `
                    created_form.appendChild(newElement)
                }
                else{
                    var newElement = document.createElement('div')
                    newElement.classList.add('simple_question')
                    newElement.innerHTML += `
                    <span class="subtopic_title">${element}</span>
                    <input type="hidden" name="question_${question}" value="${element}">
                    <hr>
                    <textarea placeholder="type answer here!" name="answer_${question}"></textarea>
                    `
                    created_form.appendChild(newElement)
                }
                question++
            }
            submitBtn = document.createElement('input')
            submitBtn.setAttribute('type', 'submit')
            submitBtn.classList.add('testSubmitBtn')
            submitBtn.setAttribute('value', 'GO!')
            created_form.appendChild(submitBtn)
            target_container.appendChild(created_form) 
            if (user_type === "teacher"){
                target_container.innerHTML += `<button class="deleteBtn" onclick="rmTopicContent(${taskID}, 'task')">
                <i class="fa fa-trash"></i></button>`
            }
        },
        error: function(xhr, status, error) {
            console.log('Error:', error);
        }
    });
}

function showTestSubmits(user_type, courseId, user){
    var content;
    var target_container = document.getElementById('subTopicContent')
    target_container.innerHTML = ''
    if (user_type === "student"){
        $.ajax({
            url: `http://localhost:7654/submitted_tasks?course_id=${courseId}&user=${user}`,
            method: 'GET',
            success: function(data) {
                content = data['content'];
                target_container.innerHTML += `
                <table>
                    <tr>
                        <th>Task name</th>
                        <th>View answer</th>
                        <th>View my result</th>
                        <th>Final result</th>
                    </tr>
                `
                for (row of content){
                    target_container.querySelector('table').innerHTML += `
                    <tr>
                        <td>${row[0]}</td>
                        <td> <a href="/show_task_content_${row[1]}" target="_blank"><button>Open</button></a> </td>
                        <td> <a href="/show_answer_content_${row[1]}_${user}" target="_blank"><button>Open</button></a> </td>
                        <td>${row[2]}</td>
                    </tr>
                    `
                target_container.innerHTML += "</table>"
                }
            }
        })
    }
    if (user_type === "teacher"){
        $.ajax({
            url: `http://localhost:7654/all_submitted_tasks?course_id=${courseId}`,
            method: 'GET',
            success: function(data) {
                content = data['content'];
                target_container.innerHTML += `
                <table>
                    <tr>
                        <th>Task name</th>
                        <th>Student</th>
                        <th>View student's answer</th>
                        <th>View defined answer</th>
                        <th>Mark</th>
                    </tr>
                `
                for (row of content){
                    target_container.querySelector('table').innerHTML += `
                    <tr>
                        <td>${row[1]}</td>
                        <td>${row[0]}</td>
                        <td> <a href="/show_answer_content_${row[2]}_${row[0]}" target="_blank"><button>Open</button></a> </td>
                        <td> <a href="/show_task_content_${row[2]}" target="_blank"><button>Open</button></a> </td>
                        <td>
                            ${row[4] === null ? `
                                <input type="text" name="test_mark" placeholder="Mark this" id="mark_${row[2]}"> 
                                <input type="submit" value="Mark!" onclick="putAmark(${row[3]}, ${row[2]}, document.getElementById('mark_${row[2]}').value );"> 
                            ` : row[4]}
                        </td>
                    </tr>
                    `
                target_container.innerHTML += "</table>"
                }
            }
        })
    }
}

function putAmark(taskId, userId, mark){
    fetch(`http://localhost:7654/mark_task?taskId=${taskId}&userId=${userId}&mark=${mark}`, { method: 'POST' })
    location.reload()
}

async function rmTopicContent(elementId, contentType){
    if (contentType == "topic"){
        await fetch(`http://localhost:7654/remove?topicId=${elementId}`, { method: 'DELETE' })
        location.reload()
    }
    if (contentType == "task"){
        await fetch(`http://localhost:7654/remove?taskId=${elementId}`, { method: 'DELETE' })
        location.reload()
    }
    if (contentType == "course"){
        await fetch(`http://localhost:7654/remove?courseId=${elementId}`, { method: 'DELETE' })
        location.reload()
    }
    if (contentType == "video"){
        await fetch(`http://localhost:7654/remove?videoId=${elementId}`, { method: 'DELETE' })
        location.reload()
    }
}

function activate_course_inv(username){
    console.log(username)
    targetDIV = document.getElementById('inv_cr')
    targetDIV.style.display = 'flex'
    targetDIV.innerHTML += 
    `<a style="cursor:pointer; text-decoration: underline; font-weight:bolder;" 
    onclick="document.getElementById('inv_cr').style.display = 'none'">Close</a>`
    
    document.getElementById('activate_btn').addEventListener('click', function(){
        var invCode = document.getElementById('uInv_code').value
        $.ajax({
            url: `http://localhost:7654/reedem_course?code=${invCode}&user=${username}`,
            method: 'POST',
            success: function(data) {
                console.log(data.status)
                window.location.href = `/user_${username}_courses`;
            },
            error: function(xhr, status, error) {
                console.log('Error:', error);
            }
        }); 
    })
}

function shop_filter(){
    var container = document.getElementById('shop')
    document.getElementById('c_domains').addEventListener('change', function(){
        var domain = this.value
        if (domain == 'all'){
            container.innerHTML = ''
            $.ajax({
                url: `http://localhost:7654/all_courses`,
                method: 'GET',
                success: function(data) {
                    for (item in data['content']){
                        var payload = data['content'][item]
                        container.innerHTML += `
                        <div class="shop_item" onclick="fullFillCourseDescription(${payload[0]})">
                            <img src="data:image/png;base64,${payload[2]}">
                            <p>${payload[1]}</p>
                        </div>
                        `} } }); }
        else{
            container.innerHTML = ''
            $.ajax({
                url: `http://localhost:7654/courses?domain=${domain}`,
                method: 'GET',
                success: function(data) {
                    for (item in data['content']){
                        var payload = data['content'][item]
                        container.innerHTML += `
                        <div class="shop_item" onclick="fullFillCourseDescription(${payload[0]})">
                            <img src="data:image/png;base64,${payload[2]}">
                            <p>${payload[1]}</p>
                        </div>
                        ` } } });  } })
}

function registerPasswordCheck(){
    [regForm, p1, p2, alertField] = [ document.getElementById('regForm'), document.getElementsByName('pswd')[1], 
                                document.getElementsByName('re_pswd')[0], document.getElementsByClassName('errMsg')[1] ]
    console.log(regForm, p1, p2, alertField)
    regForm.addEventListener('submit', (event)=>{
        if (p1.value !== p2.value){
            event.preventDefault();
            alertField.innerText = "Passwords doesn\'t match!"
            p1.style.border = '2.5px solid #ff2800'; p2.style.border = '2.5px solid #ff2800'
        }
        if (p1.value.length < 8) {
            event.preventDefault();
            alertField.innerText = "Password length should have at least 8 characters"
            p1.style.border = '2.5px solid #ff2800';
        }
    })
}

function hideLoader(){
    var loader = document.getElementById('loading_animation')
    loader.style.display = 'none'
    window.addEventListener('beforeunload', function(){ loader.style.display = 'flex'; });
}
