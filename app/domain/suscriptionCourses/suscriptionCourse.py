from pydantic import BaseModel


class SuscriptionCourse(BaseModel):
    courseId: int
    suscriptionId: int

    class Config:
        orm_mode = True
