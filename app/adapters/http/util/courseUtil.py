from app.domain.courses.courseRepository import CourseRepository
from app.core.logger import logger
from fastapi import HTTPException


class CourseUtil:

    def check_coursename(courseRepository: CourseRepository, coursename):
        db_course = courseRepository.get_course_by_name(coursename)
        if db_course:
            logger.warn("Coursename " + coursename + " already in use")
            raise HTTPException(
                status_code=400, detail="Coursename " + coursename + " already in use"
            )

    def check_id_exists(courseRepository: CourseRepository, course_id):
        db_course = courseRepository.get_course(course_id=course_id)
        if db_course is None:
            logger.warning("Course with id = " + str(course_id) + " not found")
            raise HTTPException(status_code=404, detail="Course not found")
        return db_course
