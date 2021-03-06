from typing import Dict, List

from app.adapters.database.courseCategoriesModel import CourseCategoryDTO
from app.adapters.database.coursesModel import CourseDTO
from app.adapters.database.suscriptionCoursesModel import SuscriptionCourseDTO
from app.adapters.http.util.categoryUtil import CategoryUtil
from app.adapters.http.util.userServiceUtil import UserServiceUtil
from app.core.config import SCORE_SAME_CATEGORY, SCORE_SAME_COUNTRY
from app.core.logger import logger
from app.domain.courseCategories.courseCategory import CourseCategoryCreate
from app.domain.courseCategories.courseCategoryRepository import \
    CourseCategoryRepository
from app.domain.courses.courseRepository import CourseRepository
from fastapi import HTTPException
from sqlalchemy.orm import Session


class CourseUtil:

    def check_coursename(session: Session, coursename, id):
        courseRepository = CourseRepository(session)
        db_course = courseRepository.get_course_by_name(coursename)
        if db_course and id != db_course.id:
            logger.warning("Coursename " + coursename + " already in use")
            raise HTTPException(
                status_code=400, detail="Coursename " + coursename + " already in use"
            )

    def check_id_exists(session: Session, course_id):
        courseRepository = CourseRepository(session)
        db_course = courseRepository.get_course(course_id=course_id)
        if db_course is None:
            logger.warning("Course with id = " + str(course_id) + " not found")
            raise HTTPException(status_code=400, detail="Course not found")
        return db_course

    def check_course_exists(session: Session, id):
        repo = CourseRepository(session)
        course = repo.get_course(id)
        if not course:
            logger.warning("Course does not exist")
            raise HTTPException(status_code=400, detail="Course does not exist")

    def check_course_category(session: Session, courseCategory: CourseCategoryCreate):

        CourseUtil.check_course_exists(session, courseCategory.courseId)

        CategoryUtil.check_category_exists(session, courseCategory.categoryId)

        repo = CourseCategoryRepository(session)
        db_cc = repo.get_courseCategory(courseCategory.courseId, courseCategory.categoryId)
        if db_cc:
            logger.warning("Category already added")
            raise HTTPException(
                status_code=400, detail="Category already added"
            )

    def get_course_recomendation(session: Session, userId: int):
        user = UserServiceUtil.check_user_exists(userId)

        recommendations = {}

        courseRepo = CourseRepository(session)
        courses = courseRepo.get_all_active_courses()

        logger.info("Getting recommendations by category")
        CourseUtil.get_recommendation_by_category(userId, courses, recommendations)

        logger.info("Getting recommendations by country")
        CourseUtil.get_recommendation_by_country(user, courses, recommendations)

        recommendations = dict(sorted(recommendations.items(), key=lambda item: item[1], reverse=True))

        best_recommendations = []
        for i in range(0, 5):
            if len(recommendations.items()) != 0:
                max_key = max(recommendations, key=recommendations.get)
                best_recommendations.append(max_key)
                recommendations.pop(max_key)

        return best_recommendations

    def get_recommendation_by_category(userId: int, courses: List[CourseDTO], recommendations: Dict):
        user_courses_categories = UserServiceUtil.getUserCategories(userId)

        for course in courses:
            for category in course.categories:
                if category.categoryId in user_courses_categories:
                    if course.courseName in recommendations.keys():
                        recommendations[course] += SCORE_SAME_CATEGORY
                    else:
                        recommendations[course] = SCORE_SAME_CATEGORY

        return recommendations

    def get_recommendation_by_country(user: Dict, courses: List[CourseDTO], recommendations: Dict):

        users = UserServiceUtil.getActiveUsers()

        for course in courses:
            for collaborator in course.collaborators:
                if collaborator.isOwner:
                    logger.info("Collaborator with id: " + str(collaborator.userId) + " is owner")

                    owner = UserServiceUtil.getUserFromUsers(users, user["id"])
                    if owner and (owner["country"] == user["country"]):
                        logger.info("User has same country as owner")

                        if course.courseName in recommendations.keys():
                            recommendations[course] += SCORE_SAME_COUNTRY
                        else:
                            recommendations[course] = SCORE_SAME_COUNTRY

        return recommendations

    def getCoursesForResponse(courses: List[CourseDTO]):
        courses_full_info = []

        courses = set(courses)

        for course in courses:
            dict = course.__dict__
            dict['categories'] = list(map(CourseCategoryDTO.getCategory, course.categories))
            dict['suscriptions'] = list(map(SuscriptionCourseDTO.getSuscription, course.suscriptions))
            for collaborator in course.collaborators:
                if collaborator.isOwner:
                    dict['owner'] = UserServiceUtil.check_user_exists(collaborator.userId)

            courses_full_info.append(dict)

        return courses_full_info

    def cancelCourse(session: Session, course_id: int, throw=True):
        logger.info("Cancelling course " + str(course_id))
        repo = CourseRepository(session)
        db_course = CourseUtil.check_id_exists(session, course_id)
        if(db_course.status == 'Cancelled'):
            logger.warning("Course " + str(course_id) + " already cancelled")
            if throw:
                raise HTTPException(
                    status_code=400, detail=("Course " + str(course_id) + " already cancelled")
                )
        db_course.status = 'Cancelled'
        repo.update_course_with_id(db_course)
        return db_course

    def activateCourse(session: Session, course_id: int, throw=True):
        logger.info("Activating course " + str(course_id))
        repo = CourseRepository(session)
        db_course = CourseUtil.check_id_exists(session, course_id)
        if db_course.status == 'Active':
            logger.warning("Course " + str(course_id) + " already active")
            if throw:
                raise HTTPException(
                    status_code=400, detail=("Course " + str(course_id) + " already active")
                )
        db_course.status = 'Active'
        repo.update_course_with_id(db_course)
        return db_course
