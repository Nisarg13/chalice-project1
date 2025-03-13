from chalice import BadRequestError

def validate_student_request(request):
    if not isinstance(request, dict):
        raise BadRequestError("Invalid request format. Expected JSON object.")

    required_fields = ["name", "age", "course"]

    for field in required_fields:
        if field not in request:
            raise BadRequestError(f"Missing required field: {field}")

    if not isinstance(request["name"], str) or len(request["name"].strip()) == 0:
        raise BadRequestError("Name must be a non-empty string.")

    if not isinstance(request["age"], int) or request["age"] <= 0:
        raise BadRequestError("Age must be a positive integer.")

    if not isinstance(request["course"], str) or len(request["course"].strip()) == 0:
        raise BadRequestError("Course must be a non-empty string.")

    return request
