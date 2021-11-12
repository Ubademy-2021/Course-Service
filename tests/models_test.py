import unittest
from datetime import datetime

from app.adapters.database.categoriesModel import CategoryDTO
from app.adapters.database.collaboratorsModel import CollaboratorDTO
from app.adapters.database.courseCategoriesModel import CourseCategoryDTO
from app.adapters.database.courseInscriptionsModel import CourseInscriptionDTO
from app.adapters.database.coursesModel import CourseDTO
from app.adapters.database.suscriptionCoursesModel import SuscriptionCourseDTO
from app.adapters.database.suscriptionInscriptionsModel import \
    SuscriptionInscriptionDTO
from app.adapters.database.suscriptionsModel import SuscriptionDTO
from app.domain.categories.category import CategoryBase
from app.domain.collaborators.collaborator import CollaboratorCreate
from app.domain.courseCategories.courseCategory import CourseCategoryCreate
from app.domain.courseInscriptions.courseInscription import \
    CourseInscriptionCreate
from app.domain.courses.course import CourseCreate
from app.domain.suscriptionCourses.suscriptionCourse import SuscriptionCourse
from app.domain.suscriptionInscriptions.suscriptionInscription import \
    SuscriptionInscriptionCreate
from app.domain.suscriptions.suscription import SuscriptionCreate


def make_default_categoryBase():
    category = CategoryBase(
        name="asda"
    )
    return category


def make_default_collaboratorCreate():
    collaborator = CollaboratorCreate(
        courseId=1,
        userId=1
    )
    return collaborator


def make_default_courseCategoryCreate():
    cc = CourseCategoryCreate(
        courseId=1,
        categoryId=1
    )
    return cc


def make_default_courseInscriptionCreate():
    ci = CourseInscriptionCreate(
        courseId=1,
        userId=1
    )
    return ci


def make_default_courseCreate():
    course = CourseCreate(
        courseName="str",
        duration="16:00:00",
        inscriptionPrice=14,
        ownerId=1
    )
    return course


def make_default_suscriptionCourse():
    sc = SuscriptionCourse(
        courseId=1,
        suscriptionId=1
    )
    return sc


def make_default_suscriptionInscriptionCreate():
    si = SuscriptionInscriptionCreate(
        userId=1,
        suscriptionId=1
    )
    return si


def make_default_suscriptionCreate():
    suscription = SuscriptionCreate(
        price=13,
        description="asd"
    )
    return suscription


class TestModels(unittest.TestCase):

    def test_category_model(self):
        model = make_default_categoryBase()
        dto = CategoryDTO()
        dto.initWithCategoryBase(model)
        assert dto.name == model.name

    def test_collaborator_model(self):
        model = make_default_collaboratorCreate()
        assert model.isComplete()
        dto = CollaboratorDTO()
        dto.initWithCollaboratorCreate(model)
        assert dto.courseId == model.courseId
        assert dto.getUserId() == model.userId

    def test_course_categoy_model(self):
        model = make_default_courseCategoryCreate()
        assert model.isComplete()
        dto = CourseCategoryDTO()
        dto.initWithCourseCategoryCreate(model)
        assert dto.courseId == model.courseId
        assert dto.categoryId == model.categoryId

    def test_course_inscription_model(self):
        model = make_default_courseInscriptionCreate()
        assert model.isComplete()
        dto = CourseInscriptionDTO()
        dto.initWithCourseInscriptionCreate(model)
        assert dto.courseId == model.courseId
        assert dto.getUserId() == model.userId

    def test_course_model(self):
        start = datetime.now()
        model = make_default_courseCreate()
        assert model.isComplete()
        dto = CourseDTO()
        dto.initWithCourseCreate(model)
        assert dto.courseName == model.courseName
        assert dto.duration == model.duration
        assert dto.inscriptionPrice == model.inscriptionPrice
        assert dto.status == "Active"
        assert dto.createdDate >= start

    def test_suscription_course_model(self):
        model = make_default_suscriptionCourse()
        dto = SuscriptionCourseDTO()
        dto.initWithSuscriptionCourse(model)
        assert dto.courseId == model.courseId
        assert dto.suscriptionId == model.suscriptionId

    def test_suscription_inscription_model(self):
        model = make_default_suscriptionInscriptionCreate()
        assert model.isComplete()
        dto = SuscriptionInscriptionDTO()
        dto.initWithSuscriptionInscriptionCreate(model)
        assert dto.userId == model.userId
        assert dto.suscriptionId == model.suscriptionId

    def test_suscription_model(self):
        model = make_default_suscriptionCreate()
        assert model.isComplete()
        dto = SuscriptionDTO()
        dto.initWithSuscriptionCreate(model)
        assert dto.price == model.price
        assert dto.description == model.description
