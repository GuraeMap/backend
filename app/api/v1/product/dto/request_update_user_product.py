from pydantic import BaseModel, ConfigDict


class RequestUpdateUserProduct(BaseModel):
    model_config = ConfigDict(extra="allow")
