from pydantic import BaseModel, Field


class ResponseBase(BaseModel):
    success: bool
    msg: str
    data: BaseModel


class Response(ResponseBase):
    success: bool = Field(examples=[True])


class ErrorResponse(ResponseBase):
    success: bool = Field(examples=[False])


class ValidationErrorDict(BaseModel):
    loc: list[str | int]
    msg: str
    type: str


class ValidationErrorResponse(ErrorResponse):
    errors: list[ValidationErrorDict]
