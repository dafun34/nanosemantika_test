"""Модели связанные с рецептами."""
from typing import Optional

from fastapi import Form
from pydantic import BaseModel

from app.tables.recipes import Component


class IngredientSchema(BaseModel):
    """Модель отображения ингридиентов."""

    id: int
    name: str
    measurement_unit: str

    class Config:
        """Конфиг модели."""

        orm_mode = True


class ComponentSchema(BaseModel):
    """Модель отображения Компонента."""

    id: int
    name: str
    measurement_unit: str
    amount: int

    @classmethod
    def validate(cls, value: Component) -> dict:
        """Валидация ингредиента.

        Эта валидация отвечает за отображения ингридиента по foreign key
        """
        try:
            return {
                "id": value.ingredient.id,
                "name": value.ingredient.name,
                "measurement_unit": value.ingredient.measurement_unit,
                "amount": value.amount,
            }
        except AttributeError:
            return value

    class Config:
        """Конфиг модели."""

        orm_mode = True


class RecipeSchema(BaseModel):
    """Модель отображения рецепта."""

    id: int
    name: str
    ingredients: list[ComponentSchema]
    description: str
    cooking_time: int

    class Config:
        """Конфиг модели."""

        orm_mode = True


class ComponentCreateSchema(BaseModel):
    """Модель для создания компонента."""

    ingredient_id: int
    amount: int


class RecipeCreateSchema(BaseModel):
    """Пидантик модель для создания рецепта."""

    name: str
    ingredients: list[ComponentCreateSchema] = Form(...)
    description: str
    cooking_time: int


class RecipeUpdateSchema(BaseModel):
    """Пидантик модель для обновления рецепта."""

    name: Optional[str]
    ingredients: Optional[list[ComponentCreateSchema]] = Form()
    description: Optional[str]
    cooking_time: Optional[int]
