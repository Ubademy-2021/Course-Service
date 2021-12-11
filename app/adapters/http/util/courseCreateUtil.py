from app.adapters.database.collaboratorsModel import CollaboratorDTO
from app.adapters.database.coursesModel import CourseDTO
from app.adapters.http.util.categoryUtil import CategoryUtil
from app.adapters.http.util.courseUtil import CourseUtil
from app.adapters.http.util.suscriptionUtil import SuscriptionUtil
from app.adapters.http.util.userServiceUtil import UserServiceUtil
from app.domain.collaborators.collaboratorRepository import \
    CollaboratorRepository
from app.domain.courses.course import CourseCreate
from app.domain.courses.courseRepository import CourseRepository
from sqlalchemy.orm import Session


class CourseCreateUtil:

    def createCourse(session: Session, course: CourseCreate):
        CourseUtil.check_coursename(session, course.courseName, 0)

        SuscriptionUtil.check_suscription_exists(session, course.suscriptionId)

        for categoryId in course.categoryIds:
            CategoryUtil.check_category_exists(session, categoryId)

        repo = CourseRepository(session)
        db_course = repo.create_course(course=course)
        CourseCreateUtil.createOwner(session, db_course, course.ownerId)
        SuscriptionUtil.make_course_suscription(session, db_course.id, course.suscriptionId)

        for categoryId in course.categoryIds:
            CategoryUtil.createCourseCategory(session, db_course.id, categoryId)

        return db_course

    def createOwner(session: Session, course: CourseDTO, ownerId: int):

        UserServiceUtil.check_user_exists(ownerId)

        collaborator = CollaboratorDTO()
        collaborator.courseId = course.id
        collaborator.userId = ownerId
        collaborator.isOwner = True
        repo = CollaboratorRepository(session)
        return repo.add_collaborator(collaborator)
