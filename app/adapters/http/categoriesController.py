from app.adapters.database.database import SessionLocal
from app.adapters.database.categoriesModel import CategoryDTO
from app.domain.categories.category import Category, CategoryBase
from app.domain.categories.categoryRepository import CategoryRepository
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.logger import logger
from app.adapters.http.util.categoryUtil import CategoryUtil


router = APIRouter(tags=["categories"])


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.critical("Internal Error: " + e.__str__())
    finally:
        db.close()


@router.get("/categories", response_model=List[Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info("Getting categories list")
    repo = CategoryRepository(db)
    categories = repo.get_categories(skip=skip, limit=limit)
    logger.debug("Getting " + str(len(categories)) + " categories")
    return categories


@router.get("/categories/{categoryId}", response_model=List[Category])
def read_category(categoryId, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info("Getting category " + str(categoryId))
    category = CategoryUtil.check_category_exists(db, categoryId)
    return category


@router.get("/categories/all", response_model=List[Category])
def read_all_categories(db: Session = Depends(get_db)):
    logger.info("Getting all categories")
    repo = CategoryRepository(db)
    categories = repo.get_all_categories()
    logger.debug("Getting " + str(len(categories)) + " categories")
    return categories


@router.post("/categories", response_model=Category)
def create_category(category: CategoryBase, db: Session = Depends(get_db)):
    logger.info("Creating " + category.name + " category")
    if not category.name:
        logger.warning("Required fields are not complete")
        raise HTTPException(status_code=400, detail="Required fields are not complete")
    repo = CategoryRepository(db)
    CategoryUtil.check_category(db, category.name)
    return repo.create_category(category=category)
