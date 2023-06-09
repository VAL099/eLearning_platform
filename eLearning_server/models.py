from pydantic import BaseModel

class User(BaseModel):
    username:str
    password:str
    name:str | None=None
    email:str | None=None
    user_type:str | None=None
    user_interest:str | None=None

class Course(BaseModel):
    name:str
    description:str
    requirements:str
    course_domain:str
    creator:str
    thumb:bytes

class PRecovery(BaseModel):
    email:str | None=None
    code:int | None=None
    password:str | None=None

class Topic(BaseModel):
    name:str
    content:str
    parent_course:int

class Submission(BaseModel):
    task:int
    username:str
    content:str

class VideoTopic(BaseModel):
    title:str
    fn:str
    content:str
    parent_course:int