from app.domain.categories.categoryRepository import CategoryRepository
from app.core.logger import logger
from fastapi import HTTPException
from sqlalchemy.orm import Session


class CategoryUtil:

    def check_category(session: Session, category_name):
        categoryRepository = CategoryRepository(session)
        db_category = categoryRepository.get_category_by_name(category_name)
        if db_category:
            logger.warning("Category " + category_name + " already exists")
            raise HTTPException(
                status_code=400, detail="Category " + category_name + " already exists"
            )

    def check_category_exists(session: Session, id: int):
        repo = CategoryRepository(session)
        category = repo.get_category(id)
        if not category:
            logger.warning("Category does not exist")
            raise HTTPException(status_code=400, detail="Category does not exist")
