from typing import List, Optional

from app.adapters.database.courseCategoriesModel import CourseCategoryDTO
from app.adapters.database.courseInscriptionsModel import CourseInscriptionDTO
from app.adapters.database.database import SessionLocal
from app.adapters.database.suscriptionCoursesModel import SuscriptionCourseDTO
from app.adapters.http.util.collaboratorUtil import CollaboratorUtil
from app.adapters.http.util.courseUtil import CourseUtil
from app.core.logger import logger
from app.domain.courseCategories.courseCategory import (CourseCategory,
                                                        CourseCategoryCreate)
from app.domain.courseCategories.courseCategoryRepository import \
    CourseCategoryRepository
from app.domain.courseInscriptions.courseInscriptionRepository import \
    CourseInscriptionRepository
from app.domain.courses.course import Course, CourseBase, CourseCreate
from app.domain.courses.courseRepository import CourseRepository
from app.domain.exceptions import CourseNotFoundError
from app.domain.suscriptionCourses.suscriptionCourseRepository import \
    SuscriptionCourseRepository
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

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
        raise HTTPException(status_code=400, detail=e.message)

    logger.info("Course course with id " + str(course_id) + " updates successfully")
    return course_updated


@router.get("/courses")
def read_courses(
    skip: int = 0,
    limit: int = 100,
    course_id: Optional[int] = None,
    active: Optional[bool] = None,
    category_id: Optional[int] = None,
    suscription_id: Optional[int] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    repo = CourseRepository(db)
    courses = []

    if course_id:
        logger.info("Getting course with id = " + str(course_id))

        CourseUtil.check_course_exists(db, course_id)
        courses.append(repo.get_course(course_id))
    elif active:
        logger.info("Getting active courses")

        courses = repo.get_active_courses(skip=skip, limit=limit)
    elif category_id:
        logger.info("Getting course with category id = " + str(category_id))

        repo = CourseCategoryRepository(db)
        courses = repo.get_courses_by_category(category_id, skip=skip, limit=limit)
        logger.debug("Got " + str(len(courses)) + " courses for category id: " + str(category_id))

        courses = list(map(CourseCategoryDTO.getCourse, courses))
    elif suscription_id:
        logger.info("Getting course with suscription id = " + str(suscription_id))

        repo = SuscriptionCourseRepository(db)
        courses = repo.get_courses_by_suscription(suscription_id, skip=skip, limit=limit)
        logger.debug("Got " + str(len(courses)) + " courses for suscription id: " + str(suscription_id))

        courses = list(map(CourseCategoryDTO.getCourse, courses))
    elif user_id:
        logger.info("Getting courses in which user " + str(user_id) + " is a student")

        repo = CourseInscriptionRepository(db)
        courses = repo.get_courses_by_student(user_id, skip=skip, limit=limit)
        logger.debug("Got " + str(len(courses)) + " courses for user id: " + str(user_id))

        courses = list(map(CourseInscriptionDTO.getCourse, courses))
    else:
        logger.info("Getting all courses")
        courses = repo.get_courses(skip=skip, limit=limit)

    return CourseUtil.getCoursesForResponse(courses)


@router.get("/courses/active", response_model=List[Course])
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


@router.get("/courses/recommendation/{user_id}")
def get_course_recomendation(user_id: int, db: Session = Depends(get_db)):
    logger.info("Getting courses recommendation for user with id " + str(user_id))
    courses_to_recommend = CourseUtil.get_course_recomendation(db, user_id)

    return CourseUtil.getCoursesForResponse(courses_to_recommend)
