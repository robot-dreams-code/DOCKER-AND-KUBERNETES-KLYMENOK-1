from fastapi import APIRouter, HTTPException
from ...models.schemas import ItemIn, ItemOut

router = APIRouter(prefix="/items", tags=["items"])

_db: list[ItemOut] = []
_counter = 0

@router.get("", response_model=list[ItemOut])
def list_items():
    return _db

@router.post("", response_model=ItemOut, status_code=201)
def create_item(payload: ItemIn):
    global _counter
    _counter += 1
    item = ItemOut(id=_counter, **payload.model_dump())
    _db.append(item)
    return item

@router.get("/{item_id}", response_model=ItemOut)
def get_item(item_id: int):
    for it in _db:
        if it.id == item_id:
            return it
    raise HTTPException(status_code=404, detail="Item not found")
