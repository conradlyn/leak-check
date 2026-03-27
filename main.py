import re
from typing import Sequence

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import PlainTextResponse

from db import crud
from db.crud import SessionDep
from models.database import Person
from models.request import ModelRequestQuery
from models.response import ModelResponsePersonAggregated

app = FastAPI(
    root_path="/person",
    title="api-dig.garinasset.com",
    version="1.0.0",
    summary="个人信息 “泄漏” 查询接口",
    contact={
        "name": "嘉林数据",
        "url": "https://person.garinasset.com",
        "email": "contact@garinasset.com",
    },
    license_info={
        "name": "CC BY 4.0",
        "identifier": "CC-BY-4.0",
    }
)

# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("", summary="Hello person! 🚀 https://person.garinasset.com",
         response_class=PlainTextResponse,
         responses={
             200: {
                 "content": {
                     "text/plain": {
                         "example": "Hello person!\n"
                     }
                 }
             }
         }
         )
async def root():
    return f"Hello person!\n"


@app.get("/", summary="响应 数据库 记录",
         response_class=PlainTextResponse,
         responses={
             200: {
                 "content": {
                     "text/plain": {
                         "example": "0\n"
                     }
                 }
             }
         }
         )
async def get_counts(session: SessionDep):
    counts = crud.read_counts(session=session)
    return counts


# ---------- 类型识别函数 ----------
def detect_input_type(user_input: str) -> str:
    """
    返回唯一类型：
    - phone
    - qq
    - email
    - id
    - unknown
    """

    phone_pattern = r"^1\d{10}$"
    # 排除手机号的 QQ
    qq_pattern = r"^(?!1\d{10}$)\d{5,11}$"
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    id_pattern = r"^\d{17}[\dXx]$"

    if re.fullmatch(phone_pattern, user_input):
        return "phone"
    elif re.fullmatch(email_pattern, user_input):
        return "email"
    elif re.fullmatch(id_pattern, user_input):
        return "id"
    elif re.fullmatch(qq_pattern, user_input):
        return "qq"
    else:
        return "unknown"


@app.post("/dig", summary="查询 个人信息“泄漏” 记录", response_model=ModelResponsePersonAggregated)
def get_person_by_dig(body: ModelRequestQuery, session: SessionDep):
    # 定义局部变量
    persons: Sequence[Person] = []

    input_type = detect_input_type(body.q)

    match input_type:
        case "phone":
            persons = crud.read_persons_by_dig(session, phone_=body.q)
        case "qq":
            persons = crud.read_persons_by_dig(session, qq_=int(body.q))
        case "email":
            persons = crud.read_persons_by_dig(session, email_=body.q)
        case "id":
            persons = crud.read_persons_by_dig(session, id_=body.q)
        case _:
            raise ValueError(f"未知类型: {body.q}")

    # 聚合并去重
    aggregated = ModelResponsePersonAggregated(
        id=list({p.id for p in persons}),
        name=list({p.name for p in persons}),
        receiver=list({p.receiver for p in persons}),
        nickname=list({p.nickname for p in persons}),
        phone=list({p.phone for p in persons}),
        address=list({p.address for p in persons}),
        car=list({p.car for p in persons}),
        email=list({p.email for p in persons}),
        qq=list({p.qq for p in persons}),
        weibo=list({p.weibo for p in persons}),
        contact=list({p.contact for p in persons}),
        company=list({p.company for p in persons}),
        source=list({p.source_obj.source if p.source_obj else None for p in persons})
    )
    return aggregated
