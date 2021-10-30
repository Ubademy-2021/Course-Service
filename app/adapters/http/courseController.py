from app.adapters.database.database import SessionLocal
from app.adapters.database.coursesModel import CourseDTO
from app.adapters.http.util.courseUtil import CourseUtil
from app.domain.courses.course import CourseCreate, Course
from app.domain.courses.courseRepository import CourseRepository
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.logger import logger

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
    crud = CourseRepository(db)
    CourseUtil.check_coursename(crud, course.courseName)
    return crud.create_course(course=course)


@router.get("/courses", response_model=List[Course])
def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info("Getting courses list")
    crud = CourseRepository(db)
    courses = crud.get_courses(skip=skip, limit=limit)
    logger.debug("Getting " + str(courses.count(CourseDTO)) + " courses")
    return courses


@router.get("/courses/{course_id}", response_model=Course)
def read_course(course_id: int, db: Session = Depends(get_db)):
    logger.info("Getting course with id = " + str(course_id))
    crud = CourseRepository(db)
    db_course = CourseUtil.check_id_exists(crud, course_id)
    return db_course


@router.post("/courses/cancel/{course_id}", response_model=Course)
def cancel_course(course_id: int, db: Session = Depends(get_db)):
    logger.info("Creating course " + str(course_id))
    crud = CourseRepository(db)
    db_course = CourseUtil.check_id_exists(crud, course_id)
    if(db_course.status == 'Cancelled'):
        logger.warn("Course " + str(course_id) + " already blocked")
        raise HTTPException(
            status_code=400, detail=("Course " + str(course_id) + " already blocked")
        )
    db_course.status = 'Cancelled'
    crud.update_course_with_id(db_course)
    return db_course
