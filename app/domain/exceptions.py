class CourseNotFoundError(Exception):
    def __init__(self):
        self.message = "Course could not be found in database"
        super().__init__(self.message)
