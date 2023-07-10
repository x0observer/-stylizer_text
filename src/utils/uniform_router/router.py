

from sqlmodel import SQLModel
from typing import Optional



from fastapi import APIRouter, Depends, Response, Request
from typing import Any, Type, Union, TypeVar, Callable
from pydantic import Json


from sqlmodel import SQLModel as BaseModel
from .query_engine.filter_set import AsyncFilterSet, FilterSet

T = TypeVar("T", bound=BaseModel)


class UniformRouter(APIRouter):
    Model = None

    def __init__(
        self,
        Model: Type[T],
        create_route: bool = True,
        update_route: bool = True,
        delete_route: bool = True,
        get_route: bool = True,
        **kwargs: Any,
    ) -> None:
        self.Model = Model

        super().__init__(**kwargs)

        if create_route:
            self.add_api_route(f"{Model.__route__}", self.create(), methods=["POST"])
        if update_route:
            self.add_api_route(
                f"{Model.__route__}/{{id}}", self.update(), methods=["PUT"]
            )
        if delete_route:
            self.add_api_route(
                f"{Model.__route__}/{{id}}", self.delete(), methods=["DELETE"]
            )
        if get_route:
            self.add_api_route(
                f"{Model.__route__}/{{id}}",
                self.get(),
                methods=["GET"],
                response_model=Model,
                response_model_exclude_none=True,
            )

    def search(self, *args: Any, **kwargs: Any) -> Callable:
        Model = self.Model

        async def route(
            response: Response,
            uniform_filters: Json = None,
        ):
            try:
                if uniform_filters:
                    #do validation

                async_filters_engine = await AsyncFilterSet(
                    Model,
                    Model.get_store_fields(),
                    uniform_filters,
                )
                count_total = await async_filters_engine
                response.headers["X-Total-Count"] = str(count_total)
                return async_filters_engine
            except Exception as e:
                LOG.exception(f"Error when {Model.__name__} fetching: {e.__context__}")

        return route