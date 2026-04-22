from fastapi import APIRouter, status, Depends, HTTPException
# from fastapi.security import HTTPBearer
from sqlalchemy import select
from auth.jwt import verify_user
from database.connection import get_session
from user.models import HealthProfile
from prediction.llm import predict_health_risk
from prediction.models import HealthRiskPrediction


# 새로운 카테고리 추가
router = APIRouter(tags=["Prediction"])

@router.post(
    "/predictions",
    summary="당뇨병/고혈압 위험도 예측 API",
    status_code=status.HTTP_201_CREATED,
)

async def predict_health_risk_handler(
    # 인증 토큰 요구. 이거 넣으면 인증이(토큰 요구) 필요한 자물쇠 생김
    user_id = Depends(verify_user),
    session = Depends(get_session)
):
    
    # 1) 건강 프로필 조회
    stmt = (
        select(HealthProfile)
        .where(HealthProfile.user_id == user_id)
    )

    result = await session.execute(stmt)
    profile = result.scalar()
    if not profile:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail="건강 프로필이 없습니다."
        )
    # 2) 위험도 예측
    model_version = "gpt-5-mini"
    risk_prediction = await predict_health_risk(
        profile=profile, model_version = model_version
    )

    
    # 3) 결과물 저장
    new_prediction = HealthRiskPrediction(
        user_id=user_id,
        diabetes_propability=risk_prediction.diabetes_propability,
        hypertension_propability=risk_prediction.hypertension_propability,
        model_version=model_version
    )

    session.add(new_prediction)
    await session.commit()
    await session.refresh(new_prediction)
    
    return risk_prediction