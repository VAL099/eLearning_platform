from flask import Flask, render_template, redirect, url_for, flash, make_response, abort, request, session
from hashlib import sha256
import requests, json, base64, handlers
import mimetypes

client = Flask(__name__)
client.secret_key = 'v3ry_v3r1_s3cr3t_k3y'

@client.context_processor
def localize():
    if 'language_pack' not in session:
        if request.cookies.get('language') == None:
            with open('./static/res/localization/en/pack.json', 'r', encoding='utf-8') as lang_pack:
                session['language_pack'] = json.load(lang_pack)
        else:
            with open(f'./static/res/localization/{request.cookies.get("language")}/pack.json', 'r', encoding='utf-8') as lang_pack:
                session['language_pack'] = json.load(lang_pack)
    return dict(localization=session['language_pack'])

@client.route('/')
def initialising():
    if 'user' in session:
        if session['user_type'] == "student":
            cList = requests.get(f'http://localhost:7654/recommended?user={session["user"]}')
            return render_template('index.html', user_name=session['name'], uType=session['user_type'], uname=session['user'], recommended = json.loads(cList.content)['content'] )
        return render_template('index.html', user_name=session['name'], uType=session['user_type'], uname=session['user'] )
    else:
        return redirect('/landing')

@client.route('/select_language')
def lang_menu():
    return render_template('language_selection.html')

@client.route('/set_lang', methods = ['POST'])
def set_lang():
    if request.method == 'POST':
        lang = request.form.get('language')
        with open(f'./static/res/localization/{lang}/pack.json', 'r', encoding='utf-8') as lang_pack:
            session['language_pack'] = json.load(lang_pack)
            resp = make_response( redirect('/') )
            resp.set_cookie('language', lang, 185*24*3600)
    return resp

@client.route('/landing')
def landing():
    message = request.args.get('message')
    if message:
        return render_template('landing.html', message=message)
    return render_template('landing.html')

@client.route('/logout', methods = ['GET', 'POST'])
def logout():
    session.clear()
    return redirect('/')

@client.route('/login', methods = ['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['pswd']
        rData = {"username": username, "password": sha256(password.encode()).hexdigest()}
        gate = requests.post(url='http://localhost:7654/login_user', json=rData)
        if gate.status_code == 200:
            session['user'] = username
            session['user_type'] = json.loads(gate.content.decode())['user_type']
            session['name'] = json.loads(gate.content.decode())['name']
            return redirect('/')
        elif gate.status_code == 401:
            return redirect( url_for('landing', message='Wrong Credentials!!!') )
    return redirect('/')

@client.route('/register', methods = ['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        username = request.form['uname']
        name = request.form['name']
        email_addr = request.form['email']
        password = request.form['pswd']
        user_type = request.form['identity']
        user_interest = request.form['interest']
        rData = { "username": username, "password": sha256(password.encode()).hexdigest(), "name": name, "email": email_addr, "user_type": user_type, "user_interest":user_interest }
        gate = requests.post(url='http://localhost:7654/register_user', json=rData)
        if gate.status_code == 201:
            session['user'] = username
            session['name'] = name
            session['user_type'] = user_type
            return redirect('/')
        elif gate.status_code == 409:
            return redirect( url_for('landing', message=json.loads(gate.content.decode())['message']) )
    return redirect('/')

@client.route('/add_course', methods = ['GET', 'POST'])
def add_course():
    if 'user' in session:
        if request.method == 'POST':
            title = request.form['course_name']
            description = request.form['course_description']
            requirements = request.form['course_requirements']
            domain = request.form['course_domain']
            thumb = request.files['course_thumbnail'].read()
            rData = { "name":title, "description":description, "requirements":requirements, "course_domain":domain, "creator":session['user'], "thumb":base64.b64encode(thumb).decode('utf-8') }
            gate = requests.post(url='http://localhost:7654/add_course', json=rData)
            if gate.status_code == 201:
                return redirect(url_for('users_course_list', user=session['user']))
        return render_template('add_course.html', user_name=session['name'], uType=session['user_type'], uname=session['user'])
    else:
        return redirect('/')

@client.route('/shop')
def shop():
    if 'user' in session:
        if request.method == 'GET':
            data = requests.get(url='http://localhost:7654/all_courses')
            if data.status_code == 200:
                temp = json.loads(data.content)
        return render_template('shop.html', user_name=session['name'], content=temp['content'], uType=session['user_type'], uname=session['user'])
    else:
        return redirect('/')
    
@client.route('/buy_course_<cId>', methods = ['POST'])
def buy_course(cId):
    if request.method == 'POST':
        gate = requests.post(url=f'http://localhost:7654/buy_course?course={cId}&user={session["user"]}')
        if gate.status_code == 201:
            return redirect(f'/course_{cId}')
        else: return redirect('/shop')
    return redirect('/shop')

@client.route(f'/user_<user>_courses')
def users_course_list(user):
    if 'user' in session and user == session['user']:
        data = requests.get(url=f'http://localhost:7654/users_courses?user={user}&user_type={session["user_type"]}')
        if data.status_code == 200:
            temp = json.loads(data.content)
        return render_template('user_courses.html', user_name=session['name'], uType=session['user_type'], uname=session['user'], data=temp['content'])
    return redirect('/')

@client.route(f'/course_<id>')
def show_course(id):
    if 'user' in session:
        topics = requests.get(url=f'http://localhost:7654/course_topics?id={id}')
        tasks = requests.get(url=f'http://localhost:7654/course_tasks?id={id}')
        vids = requests.get(url=f'http://localhost:7654/course_videos?id={id}')
        if topics.status_code == 200 and tasks.status_code == 200:
            payload_theory = json.loads(topics.content)
            payload_tasks = json.loads(tasks.content)
            payload_vids = json.loads(vids.content)
        return render_template('course_page.html', uname=session['user'], uType=session['user_type'], 
                           course_name = 'Top course', cId = id, 
                           theory=payload_theory['content'], tasks=payload_tasks['content'], vids=payload_vids['content'])
    else:
        return redirect('/')

@client.route('/add_topic_<cId>', methods=['POST'])
def create_topic(cId):
    topic_filling = {}
    if request.method == 'POST':
        topic_name = request.form['topic_name']
        for subtopic in range(25):
            try:
                name = request.form[f'subtopic_{subtopic}']
                content = request.form[f'subtopic_content_{subtopic}']
                img = request.files[f'subtopic_image_{subtopic}'].read()
                if img: 
                    topic_filling.setdefault(name, [content, base64.b64encode(img).decode('utf-8')] )
                else: 
                    topic_filling.setdefault(name,content)
            except KeyError: pass
        rData = {"name":topic_name, "content":json.dumps(topic_filling), "parent_course":cId}
        gate = requests.post('http://localhost:7654/add_course_topic', json=rData)
        if gate.status_code == 201:
            return redirect(f'/course_{cId}')
    return redirect(f'/course_{cId}?=BAD HAPPEND!')

@client.route('/add_task_<cId>', methods = ['POST'])
def create_task(cId):
    questions = {}
    if request.method == 'POST':
        task_name = request.form['task_name']
        for multi_choice_question in range(30):
            try:
                q = request.form[f'multi_question_{multi_choice_question}']
                questions.setdefault(q, [])
                for choice_variant in range(10):
                    try:
                        v = request.form[ f'option_{multi_choice_question}_{choice_variant}' ]
                        status = request.form.get(f'checkbox_{multi_choice_question}_{choice_variant}')
                        if status == 'on': 
                            v += '_____isCorrect'
                            questions[q].append(v)
                        else: 
                            questions[q].append(v)
                    except KeyError: continue
            except KeyError: pass
        
        for simple_question in range(20):
            try:
                q = request.form[f'question_{simple_question}']
                a = request.form[f'answer_{simple_question}']
                questions.setdefault(q, a)
            except KeyError: pass

        for ind_task in range(3):
            try:
                q = request.form[f'individual_task_{ind_task}']
                questions.setdefault(q, 'Submission required')
            except KeyError: pass
        rData = {"name":task_name, "content": json.dumps(questions), "parent_course":cId}
        gate = requests.post('http://localhost:7654/add_course_task', json=rData)
        if gate.status_code == 201:
            return redirect(f'/course_{cId}')
    return redirect(f'/course_{cId}?=BAD HAPPEND!')

@client.route('/submit_task_solution_<taskId>', methods = ['POST'])
def save_task_answer(taskId):
    submission = {}
    if request.method == 'POST':
        tempList = request.form.keys()
        question_list = [x for x in tempList if x.startswith('question')] 
        for question in question_list:
            ord_n = question_list.index(question)
            if request.form.get(f'answer_{ord_n}'):
                submission.setdefault(request.form[question], request.form[f'answer_{ord_n}'])
            elif request.files.get(f'file_{ord_n}'):
                file = request.files[f'file_{ord_n}'].read()
                file_type = mimetypes.guess_type(request.files[f'file_{ord_n}'].filename)
                fn = "task_submits/" + session['user'] + '_task_' + taskId
                handlers.upload_task_submit_to_s3(file, "elearning-licence2023", fn, file_type[0])
                submission.setdefault( "file_task__"+request.form[question], f"https://elearning-licence2023.s3.amazonaws.com/{fn}" )
            elif request.form.get(f'variant_{ord_n}_0'):
                question = request.form[question]
                submission.setdefault(question, [])
                try:
                    for variant in range(10):
                        v = request.form.get(f'variant_{ord_n}_{variant}')
                        status = request.form.get(f'check_{ord_n}_{variant}')
                        if status == 'on': 
                            v += '_____checked'
                            submission[question].append(v)
                except KeyError: continue
        rData = {"task": taskId, "username":session['user'], "content":json.dumps(submission)}
        gate = requests.post('http://localhost:7654/save_task_answer', json=rData)
        if gate.status_code == 201:
            flash("Result saved. Thank you!")
            previous_url = request.referrer
            return redirect(previous_url)
        elif gate.status_code == 409:
            flash("You have already completed this test!")
            previous_url = request.referrer
            return redirect(previous_url)
    previous_url = request.referrer
    return redirect(previous_url)

@client.route('/add_video_<cId>', methods = ["POST"])
def upload_video_topic(cId):
    if request.method == "POST":
        title = request.form['topic_name']
        video_payload = request.files['topic_video'].read()
        video_fn = request.files['topic_video'].filename
        description = request.form['video_descr']
        rData = {"title":title, "fn": "https://elearning-licence2023.s3.amazonaws.com/"+video_fn, "content":description, "parent_course":cId}
        handlers.upload_video_to_s3(video_payload, "elearning-licence2023", video_fn)
        gate = requests.post('http://localhost:7654/create_video_topic', json=rData)
        if gate.status_code == 201:
            return redirect(f'/course_{cId}')
    return redirect(f'/course_{cId}')

@client.route('/show_task_content_<taskId>', methods = ["GET"])
def show_task_content(taskId):
    data = requests.get(f'http://localhost:7654/task_content?taskId={taskId}')
    data = json.loads(data.content)['content']
    data = json.loads(data[0][0])
    # make multichoice look great!
    for key in data:
        value = data[key]
        if isinstance(value, list):
            data[key] = []
            for _ in value:
                if _.endswith('_____isCorrect'):
                    data[key].append(_.replace('_____isCorrect', ''))
    return render_template('[technical]task_content.html', data=data, title=f"Task {taskId} answers")

@client.route('/show_answer_content_<taskId>_<user>', methods = ["GET"])
def show_snwer_content(taskId, user):
    data = requests.get(f'http://localhost:7654/answer_content?taskId={taskId}&user={user}')
    data = json.loads(data.content)['content']
    data = json.loads(data[0][0])
    # make multichoice look great!
    for key in data:
        value = data[key]
        if isinstance(value, list):
            data[key] = []
            for _ in value:
                data[key].append(_.replace('_____checked', ''))
    return render_template('[technical]task_content.html', data=data, title=f"{user}'s answers")

if __name__ == '__main__':
    client.run(port=7890, debug=True)