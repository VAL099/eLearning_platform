
CREATE TABLE users(  
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL,
    name VARCHAR(100),
    email VARCHAR(255) NOT NULL,
    user_type varchar(8),
    user_init_interest varchar(50)
);

CREATE TABLE courses(  
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    description VARCHAR(500) NOT NULL,
    requirements VARCHAR(255) NOT NULL,
    domain VARCHAR(50) NOT NULL,
    thumbnail LONGTEXT,
    creator VARCHAR(50) NOT NULL
);

CREATE TABLE course_topics(  
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255),
    content JSON,
    course INT, 
    FOREIGN KEY (course) REFERENCES courses(id)
);

CREATE TABLE course_videos(  
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255),
    content TEXT,
    course INT, 
    video_location TEXT,
    FOREIGN KEY (course) REFERENCES courses(id)
);

CREATE TABLE course_tasks(  
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255),
    content JSON,
    course INT,
    FOREIGN KEY (course) REFERENCES courses(id)
);

CREATE TABLE student2courses (
    student_id INT,
    course_id INT,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

CREATE TABLE tasks_submissions (
    student_id INT,
    task_id INT,
    acceptance INT,
    content JSON,
    PRIMARY KEY (student_id, task_id),
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (task_id) REFERENCES course_tasks(id)
);