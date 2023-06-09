import mysql.connector as mysql
from hashlib import sha256
import boto3

# docker run --name eLearningDB -p 7700:3306 -e MYSQL_ROOT_PASSWORD=very_str0ng_pa55w0rd -d mysql

db = mysql.connect(host='localhost', port=7700, user='root', password='very_str0ng_pa55w0rd', database='eLearning')
cursor = db.cursor()

def write2DB(**kwargs):
    """
        this function takes as arguments action:str and data:tuple
        then initiates writing process
    """

    if kwargs.get('action') == 'register':
        query = "INSERT INTO users (username, password, name, email, user_type, user_init_interest) values (%s, %s, %s, %s, %s, %s)"
        values = kwargs.get('data')
        cursor.execute(query, values); db.commit()
        return 'User registered!'
    if kwargs.get('action') == 'reset_password':
        query = "UPDATE users SET password = %s WHERE email = %s"
        values = kwargs.get('data')
        cursor.execute(query, values); db.commit()
        return 'Password UPDATED!'
    elif kwargs.get('action') == 'add_course':
        query = "INSERT INTO courses (title, description, requirements, domain, thumbnail, creator) values (%s, %s, %s, %s, %s, %s)"
        values = kwargs.get('data')
        cursor.execute(query, values); db.commit()
        return 'Course created!'
    elif kwargs.get('action') == 'add_topic':
        query = "INSERT INTO course_topics (title, content, course) values (%s, %s, %s)"
        values = kwargs.get('data')
        cursor.execute(query, values); db.commit()
        return 'Topic added!'
    elif kwargs.get('action') == 'add_task':
        query = "INSERT INTO course_tasks (title, content, course) values (%s, %s, %s)"
        values = kwargs.get('data')
        cursor.execute(query, values); db.commit()
        return 'Task added!'
    elif kwargs.get('action') == 'save_answer':
        query = "INSERT INTO tasks_submissions (student_id, task_id, content) values ((SELECT id FROM users WHERE username = %s), %s, %s)"
        values = kwargs.get('data')
        cursor.execute(query, values); 
        db.commit()
        return 'Answer saved!'
    elif kwargs.get('action') == 'add_video_topic':
        query = "INSERT INTO course_videos (title, content, course, video_location) values (%s, %s, %s, %s)"
        values = kwargs.get('data')
        cursor.execute(query, values); 
        db.commit()
        return 'Video saved!'
        
def login_handler(**kwargs):
    query = "SELECT password, user_type, name FROM users WHERE username = %s"
    query_data = (kwargs.get('u'), )
    cursor.execute(query, query_data)
    control_data = cursor.fetchall()
    if control_data:
        if control_data[0][0] == kwargs.get('p'):
            return True, control_data[0][1], control_data[0][2]
        else: 
            return False
    else:
        return None
    
def check_user(**kwargs):
    query = "SELECT username FROM users WHERE email = %s"
    query_data = kwargs.get('data')
    cursor.execute(query, query_data)
    return cursor.fetchall()

def check_user_existency(**kwargs):
    query = "SELECT * FROM users WHERE username = %s OR email = %s"
    query_data = kwargs.get('data')
    cursor.execute(query, query_data)
    return cursor.fetchall()

def get_course_list_4_shop():
    query = "SELECT id, title, thumbnail FROM courses"
    cursor.execute(query)
    return cursor.fetchall()

def get_course_details(c_id):
    query = f"SELECT title, thumbnail, description, requirements FROM courses WHERE id = {c_id}"
    cursor.execute(query)
    return cursor.fetchall()

def get_teachers_courses(user):
    query = "SELECT id, title, thumbnail FROM courses WHERE creator = %s"
    cursor.execute(query, (user,))
    return cursor.fetchall()

def get_students_courses(user):
    query = "SELECT id, title, thumbnail FROM courses WHERE id IN (SELECT course_id from student2courses WHERE student_id = (SELECT id FROM users WHERE username = %s))"
    cursor.execute(query, (user,))
    return cursor.fetchall()

def get_all_topics(id):
    query = f"SELECT id, title FROM course_topics WHERE course = {id}"
    cursor.execute(query)
    return cursor.fetchall()

def get_all_tasks(id):
    query = f"SELECT id, title FROM course_tasks WHERE course = {id}"
    cursor.execute(query)
    return cursor.fetchall()

def get_all_videos(id):
    query = f"SELECT id, title FROM course_videos WHERE course = {id}"
    cursor.execute(query)
    return cursor.fetchall()

def get_topic_content(id):
    query = f"SELECT content FROM course_topics WHERE id = {id}"
    cursor.execute(query)
    return cursor.fetchall()

def get_video_content(id):
    query = f"SELECT content FROM course_topics WHERE id = {id}"
    cursor.execute(query)
    return cursor.fetchall()

# def get_task_content(id):
#     query = f"SELECT content, video_location FROM course_videos WHERE id = {id}"
#     cursor.execute(query)
#     return cursor.fetchall()

def buy_course(course, user):
    query = "INSERT INTO student2courses (student_id, course_id) VALUES ((SELECT id FROM users WHERE username = %s ), %s)"
    cursor.execute(query, (user, course)); db.commit()
    return True

def get_task_content(taskID):
    query = f"SELECT content FROM course_tasks WHERE id = {taskID}"
    cursor.execute(query)
    return cursor.fetchall()

def get_task_submissions(taskID, user):
    query = "SELECT content FROM tasks_submissions WHERE task_id = %s AND student_id = (SELECT id FROM users WHERE username = %s)"
    cursor.execute(query, (taskID, user))
    return cursor.fetchall()

def get_video(vidId):
    query = f"SELECT content, video_location FROM course_videos WHERE id = {vidId}"
    cursor.execute(query)
    return cursor.fetchall()

def get_courses_by_category(category):
    query = "SELECT id, title, thumbnail FROM courses WHERE domain = %s"
    cursor.execute(query, (category,))
    return cursor.fetchall()

def rm_video_from_s3(video_name): 
    s3 = boto3.client('s3', aws_access_key_id='AKIAUTQSVRDQNROXLQ53', 
                        aws_secret_access_key='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') 
    s3.delete_object(Bucket='elearning-licence2023', Key=video_name) 

def remove_course(cId):
    query = "DELETE FROM course_tasks WHERE course = %s"; cursor.execute(query, (cId, )); db.commit() # rm all course_tasks
    query = "DELETE FROM course_topics WHERE course = %s"; cursor.execute(query, (cId, )); db.commit() # rm all course_topics
    cursor.execute("SELECT video_location FROM course_videos WHERE course = %s", (cId, )); # find videos that belongs to this course
    for location in cursor.fetchall(): 
        rm_video_from_s3(location[0].split('/')[-1]); # rm video from bucket
    query = "DELETE FROM course_videos WHERE course = %s"; cursor.execute(query, (cId, )); db.commit() # rm all course_videos_paths
    query = "DELETE FROM student2courses WHERE course_id = %s"; cursor.execute(query, (cId, )); db.commit() # unroll all students
    query = "DELETE FROM courses WHERE id = %s"; cursor.execute(query, (cId, )); db.commit() # finally, remove course
    return True

def remove_topic(topicId):
    query = "DELETE FROM course_topics WHERE id = %s"; 
    cursor.execute(query, (topicId, )); 
    db.commit()

def remove_task(taskId):
    cursor.execute("DELETE FROM tasks_submissions WHERE task_id = %s", (taskId, ))
    query = "DELETE FROM course_tasks WHERE id = %s"; 
    cursor.execute(query, (taskId, )); 
    db.commit()

def remove_video(videoId):
    cursor.execute("SELECT video_location FROM course_videos WHERE id = %s", (videoId, ))
    rm_video_from_s3(cursor.fetchall()[0][0].split('/')[-1])
    cursor.execute("DELETE FROM course_videos WHERE id = %s", (videoId, ))
    db.commit()

def check_cretor(cId):
    query = "SELECT creator FROM courses WHERE id = %s"
    cursor.execute(query, (cId, ))
    return cursor.fetchall()

def student_submitted_tasks(cId, user):
    cursor.execute("""
    SELECT
    ct.title AS task_title, 
    ct.id AS task_id,
    ts.acceptance
    FROM 
    tasks_submissions ts 
    JOIN course_tasks ct ON ts.task_id = ct.id 
    JOIN courses c ON ct.course = c.id
    WHERE c.id = %s AND ts.student_id = (SELECT id FROM users WHERE username = %s)""", (cId, user))
    return cursor.fetchall()

def all_submitted_tasks(course):
    cursor.execute("""
    SELECT u.username, 
    ct.title AS task_title, 
    ct.id AS task_id, 
    u.id AS user_id,
    ts.acceptance
    FROM users u
    JOIN tasks_submissions ts ON ts.student_id = u.id
    JOIN course_tasks ct ON ct.id = ts.task_id
    JOIN courses c ON c.id = ct.course
    WHERE c.id = %s """, (course, ))
    return cursor.fetchall()

def get_recommends(user):
    query = """ SELECT id, title, thumbnail FROM courses WHERE domain = 
                (SELECT user_init_interest FROM users WHERE username = %s) 
                ORDER BY RAND() LIMIT 4"""
    cursor.execute(query, (user,))
    return cursor.fetchall()

def put_mark(uId, tId, mark):
    query = "UPDATE tasks_submissions SET acceptance = %s WHERE student_id = %s AND task_id = %s"
    cursor.execute(query, (mark, uId, tId))
    db.commit()
    print(uId, tId, "marked with", mark)
    return True
