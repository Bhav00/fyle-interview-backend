from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentSubmitSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)



@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def list_assignments(p):
    """Returns list of assignments submitted to the teacher"""
    submitted_assignments = Assignment.assignments_submitted_to_teacher(p.teacher_id)
    submitted_assignments_dump = AssignmentSchema().dump(submitted_assignments, many=True)
    return APIResponse.respond(data=submitted_assignments_dump)
