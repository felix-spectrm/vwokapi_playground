from typing import Any, Self

from attrs import define

from vwok_client.http import DEFAULT_BASE_URL, HttpClient
from vwok_client.models import (
    BaseConfiguration,
    CheckResponse,
    Choice,
    Configuration,
    DataResponse,
    MarketingCodeConfiguration,
    Model,
    TypeModel,
    TypeWithOptions,
    parse_response,
)


@define
class VwokClient:
    http: HttpClient

    @classmethod
    def from_credentials(
        cls,
        client_id: str,
        client_secret: str,
        base_url: str = DEFAULT_BASE_URL,
    ) -> Self:
        return cls(HttpClient(client_id, client_secret, base_url))

    def close(self) -> None:
        self.http.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_exc: object) -> None:
        self.close()

    def _call[T](
        self,
        method: str,
        path: str,
        response_type: type[T],
        payload: Configuration | None = None,
        **params: Any,
    ) -> T:
        raw = self.http.request(
            method,
            path,
            params=params,
            json=payload.to_body() if payload else None,
        )
        # An empty body (e.g. 204) parses as an empty response.
        return parse_response(response_type, {} if raw is None else raw)

    # Catalog

    def list_models(
        self,
        country_code: str,
        brand: str,
        *,
        language_code: str | None = None,
        product_data_key: str | None = None,
    ) -> DataResponse[Model]:
        return self._call(
            "GET",
            f"/v3/catalog/{country_code}/brands/{brand}/models",
            DataResponse[Model],
            language_code=language_code,
            product_data_key=product_data_key,
        )

    def get_base_configuration(
        self,
        country_code: str,
        brand: str,
        type_code: str,
        *,
        language_code: str | None = None,
        product_data_key: str | None = None,
    ) -> DataResponse[BaseConfiguration]:
        return self._call(
            "GET",
            f"/v3/catalog/{country_code}/brands/{brand}/types/{type_code}/base_configuration",
            DataResponse[BaseConfiguration],
            language_code=language_code,
            product_data_key=product_data_key,
        )

    def list_types(
        self,
        country_code: str,
        model: str,
        *,
        fetch_wltp_span: bool | None = None,
        language_code: str | None = None,
        product_data_key: str | None = None,
    ) -> DataResponse[TypeModel]:
        return self._call(
            "GET",
            f"/v3/catalog/{country_code}/models/{model}/types",
            DataResponse[TypeModel],
            fetch_wltp_span=fetch_wltp_span,
            language_code=language_code,
            product_data_key=product_data_key,
        )

    def get_type_options(
        self,
        country_code: str,
        type_code: str,
        *,
        language_code: str | None = None,
        product_data_key: str | None = None,
    ) -> DataResponse[TypeWithOptions]:
        return self._call(
            "GET",
            f"/v3/catalog/{country_code}/types/{type_code}/options",
            DataResponse[TypeWithOptions],
            language_code=language_code,
            product_data_key=product_data_key,
        )

    # Operation

    def configure(
        self,
        country_code: str,
        payload: Configuration,
        *,
        categories: str | None = None,
        with_add_dependencies: bool | None = None,
        with_remove_dependencies: bool | None = None,
        language_code: str | None = None,
        product_data_key: str | None = None,
    ) -> DataResponse[Choice]:
        return self._call(
            "POST",
            f"/v3/operation/{country_code}/configure",
            DataResponse[Choice],
            payload,
            categories=categories,
            with_add_dependencies=with_add_dependencies,
            with_remove_dependencies=with_remove_dependencies,
            language_code=language_code,
            product_data_key=product_data_key,
        )

    def check(
        self,
        country_code: str,
        payload: Configuration,
        *,
        complete: bool | None = None,
        language_code: str | None = None,
        product_data_key: str | None = None,
    ) -> CheckResponse:
        return self._call(
            "POST",
            f"/v3/operation/{country_code}/check",
            CheckResponse,
            payload,
            complete=complete,
            language_code=language_code,
            product_data_key=product_data_key,
        )

    def create_marketing_code(
        self,
        country_code: str,
        payload: Configuration,
        *,
        time_to_live: str | None = None,
        language_code: str | None = None,
        product_data_key: str | None = None,
    ) -> MarketingCodeConfiguration:
        return self._call(
            "POST",
            f"/v3/operation/{country_code}/marketing_code",
            MarketingCodeConfiguration,
            payload,
            time_to_live=time_to_live,
            language_code=language_code,
            product_data_key=product_data_key,
        )
