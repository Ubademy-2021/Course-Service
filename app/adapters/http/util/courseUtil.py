from app.adapters.http.util.categoryUtil import CategoryUtil
from app.domain.categories.categoryRepository import CategoryRepository
from app.domain.courseCategories.courseCategory import CourseCategoryCreate
from app.domain.courseCategories.courseCategoryRepository import CourseCategoryRepository
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

    def check_course_exists(repo: CourseRepository, id):
        course = repo.get_course(id)
        if not course:
            logger.error("Course does not exist")
            raise HTTPException(status_code=400, detail="Course does not exist")

    def check_course_category(repo: CourseCategoryRepository, courseCategory: CourseCategoryCreate):

        courseRepo = CourseRepository(repo.session)
        CourseUtil.check_course_exists(courseRepo, courseCategory.courseId)

        categoryRepo = CategoryRepository(repo.session)
        CategoryUtil.check_category_exists(categoryRepo, courseCategory.categoryId)

        db_cc = repo.get_courseCategory(courseCategory.courseId, courseCategory.categoryId)
        if db_cc:
            logger.warn("Category already added")
            raise HTTPException(
                status_code=400, detail="Category already added"
            )
