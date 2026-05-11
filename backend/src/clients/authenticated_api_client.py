import json
from dataclasses import dataclass
from http.cookiejar import CookieJar
from typing import Any
from urllib import error, parse, request


class APIClientError(Exception):
    pass


@dataclass(slots=True)
class AuthTokens:
    access_token: str | None = None


class AuthenticatedAPIClient:
    def __init__(
        self,
        base_url: str,
        auth_prefix: str = "/auth/api/v1",
        timeout: float = 10.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.auth_prefix = auth_prefix.rstrip("/")
        self.timeout = timeout
        self.tokens = AuthTokens()

        self.cookie_jar = CookieJar()
        self.opener = request.build_opener(request.HTTPCookieProcessor(self.cookie_jar))

    def login(self, email: str, password: str) -> dict[str, Any]:
        payload = parse.urlencode(
            {
                "username": email,
                "password": password,
            }
        ).encode()

        response = self._send(
            path=f"{self.auth_prefix}/login",
            method="POST",
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            use_auth=False,
        )
        self.tokens.access_token = response["access_token"]
        return response

    def refresh(self) -> dict[str, Any]:
        response = self._send(
            path=f"{self.auth_prefix}/refresh",
            method="POST",
            use_auth=False,
        )
        self.tokens.access_token = response["access_token"]
        return response

    def logout(self) -> None:
        self._send(
            path=f"{self.auth_prefix}/logout",
            method="POST",
            expected_statuses={204},
        )
        self.tokens.access_token = None
        self.cookie_jar.clear()

    def check_auth(self) -> dict[str, Any]:
        return self._send(
            path=f"{self.auth_prefix}/check",
            method="GET",
        )

    def get(self, path: str) -> dict[str, Any]:
        return self._send(path=path, method="GET")

    def post(self, path: str, json_body: dict[str, Any] | None = None) -> dict[str, Any]:
        data = json.dumps(json_body).encode() if json_body is not None else None
        headers = {"Content-Type": "application/json"} if json_body is not None else None
        return self._send(path=path, method="POST", data=data, headers=headers)

    def patch(self, path: str, json_body: dict[str, Any] | None = None) -> dict[str, Any]:
        data = json.dumps(json_body).encode() if json_body is not None else None
        headers = {"Content-Type": "application/json"} if json_body is not None else None
        return self._send(path=path, method="PATCH", data=data, headers=headers)

    def delete(self, path: str) -> dict[str, Any] | None:
        return self._send(path=path, method="DELETE", expected_statuses={200, 204})

    def _send(
        self,
        path: str,
        method: str,
        data: bytes | None = None,
        headers: dict[str, str] | None = None,
        use_auth: bool = True,
        retry_on_401: bool = True,
        expected_statuses: set[int] | None = None,
    ) -> dict[str, Any] | None:
        req_headers = dict(headers or {})
        if use_auth and self.tokens.access_token:
            req_headers["Authorization"] = f"Bearer {self.tokens.access_token}"

        req = request.Request(
            url=self._build_url(path),
            data=data,
            headers=req_headers,
            method=method,
        )

        try:
            with self.opener.open(req, timeout=self.timeout) as response:
                body = response.read()
                if expected_statuses and response.status not in expected_statuses:
                    raise APIClientError(f"Unexpected status code: {response.status}")
                if not body:
                    return None
                return json.loads(body.decode())
        except error.HTTPError as exc:
            if exc.code == 401 and retry_on_401 and path != f"{self.auth_prefix}/refresh":
                self.refresh()
                return self._send(
                    path=path,
                    method=method,
                    data=data,
                    headers=headers,
                    use_auth=use_auth,
                    retry_on_401=False,
                    expected_statuses=expected_statuses,
                )

            error_body = exc.read().decode(errors="ignore")
            raise APIClientError(
                f"Request failed with status {exc.code}: {error_body or exc.reason}"
            ) from exc
        except error.URLError as exc:
            raise APIClientError(f"Failed to connect to API: {exc.reason}") from exc

    def _build_url(self, path: str) -> str:
        if path.startswith("http://") or path.startswith("https://"):
            return path
        if not path.startswith("/"):
            path = f"/{path}"
        return f"{self.base_url}{path}"
