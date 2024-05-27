from pydantic import BaseModel, ConfigDict

from app.api.common.dto.base_response_dto import BaseResponseDTO
from app.api.v1.product.dto.product_base import ProductBase


class ResponseUserProductList(ProductBase):
    model_config = ConfigDict(from_attributes=True, extra="allow")


class ResponseUserProductListDTO(BaseResponseDTO): ...
