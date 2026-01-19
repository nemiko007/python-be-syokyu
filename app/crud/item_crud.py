from sqlalchemy.orm import Session
from app.models.item_model import ItemModel
from app.models.list_model import ListModel
from app.schemas.item_schema import NewTodoItem, UpdateTodoItem
from app.const import TodoItemStatusCode

def get_todo_items(db: Session, list_id: int, per_page: int | None = None, page: int | None = None):
    query = db.query(ItemModel).filter(ItemModel.todo_list_id == list_id)
    if per_page is not None and page is not None:
        offset = per_page * (page - 1)
        query = query.offset(offset).limit(per_page)
    return query.all()

def get_todo_item(db: Session, list_id: int, item_id: int):
    return db.query(ItemModel).filter(
        ItemModel.id == item_id,
        ItemModel.todo_list_id == list_id
    ).first()

def create_todo_item(db: Session, list_id: int, todo_item: NewTodoItem):
    db_item = ItemModel(
        todo_list_id=list_id,
        title=todo_item.title,
        description=todo_item.description,
        due_at=todo_item.due_at,
        status_code=TodoItemStatusCode.NOT_COMPLETED.value,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_todo_item(db: Session, list_id: int, item_id: int, todo_item: UpdateTodoItem):
    db_item = get_todo_item(db, list_id, item_id)
    if db_item:
        if todo_item.title is not None:
            db_item.title = todo_item.title
        if todo_item.description is not None:
            db_item.description = todo_item.description
        if todo_item.due_at is not None:
            db_item.due_at = todo_item.due_at
        if todo_item.complete is not None:
            db_item.status_code = TodoItemStatusCode.COMPLETED.value if todo_item.complete else TodoItemStatusCode.NOT_COMPLETED.value
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_todo_item(db: Session, list_id: int, item_id: int):
    db_item = get_todo_item(db, list_id, item_id)
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False
