from pydantic import BaseModel ,Field

class TitleRecommendation(BaseModel):
    page_url:str
    current_title:str | None = None
    recommended_title:str
    reason : str

class MetaRecommendation(BaseModel):
    page_url:str
    current_meta : str |None=None
    recommended_meta:str
    reason : str

class HeadingRecommendation(BaseModel):
    page_url:str
    current_h1 : str |None=None
    recommended_h1:str
    recommended_h1:list[str] = Field(default_factory=list)
    reason : str

class InternalLinkRecommendation(BaseModel):
    page_url: str
    suggested_links: list[str] = Field(default_factory=list)
    reason: str


class ContentRecommendation(BaseModel):
    page_url: str
    current_word_count: int
    recommendation: str
    reason: str


class SEORecommendationResult(BaseModel):
    overall_summary: str
    title_recommendations: list[TitleRecommendation] = Field(default_factory=list)
    meta_recommendations: list[MetaRecommendation] = Field(default_factory=list)
    heading_recommendations: list[HeadingRecommendation] = Field(default_factory=list)
    internal_link_recommendations: list[InternalLinkRecommendation] = Field(default_factory=list)
    content_recommendations: list[ContentRecommendation] = Field(default_factory=list)
    priority_action_plan: list[str] = Field(default_factory=list)