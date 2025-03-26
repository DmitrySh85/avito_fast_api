from pydantic import BaseModel


class AvitoReview(BaseModel):
    id: int
    score: int
    stage: str
    text: str
    usedInScore: bool
    canAnswer: bool
    createdAt: int


class AvitoReviewResponse(BaseModel):
    total: int
    reviews: list[AvitoReview]