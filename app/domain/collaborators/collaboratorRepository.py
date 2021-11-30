from app.adapters.database.collaboratorsModel import CollaboratorDTO
from app.domain.collaborators.collaborator import (Collaborator,
                                                   CollaboratorCreate)
from sqlalchemy.orm import Session


class CollaboratorRepository:
    def __init__(self, session: Session):
        self.session: Session = session

    def get_collaborator(self, course_id: int, user_id: int):
        return self.session.query(CollaboratorDTO).filter(CollaboratorDTO.courseId == course_id).filter(CollaboratorDTO.userId == user_id).first()

    def get_collaborators_by_course(self, course_id: int, skip: int = 0, limit: int = 100):
        return self.session.query(CollaboratorDTO).filter(CollaboratorDTO.courseId == course_id).offset(skip).limit(limit).all()

    def get_courses_by_collaborator(self, collaborator_id: int, skip: int = 0, limit: int = 100):
        return self.session.query(CollaboratorDTO).filter(CollaboratorDTO.userId == collaborator_id).offset(skip).limit(limit).all()

    def get_courses_by_owner(self, owner_id: int, skip: int = 0, limit: int = 100):
        return self.session.query(CollaboratorDTO).filter(CollaboratorDTO.userId == owner_id).filter(CollaboratorDTO.isOwner == True).offset(skip).limit(limit).all()

    def get_collaborators(self, skip: int = 0, limit: int = 100):
        return self.session.query(CollaboratorDTO).offset(skip).limit(limit).all()

    def get_all_collaborators(self):
        return self.session.query(CollaboratorDTO).all()

    def create_collaborator(self, collaborator: CollaboratorCreate):
        session_collaborator = CollaboratorDTO()
        session_collaborator.initWithCollaboratorCreate(collaborator)
        self.session.add(session_collaborator)
        self.session.commit()
        self.session.refresh(session_collaborator)
        return session_collaborator

    def update_collaborator_with_id(self, collaborator_updated: Collaborator):
        # Only use with collaborator gotten from database
        self.session.add(collaborator_updated)
        self.session.commit()
        self.session.refresh(collaborator_updated)
        return collaborator_updated

    def add_collaborator(self, collaborator: CollaboratorDTO):
        self.session.add(collaborator)
        self.session.commit()
        self.session.refresh(collaborator)
        return collaborator
