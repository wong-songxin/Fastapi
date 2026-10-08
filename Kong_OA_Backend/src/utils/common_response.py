# pip3 install orjson
from typing import Optional, Any, Tuple, List
from fastapi import status
from fastapi.responses import ORJSONResponse as JSONResponse  # 内部使用orjson，性能更改，但是需要安装
import math

class APIResponse(JSONResponse):
    def __init__(self, code: int = 100, msg: Optional[str] = '成功', status_code: int = status.HTTP_200_OK,
                 **kwargs) -> None:
        self.data = {
            'code': code,
            'msg': msg
        }
        self.data.update(kwargs)
        super().__init__(content=self.data, status_code=status_code)


# 分页的
class PaginationResponse(JSONResponse):
    def __init__(
            self,
            data: List[Any] = [], # 要返回给前端的数据
            msg: Optional[str] = "查询成功",
            code: int = 100,  # 状态码
            page: int = 1,
            page_size: int = 10,
            status_code: int = status.HTTP_200_OK # http响应状态码
    ):
        if page < 1 or page_size < 1:
            raise

        total, results = self.get_paginated_response(data, page, page_size)
        has_next = True if math.ceil(total / page_size) > page else False
        self.data = {
            "code": code,
            "msg": msg,
            "total": total,
            "page": page,
            "page_size": page_size,
            "has_next": has_next,
            "results": results,
        }
        super().__init__(content=self.data, status_code=status_code)


    @staticmethod
    def get_paginated_response(data,page,page_size):
        # 计算起始索引和结束索引
        start = (page - 1) * page_size
        end = page * page_size
        paginated_data = data[start:end]
        return len(data), paginated_data