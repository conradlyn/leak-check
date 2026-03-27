import re

from pydantic import BaseModel, Field, model_validator


class ModelRequestQuery(BaseModel):
    q: str = Field(
        ...,
        description='身份证号 | 手机号 | 邮箱 | QQ 号',
        examples=['13755661370','62152120001030291X','user@domain.com','5201314']
    )

    @model_validator(mode="before")
    @classmethod
    def validate_q(cls, values):
        q_ = values.get('q')
        if not q_ or not q_.strip():
            raise ValueError("q 不能为空")

        q_ = q_.strip()

        # 正则规则
        phone_pattern = r"^1\d{10}$"
        qq_pattern = r"^(?!1\d{10}$)\d{5,11}$"  # 排除手机号的 QQ
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        id_pattern = r"^\d{17}[\dXx]$"

        # 校验是否至少符合一种
        if not (re.fullmatch(phone_pattern, q_) or
                re.fullmatch(email_pattern, q_) or
                re.fullmatch(id_pattern, q_) or
                re.fullmatch(qq_pattern, q_)):
            raise ValueError("q 必须是身份证号 | 手机号 | 邮箱 | QQ 号之一")

        return values