from app.adapters.database.courseCategoriesModel import CourseCategoryDTO
from app.adapters.database.database import SessionLocal
from app.adapters.database.coursesModel import CourseDTO
from app.adapters.database.suscriptionCoursesModel import SuscriptionCourseDTO
from app.adapters.http.util.collaboratorUtil import CollaboratorUtil
from app.adapters.http.util.courseUtil import CourseUtil
from app.domain.courseCategories.courseCategory import CourseCategory, CourseCategoryCreate
from app.domain.courseCategories.courseCategoryRepository import CourseCategoryRepository
from app.domain.courses.course import CourseBase, CourseCreate, Course
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
    CourseUtil.check_coursename(db, course.courseName)
    db_course = repo.create_course(course=course)
    CollaboratorUtil.createOwner(db, db_course, course.ownerId)
    return db_course


@router.put("/courses/{course_id}", response_model=Course)
def update_course(course_id: int, course_updated: CourseBase, db: Session = Depends(get_db)):
    logger.info("Updating course with id " + str(course_id))

    CourseUtil.check_coursename(db, course_updated.courseName)
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
    db_course = CourseUtil.check_id_exists(db, course_id)
    return db_course


@router.get("/courses/suscription/{suscriptionId}", response_model=List[Course])
def read_courses_from_suscription(
    suscriptionId: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    logger.info("Getting course list of suscription " + str(suscriptionId))
    crud = SuscriptionCourseRepository(db)
    courses = crud.get_courses_by_suscription(suscriptionId, skip=skip, limit=limit)
    logger.debug("Getting " + str(courses.count(SuscriptionCourseDTO)) + " courses")
    return list(map(SuscriptionCourseDTO.getCourse, courses))


@router.put("/courses/cancel/{course_id}", response_model=Course)
def cancel_course(course_id: int, db: Session = Depends(get_db)):
    logger.info("Creating course " + str(course_id))
    repo = CourseRepository(db)
    db_course = CourseUtil.check_id_exists(db, course_id)
    if(db_course.status == 'Cancelled'):
        logger.warn("Course " + str(course_id) + " already cancelled")
        raise HTTPException(
            status_code=400, detail=("Course " + str(course_id) + " already cancelled")
        )
    db_course.status = 'Cancelled'
    repo.update_course_with_id(db_course)
    return db_course


@router.post("/courses/category", response_model=CourseCategory)
def add_category_to_course(courseCategory: CourseCategoryCreate, db: Session = Depends(get_db)):
    logger.info("Adding category to course")
    if not courseCategory.isComplete():
        logger.warn("Required fields are not complete")
        raise HTTPException(status_code=400, detail="Required fields are not complete")
    repo = CourseCategoryRepository(db)
    CourseUtil.check_course_category(db, courseCategory)
    return repo.create_courseCategory(courseCategory)


@router.get("/courses/category/{category_id}", response_model=List[Course])
def read_courses_by_category(category_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info("Getting courses by category")
    repo = CourseCategoryRepository(db)
    courses = repo.get_courses_by_category(category_id, skip=skip, limit=limit)
    logger.debug("Getting " + str(courses.count(CourseCategoryDTO)) + " courses")
    return list(map(CourseCategoryDTO.getCourse, courses))


@router.get("/courses/recommendation/{user_id}", response_model=List[Course])
def get_course_recomendation(user_id: int, db: Session = Depends(get_db)):
    logger.info("Getting courses recommendation for user with id " + str(user_id))
    courses_to_recommend = CourseUtil.get_course_recomendation(db, user_id)

    return courses_to_recommend
