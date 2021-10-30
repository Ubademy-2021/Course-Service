from app.adapters.database.database import SessionLocal
from app.adapters.database.coursesModel import CourseDTO
from app.adapters.database.suscriptionCoursesModel import SuscriptionCourseDTO
from app.adapters.http.util.courseUtil import CourseUtil
from app.domain.courses.course import CourseCreate, Course
from app.domain.courses.courseRepository import CourseRepository
from app.domain.exceptions import CourseNotFoundError
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.logger import logger
from app.domain.suscriptionCourses.suscriptionCourseRepository import SuscriptionCourseRepository

router = APIRouter(tags=["courses"])


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.critical("Internal Error: " + e.__str__())
    finally:
        db.close()


@router.post("/courses", response_model=Course)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    logger.info("Creating course " + course.courseName)
    if not course.isComplete():
        logger.warn("Required fields are not complete")
        raise HTTPException(status_code=400, detail="Required fields are not complete")
    repo = CourseRepository(db)
    CourseUtil.check_coursename(repo, course.courseName)
    return repo.create_course(course=course)


@router.put("/courses/{course_id}", response_model=Course)
def update_course(course_id: int, course_updated: CourseCreate, db: Session = Depends(get_db)):
    logger.info("Updating course with id " + str(course_id))
    repo = CourseRepository(db)

    try:
        course_updated = repo.update_course(course_id, course_updated)
    except CourseNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)

    logger.info("Course course with id " + str(course_id) + " updates successfully")
    return course_updated


@router.get("/courses", response_model=List[Course])
def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info("Getting courses list")
    repo = CourseRepository(db)
    courses = repo.get_courses(skip=skip, limit=limit)
    logger.debug("Getting " + str(courses.count(CourseDTO)) + " courses")
    return courses


@router.get("/courses/{course_id}", response_model=Course)
def read_course(course_id: int, db: Session = Depends(get_db)):
    logger.info("Getting course with id = " + str(course_id))
    repo = CourseRepository(db)
    db_course = CourseUtil.check_id_exists(repo, course_id)
    return db_course


@router.get("/courses/{suscriptionId}", response_model=List[Course])
def read_courses_from_suscription(
    suscriptionId, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    logger.info("Getting course list of suscription " + str(suscriptionId))
    crud = SuscriptionCourseRepository(db)
    courses = crud.get_cou(suscriptionId, skip=skip, limit=limit)
    logger.debug("Getting " + str(courses.count(SuscriptionCourseDTO)) + " courses")
    return list(map(SuscriptionCourseDTO.getCourse, courses))



@router.post("/courses/cancel/{course_id}", response_model=Course)
def cancel_course(course_id: int, db: Session = Depends(get_db)):
    logger.info("Creating course " + str(course_id))
    repo = CourseRepository(db)
    db_course = CourseUtil.check_id_exists(repo, course_id)
    if(db_course.status == 'Cancelled'):
        logger.warn("Course " + str(course_id) + " already blocked")
        raise HTTPException(
            status_code=400, detail=("Course " + str(course_id) + " already blocked")
        )
    db_course.status = 'Cancelled'
    repo.update_course_with_id(db_course)
    return db_course
