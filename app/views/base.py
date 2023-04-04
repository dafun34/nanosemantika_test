"""Модуль с базовыми представлениями."""
from fastapi import Request
from starlette.responses import Response


class BaseView:
    """Базовый класс представления."""

    request: Request
    response: Response
