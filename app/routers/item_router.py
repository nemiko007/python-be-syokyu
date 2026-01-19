from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.item_schema import NewTodoItem, UpdateTodoItem, ResponseTodoItem
from app.crud import item_crud, list_crud

router = APIRouter(prefix="/lists/{todo_list_id}/items", tags=["Todo Items"])

@router.get("/", response_model=list[ResponseTodoItem])
@router.get("", response_model=list[ResponseTodoItem], include_in_schema=False)
def read_todo_items(todo_list_id: int, per_page: int | None = None, page: int | None = None, db: Session = Depends(get_db)):
    db_list = list_crud.get_todo_list(db, list_id=todo_list_id)
    if db_list is None:
        raise HTTPException(status_code=404, detail="Todo list not found")
    return item_crud.get_todo_items(db, list_id=todo_list_id, per_page=per_page, page=page)

@router.get("/{todo_item_id}", response_model=ResponseTodoItem)
def read_todo_item(todo_list_id: int, todo_item_id: int, db: Session = Depends(get_db)):
    db_item = item_crud.get_todo_item(db, list_id=todo_list_id, item_id=todo_item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Todo item not found")
    return db_item

@router.post("/", response_model=ResponseTodoItem)
@router.post("", response_model=ResponseTodoItem, include_in_schema=False)
def create_todo_item(todo_list_id: int, todo_item: NewTodoItem, db: Session = Depends(get_db)):
    db_list = list_crud.get_todo_list(db, list_id=todo_list_id)
    if db_list is None:
        raise HTTPException(status_code=404, detail="Todo list not found")
    return item_crud.create_todo_item(db, list_id=todo_list_id, todo_item=todo_item)

@router.put("/{todo_item_id}", response_model=ResponseTodoItem)
def update_todo_item(todo_list_id: int, todo_item_id: int, todo_item: UpdateTodoItem, db: Session = Depends(get_db)):
    db_item = item_crud.update_todo_item(db, list_id=todo_list_id, item_id=todo_item_id, todo_item=todo_item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Todo item not found")
    return db_item

@router.delete("/{todo_item_id}")
def delete_todo_item(todo_list_id: int, todo_item_id: int, db: Session = Depends(get_db)):
    success = item_crud.delete_todo_item(db, list_id=todo_list_id, item_id=todo_item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo item not found")
    return {}
