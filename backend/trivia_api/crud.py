from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import UnmappedInstanceError
from .models import Model


class TriviaCRUD(object):
    def __init__(self, database_uri: str):
        self.engine = create_engine(database_uri)
        self.create_all()
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def create_all(self):
        Model.metadata.create_all(self.engine)

    def drop_all(self):
        Model.metadata.drop_all(self.engine)

    @contextmanager
    def auto_save(self):
        try:
            yield self.session
            self.session.commit()
        except UnmappedInstanceError as e:
            self.session.rollback()
            print(e)
        finally:
            self.session.close()

    # Create
    def add(self, model: Model):
        with self.auto_save() as db:
            db.add(model)
            
    def add_all(self, models: list):
        with self.auto_save() as db:
            db.add_all(models)

    # Read
    def all(self, model_class: Model) -> list:
        models = self.session.query(model_class).all()
        return models

    def get(self, model_class: Model, model_id: int) -> Model:
        model = self.session.query(model_class).get(model_id)
        return model

    # Update
    def update(self):
        with self.auto_save():
            pass
    
    # Delete
    def delete(self, model_class: Model, model_id: int) -> bool:
        deleted = True

        with self.auto_save() as db:
            model = self.get(model_class, model_id)

            if model is None:
                deleted = False

            db.delete(model)

        return deleted
