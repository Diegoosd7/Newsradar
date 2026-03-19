from sqlalchemy.orm import Session


class CommonService:
    def __init__(self, db: Session):
        self.db = db
