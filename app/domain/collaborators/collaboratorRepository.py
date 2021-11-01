from sqlalchemy.orm import Session
from app.domain.collaborators.collaborator import CollaboratorCreate, Collaborator
from app.adapters.database.collaboratorsModel import CollaboratorDTO


class CollaboratorRepository:
    def __init__(self, session: Session):
        self.session: Session = session

    def get_collaborator(self, course_id: int, user_id: int):
        return self.session.query(CollaboratorDTO).filter(CollaboratorDTO.courseId == course_id).filter(CollaboratorDTO.userId == user_id).first()

    def get_collaborators_by_course(self, course_id: int, skip: int = 0, limit: int = 100):
        return self.session.query(CollaboratorDTO).filter(CollaboratorDTO.courseId == course_id).offset(skip).limit(limit).all()

    def get_collaborators(self, skip: int = 0, limit: int = 100):
        return self.session.query(CollaboratorDTO).offset(skip).limit(limit).all()

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
