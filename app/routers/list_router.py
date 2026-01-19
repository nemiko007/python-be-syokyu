from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.list_schema import NewTodoList, UpdateTodoList, ResponseTodoList
from app.crud import list_crud

router = APIRouter(prefix="/lists", tags=["Todo Lists"])

@router.get("/", response_model=list[ResponseTodoList])
@router.get("", response_model=list[ResponseTodoList], include_in_schema=False)
def read_todo_lists(per_page: int | None = None, page: int | None = None, db: Session = Depends(get_db)):
    return list_crud.get_todo_lists(db, per_page=per_page, page=page)

@router.get("/{todo_list_id}", response_model=ResponseTodoList)
def read_todo_list(todo_list_id: int, db: Session = Depends(get_db)):
    db_list = list_crud.get_todo_list(db, list_id=todo_list_id)
    if db_list is None:
        raise HTTPException(status_code=404, detail="Todo list not found")
    return db_list

@router.post("/", response_model=ResponseTodoList)
@router.post("", response_model=ResponseTodoList, include_in_schema=False)
def create_todo_list(todo_list: NewTodoList, db: Session = Depends(get_db)):
    return list_crud.create_todo_list(db, todo_list=todo_list)

@router.put("/{todo_list_id}", response_model=ResponseTodoList)
def update_todo_list(todo_list_id: int, todo_list: UpdateTodoList, db: Session = Depends(get_db)):
    db_list = list_crud.update_todo_list(db, list_id=todo_list_id, todo_list=todo_list)
    if db_list is None:
        raise HTTPException(status_code=404, detail="Todo list not found")
    return db_list

@router.delete("/{todo_list_id}")
def delete_todo_list(todo_list_id: int, db: Session = Depends(get_db)):
    success = list_crud.delete_todo_list(db, list_id=todo_list_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo list not found")
    return {}
