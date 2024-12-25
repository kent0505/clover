from src.routers import *

router = APIRouter()

class _Body(BaseModel):
    title: str

# @router.get("/", dependencies=[Depends(JWTBearer(role="user"))])
@router.get("/")
async def get_tests(db: AsyncSession = Depends(db_helper.get_db)):
    tests = await db.scalars(select(Test))
    return {"tests": [
        {
            "id":    test.id,
            "title": test.title,
        } 
        for test in tests
    ]}

@router.post("/")
async def add_test(body: _Body, db: AsyncSession = Depends(db_helper.get_db)):
    db.add(Test(title=body.title))
    await db.commit()
    return {"message": "test added"}

@router.put("/{id}")
async def edit_test(id: int, body: _Body, db: AsyncSession = Depends(db_helper.get_db)):
    test = await db.scalar(select(Test).filter(Test.id == id))
    if test:
        test.title = body.title
        await db.commit()
        return {"message": "test updated"}
    raise HTTPException(404, "id not found")

@router.delete("/{id}")
async def delete_test(id: int, db: AsyncSession = Depends(db_helper.get_db)):
    test = await db.scalar(select(Test).filter(Test.id == id))
    if test:
        await db.delete(test)
        await db.commit()
        return {"message": "test deleted"}
    raise HTTPException(404, "id not found")
