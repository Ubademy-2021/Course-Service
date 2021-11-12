from app.adapters.database.courseCategoriesModel import CourseCategoryDTO
from app.adapters.database.database import SessionLocal
from app.adapters.database.coursesModel import CourseDTO
from app.adapters.database.suscriptionCoursesModel import SuscriptionCourseDTO
from app.adapters.http.util.categoryUtil import CategoryUtil
from app.adapters.http.util.collaboratorUtil import CollaboratorUtil
from app.adapters.http.util.courseUtil import CourseUtil
from app.domain.courseCategories.courseCategory import CourseCategory, CourseCategoryCreate
from app.domain.courseCategories.courseCategoryRepository import CourseCategoryRepository
from app.domain.courses.course import CourseBase, CourseCreate, Course
from app.domain.courses.courseRepository import CourseRepository
from app.domain.exceptions import CourseNotFoundError
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
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
        logger.warning("Required fields are not complete")
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
def read_courses(
    skip: int = 0, 
    limit: int = 100,
    course_id: Optional[int] = None,
    active: Optional[bool] = None,
    category_id: Optional[int] = None,
    suscription_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    repo = CourseRepository(db)

    if course_id:
        logger.info("Getting course with id = " + str(course_id))
        CourseUtil.check_course_exists(db, course_id)
        courses = []
        courses.append(repo.get_course(course_id))
        return courses
    elif active == True:
        logger.info("Getting active courses")
        return repo.get_active_courses(skip=skip, limit=limit)
    elif category_id:
        logger.info("Getting course with category id = " + str(category_id))
        repo = CourseCategoryRepository(db)
        courses = repo.get_courses_by_category(category_id, skip=skip, limit=limit)
        logger.debug("Got " + str(len(courses)) + " courses for category id: " + str(category_id))
        return list(map(CourseCategoryDTO.getCourse, courses))
    elif suscription_id:
        logger.info("Getting course with suscription id = " + str(category_id))
        repo = SuscriptionCourseRepository(db)
        courses = repo.get_courses_by_suscription(suscription_id, skip=skip, limit=limit)
        logger.debug("Got " + str(len(courses)) + " courses for suscription id: " + str(category_id))
        return list(map(CourseCategoryDTO.getCourse, courses))

    logger.info("Getting all courses")
    return (repo.get_courses(skip=skip, limit=limit))
    

@router.get("/courses/suscription/{suscriptionId}", response_model=List[Course])
def read_courses_from_suscription(
    suscriptionId: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    logger.info("Getting course list of suscription " + str(suscriptionId))
    crud = SuscriptionCourseRepository(db)
    courses = crud.get_courses_by_suscription(suscriptionId, skip=skip, limit=limit)
    logger.debug("Getting " + str(len(courses)) + " courses")
    return list(map(SuscriptionCourseDTO.getCourse, courses))


@router.get("/courses/active/", response_model=List[Course])
def read_active_courses(db: Session = Depends(get_db)):
    logger.info("Getting active course list")
    crud = CourseRepository(db)
    courses = crud.get_all_active_courses()
    logger.debug("Getting " + str(len(courses)) + " courses")
    return courses


@router.put("/courses/cancel/{course_id}", response_model=Course)
def cancel_course(course_id: int, db: Session = Depends(get_db)):
    logger.info("Creating course " + str(course_id))
    repo = CourseRepository(db)
    db_course = CourseUtil.check_id_exists(db, course_id)
    if(db_course.status == 'Cancelled'):
        logger.warning("Course " + str(course_id) + " already cancelled")
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
        logger.warning("Required fields are not complete")
        raise HTTPException(status_code=400, detail="Required fields are not complete")
    repo = CourseCategoryRepository(db)
    CourseUtil.check_course_category(db, courseCategory)
    return repo.create_courseCategory(courseCategory)


@router.get("/courses/recommendation/{user_id}", response_model=List[Course])
def get_course_recomendation(user_id: int, db: Session = Depends(get_db)):
    logger.info("Getting courses recommendation for user with id " + str(user_id))
    courses_to_recommend = CourseUtil.get_course_recomendation(db, user_id)

    return courses_to_recommend
