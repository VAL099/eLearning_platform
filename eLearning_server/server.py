from fastapi import FastAPI, Response, Header
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import models, db_handler, handlers
from hashlib import sha256
import os, redis

redis_tmp = redis.Redis(host='localhost', port=6379, db=0)

server = FastAPI()

origins = [
    "http://127.0.0.1:7890",
    "http://localhost:7890",
    "http://192.168.0.26:7890"
] 

server.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@server.get('/')
async def home():
    return RedirectResponse('/docs')

@server.post('/register_user')
async def register_user(user: models.User):
    data = user.username, user.password, user.name, user.email, user.user_type, user.user_interest
    check = db_handler.check_user_existency(data=(user.username, user.email))
    try:
        if check[0][3] == user.email:
            return JSONResponse(content={"message":"Email alredy registered!"}, status_code=409)
        elif check[0][1] == user.username:
            return JSONResponse(content={"message":"This username has been alredy taken!"}, status_code=409)
    except IndexError:
        db_handler.write2DB(action='register', data=data)
    return Response(status_code=201) 

@server.post('/login_user')
async def login(user: models.User):
    job = db_handler.login_handler(u=user.username, p=user.password)
    if job:
        return JSONResponse({'user_type':job[1], 'name':job[2]}, 200)
    else: 
        return Response(status_code=401)
    
@server.post('/password_recovery')
async def password_recovery(form: models.PRecovery):
    global security_code # this will be stored in REDIS
    if form.email:
        if db_handler.check_user(data=(form.email, )): # check if a user with such email exist
            security_code = handlers.send_code(receiver=form.email)
            return Response(status_code=200)
        return Response('No such email registered!!!', 401)
    elif form.code:
        if form.code == security_code:
            return Response(status_code=200)
    elif form.password:
        db_handler.write2DB(action='reset_password', data=(form.email, form.email))
        return Response(status_code=201)
    
@server.post('/add_course')
async def add_course(course: models.Course):
    data = course.name, course.description, course.requirements, course.course_domain, course.thumb, course.creator
    db_handler.write2DB(action='add_course', data=data)
    return Response(status_code=201)

@server.post('/add_course_topic')
async def add_topic(topic: models.Topic):
    data = topic.name, topic.content, topic.parent_course
    db_handler.write2DB(action='add_topic', data=data)
    return Response(status_code=201)

@server.post('/add_course_task')
async def add_topic(topic: models.Topic):
    data = topic.name, topic.content, topic.parent_course
    db_handler.write2DB(action='add_task', data=data)
    return Response(status_code=201)
    
@server.get('/all_courses')
async def get_courses4shop():
    data = db_handler.get_course_list_4_shop()
    return JSONResponse(status_code=200, content={'content':data})

@server.get('/courses')
async def get_courses4shop(domain):
    data = db_handler.get_courses_by_category(domain)
    return JSONResponse(status_code=200, content={'content':data})

@server.get('/course_details')
async def get_course_details(c_id): 
    data = db_handler.get_course_details(c_id)
    return JSONResponse(status_code=200, content={'content':data}) 

@server.get('/users_courses') 
async def get_users_courses(user, user_type):
    if user_type == 'teacher':
        data = db_handler.get_teachers_courses(user)
    elif user_type == 'student':
        data = db_handler.get_students_courses(user)
    return JSONResponse(status_code=200, content={'content':data}) 

@server.get('/course_topics')
async def get_all_topics(id):
    data = db_handler.get_all_topics(id)
    return JSONResponse(status_code=200, content={'content':data}) 

@server.get('/course_tasks')
async def get_all_tasks(id):
    data = db_handler.get_all_tasks(id)
    return JSONResponse(status_code=200, content={'content':data})

@server.get('/course_videos')
async def get_all_tasks(id):
    data = db_handler.get_all_videos(id)
    return JSONResponse(status_code=200, content={'content':data})

@server.get('/topic_content')
async def get_topic_content(topicId):
    data = db_handler.get_topic_content(topicId)
    return JSONResponse(status_code=200, content={'content':data}) 

@server.get('/topic_content')
async def get_topic_content(topicId):
    data = db_handler.get_video_content(topicId)
    return JSONResponse(status_code=200, content={'content':data}) 


@server.get('/task_content')
async def get_task_content(taskId):
    data = db_handler.get_task_content(taskId)
    return JSONResponse(status_code=200, content={'content':data}) 

@server.post('/save_task_answer')
async def save_task_answer(template: models.Submission):
    data = template.username, template.task, template.content
    try:
        db_handler.write2DB(action='save_answer', data=data)
    except:
        return Response(status_code=409)
    return Response(status_code=201)

@server.post('/create_video_topic')
async def save_video(topic: models.VideoTopic):
    data = topic.title, topic.content, topic.parent_course, topic.fn
    db_handler.write2DB(action='add_video_topic', data=data)
    # os.remove(f'vids/{topic.fn}')
    return Response(status_code=201)

@server.get('/video_content')
async def get_video(vidId):
    data = db_handler.get_video(vidId)
    return JSONResponse(status_code=200, content={'content':data}) 

@server.post('/buy_course')
async def buy_course(course, user):
    gate = db_handler.buy_course(course, user)
    if gate == True:
        return Response(status_code=201) 
    else: 
        return Response(status_code=400)

@server.get('/generate_reedem')
async def create_reedem(courseId, expire):
    code = handlers.generate_reedem_code()
    redis_tmp.set(code, courseId)
    redis_tmp.expire(code, int(expire)*3600) # hours to expire
    return JSONResponse(status_code=201, content={'code':code})
 
@server.post('/reedem_course')
async def reedem_course(code, user):
    course = redis_tmp.get(code)
    gate = db_handler.buy_course(course, user)
    if gate == True:
        return Response(status_code=201) 
    else: 
        return Response(status_code=400)

@server.delete('/remove')
async def remvoe_content(courseId:int = None, topicId:int = None, taskId:int = None, videoId:int = None):
    if courseId:
        db_handler.remove_course(courseId)   
    if topicId:
        db_handler.remove_topic(topicId)
    if taskId:
        db_handler.remove_task(taskId)
    if videoId:
        db_handler.remove_video(videoId)
    return Response(status_code=200)

@server.get('/recommended')
async def recommendations(user):
    courses = db_handler.get_recommends(user)
    return JSONResponse(status_code=200, content={"content":courses})

@server.get('/submitted_tasks')
async def course_Submited_tasks(course_id, user):
    data = db_handler.student_submitted_tasks(course_id, user)
    return JSONResponse(status_code=200, content={"content":data})

@server.get('/all_submitted_tasks')
async def course_all_Submited_tasks(course_id):
    data = db_handler.all_submitted_tasks(course_id)
    return JSONResponse(status_code=200, content={"content":data})

@server.get('/answer_content')
async def get_answer_content(taskId, user):
    data = db_handler.get_task_submissions(taskId, user)
    return JSONResponse(status_code=200, content={'content':data}) 

@server.post('/mark_task')
async def mark_task(taskId, userId, mark):
    db_handler.put_mark(taskId, userId, mark)
    return Response(status_code=200)