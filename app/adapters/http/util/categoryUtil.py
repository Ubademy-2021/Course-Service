from app.domain.categories.categoryRepository import CategoryRepository
from app.core.logger import logger
from fastapi import HTTPException


class CategoryUtil:

    def check_category(categoryRepository: CategoryRepository, category_name):
        db_category = categoryRepository.get_category_by_name(category_name)
        if db_category:
            logger.warn("Category " + category_name + " already exists")
            raise HTTPException(
                status_code=400, detail="Category " + category_name + " already exists"
            )
