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

        # 👉 统一清洗（去空格、-、括号）
        cleaned = re.sub(r"[ \-\(\)]", "", q_)

        # 国内手机号
        cn_phone_pattern = r"^1\d{10}$"

        # 国际手机号（E.164）
        intl_phone_pattern = r"^\+\d{6,15}$"

        phone_pattern = rf"(?:{cn_phone_pattern})|(?:{intl_phone_pattern})"

        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        # 中国大陆身份证
        mainland_id_pattern = r"^\d{17}[\dXx]$"

        # 台湾身份证（ROC ID）
        taiwan_id_pattern = r"^[A-Z][12]\d{8}$"

        # 合并
        id_pattern = rf"(?:{mainland_id_pattern})|(?:{taiwan_id_pattern})"

        # 👉 QQ：排除所有电话格式
        qq_pattern = rf"^(?!{phone_pattern}$)\d{{5,11}}$"

        # 校验是否至少符合一种
        if not (re.fullmatch(phone_pattern, q_) or
                re.fullmatch(email_pattern, q_) or
                re.fullmatch(id_pattern, q_) or
                re.fullmatch(qq_pattern, q_)):
            raise ValueError("q 必须是身份证号 | 手机号 | 邮箱 | QQ 号之一")

        return values