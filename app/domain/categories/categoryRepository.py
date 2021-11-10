from sqlalchemy.orm import Session
from app.domain.categories.category import CategoryBase
from app.adapters.database.categoriesModel import CategoryDTO


class CategoryRepository:
    def __init__(self, session: Session):
        self.session: Session = session

    def get_category(self, category_id: int):
        return (
            self.session.query(CategoryDTO)
            .filter(CategoryDTO.id == category_id)
            .first()
        )

    def get_category_by_name(self, name: str):
        return self.session.query(CategoryDTO).filter(CategoryDTO.name == name).first()

    def get_categories(self, skip: int = 0, limit: int = 100):
        return self.session.query(CategoryDTO).offset(skip).limit(limit).all()

    def get_all_categories(self):
        return self.session.query(CategoryDTO).all()

    def create_category(self, category: CategoryBase):
        session_category = CategoryDTO()
        session_category.initWithCategoryBase(category)
        self.session.add(session_category)
        self.session.commit()
        self.session.refresh(session_category)
        return session_category
