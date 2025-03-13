from chalice import Chalice, BadRequestError, NotFoundError
import uuid
import json
from services.dynamodb_service import DynamoDBService
from services.sns_service import SNSService
from services.validation import validate_student_request
from models.student_model import Student

app = Chalice(app_name="student-management")

# Initialize Services
db_service = DynamoDBService()
sns_service = SNSService()

@app.route("/students", methods=["POST"])
def create_student():
    """Create a new student and notify via SNS"""
    request = app.current_request.json_body
    student_data = validate_student_request(request)

    student = Student(**student_data)
    db_service.save_student(student)

    # Send notification to SNS
    sns_service.send_notification("New Student Created", student.to_dict())

    return {"message": "Student created", "student": student.to_dict()}


@app.route("/students", methods=["GET"])
def list_students():
    """List all students"""
    students = db_service.get_all_students()
    return {"students": students}


@app.route("/students/{student_id}", methods=["GET"])
def get_student(student_id):
    """Retrieve a student by ID"""
    student = db_service.get_student(student_id)
    if not student:
        raise NotFoundError(f"Student with ID {student_id} not found")
    return student


@app.route("/students/{student_id}", methods=["PUT"])
def update_student(student_id):
    """Update a student's details and notify via SNS"""
    request = app.current_request.json_body
    student_data = validate_student_request(request)

    updated_student = db_service.update_student(student_id, student_data)

    # Send update notification to SNS
    sns_service.send_notification("Student Updated", updated_student)

    return {"message": "Student updated", "student": updated_student}


@app.route("/students/{student_id}", methods=["DELETE"])
def delete_student(student_id):
    """Delete a student and notify via SNS"""
    db_service.delete_student(student_id)

    # Send delete notification to SNS
    sns_service.send_notification("Student Deleted", {"id": student_id})

    return {"message": f"Student {student_id} deleted"}
