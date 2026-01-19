from sqlalchemy.orm import Session
from app.models.list_model import ListModel
from app.schemas.list_schema import NewTodoList, UpdateTodoList

def get_todo_lists(db: Session, per_page: int | None = None, page: int | None = None):
    query = db.query(ListModel)
    if per_page is not None and page is not None:
        offset = per_page * (page - 1)
        query = query.offset(offset).limit(per_page)
    return query.all()

def get_todo_list(db: Session, list_id: int):
    return db.query(ListModel).filter(ListModel.id == list_id).first()

def create_todo_list(db: Session, todo_list: NewTodoList):
    db_list = ListModel(
        title=todo_list.title,
        description=todo_list.description,
    )
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list

def update_todo_list(db: Session, list_id: int, todo_list: UpdateTodoList):
    db_list = get_todo_list(db, list_id)
    if db_list:
        if todo_list.title is not None:
            db_list.title = todo_list.title
        if todo_list.description is not None:
            db_list.description = todo_list.description
        db.commit()
        db.refresh(db_list)
    return db_list

def delete_todo_list(db: Session, list_id: int):
    db_list = get_todo_list(db, list_id)
    if db_list:
        db.delete(db_list)
        db.commit()
        return True
    return False
