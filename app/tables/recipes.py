"""Модуль табличек для работы с рецептами."""
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.tables.base import Base


class Component(Base):
    """Табличка Компонентов."""

    __tablename__ = "components"
    id = sa.Column(
        "id", sa.Integer, primary_key=True, index=True, autoincrement=True
    )
    ingredient_id = sa.Column(
        sa.Integer, sa.ForeignKey("ingredients.id", ondelete="CASCADE")
    )
    ingredient = relationship(
        "Ingredient", backref=("component"), lazy="joined"
    )
    amount = sa.Column("amount", sa.SmallInteger())
    recipe_id = sa.Column(
        "recipe_id",
        sa.Integer,
        sa.ForeignKey("recipes.id", ondelete="CASCADE"),
    )

    def __repr__(self) -> str:
        """Стринговое отображение объекта."""
        return (
            f"{self.ingredient.name}"
            f" {self.amount} {self.ingredient.measurement_unit}"
        )


class Ingredient(Base):
    """Табличка Ингредиентов."""

    __tablename__ = "ingredients"
    id = sa.Column(
        "id", sa.Integer, primary_key=True, index=True, autoincrement=True
    )
    name = sa.Column("name", sa.String(200))
    measurement_unit = sa.Column("measurement_unit", sa.String(200))
    __table_args__ = (
        sa.UniqueConstraint(
            "name", "measurement_unit", name="name_measurement_unit_uc"
        ),
    )

    def __repr__(self) -> str:
        """Стринговое отображение объекта."""
        return self.name


recipe_component = sa.Table(
    "recipe_component",
    Base.metadata,
    sa.Column(
        "recipe_id",
        sa.Integer,
        sa.ForeignKey("recipes.id", ondelete="CASCADE"),
    ),
    sa.Column(
        "component_id",
        sa.Integer,
        sa.ForeignKey("components.id", ondelete="CASCADE"),
    ),
)


class Recipes(Base):
    """Модель рецептов."""

    __tablename__ = "recipes"
    id = sa.Column(
        "id", sa.Integer, primary_key=True, index=True, autoincrement=True
    )
    name = sa.Column("name", sa.String(200), nullable=False)
    description = sa.Column("description", sa.TEXT())
    ingredients = relationship("Component", secondary=recipe_component)
    cooking_time = sa.Column(sa.SmallInteger())

    def __repr__(self) -> str:
        """Стринговое отображение объекта."""
        return f"<Recipes {self.name}>"
