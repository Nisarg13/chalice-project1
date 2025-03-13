import uuid

class Student:
    def __init__(self, name, age, course, student_id=None):
        self.id = student_id if student_id else str(uuid.uuid4())
        self.name = name
        self.age = age
        self.course = course

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "course": self.course
        }
