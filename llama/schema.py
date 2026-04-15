from pydantic import BaseModel, Field

# 응답 형식 지정
class OpenAIResponse(BaseModel):
    result: str = Field(description="최종답변")
    confidence: float = Field(description="0~1 사이의 신뢰도")

# 신뢰도 조건 제어해서 통제 가능