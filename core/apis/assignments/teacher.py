from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.assignments import AssignmentStateEnum
from core.models.assignments import GradeEnum
from core.libs import assertions
from marshmallow.exceptions import ValidationError


from .schema import AssignmentSchema, AssignmentGradeSchema 
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def list_assignments(p):
    """Returns list of assignments submitted to the teacher"""
    submitted_assignments = Assignment.assignments_submitted_to_teacher(p.teacher_id, AssignmentStateEnum.SUBMITTED)
    submitted_assignments_dump = AssignmentSchema().dump(submitted_assignments, many=True)
    return APIResponse.respond(data=submitted_assignments_dump)


@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    submit_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
	
    submitted_assignment = Assignment.grade_assignments(
        _id=submit_assignment_payload.id,
        _grade=submit_assignment_payload.grade,
        principal=p
    )
    db.session.commit()
    try:
        submitted_assignment_dump = AssignmentSchema().dump(submitted_assignment)
    except:
        raise ValidationError 
    
    return APIResponse.respond(data=submitted_assignment_dump)
