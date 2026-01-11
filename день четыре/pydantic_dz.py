from pydantic import BaseModel, Field, EmailStr, UUID4
from uuid import UUID

class City(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    people_count: int= Field(ge=1)

class User(BaseModel):
    id: UUID = UUID4
    name: str = Field(min_length=3, max_length=30)
    email: EmailStr
    password_hash: str =Field(exclude=True, min_length=1)
    age: int = Field(ge=0,le=150)
    city: City

testu = User(
    id="12312312312312312312312312312312",
    name="Timofey",
    email="timofey@mail.ru",
    password_hash="hash",
    age=20,
    city=City(name="Ekaterinburg", people_count=1000000)
)
print(testu.model_dump_json())

inj1 = {"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "email": "a@test.com", "name": "Alice", "password_hash": "qweqweqwe", "age": "ERROR", "city": {"name": "Moscow", "people_count": 15000000}}
inj2 = {"users": [
        {"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "email": "a@test.com", "name": "Alice", "password_hash": "qweqweqwe", "age": 18, "city": {"name": "Moscow", "people_count": 15000000}},
        {"id": "3fa85f64-5717-4562-b3fc-2c963f66afa7", "email": "b@test.com", "name": "Bob", "password_hash": "frefrefre", "age": 20, "city": {"name": "Spb", "people_count": 10000000}}
    ]}
# print(User.model_validate(inj1))

ans = []

for user in inj2["users"]:
    ans.append(User.model_validate(user))
print(ans)    