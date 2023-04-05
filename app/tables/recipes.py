import sqlalchemy as sa

from app.tables.base import Base
from sqlalchemy.orm import relationship


class Component(Base):
    """Табличка Компонентов."""

    __tablename__ = "components"
    id = sa.Column(
        "id", sa.Integer, primary_key=True, index=True, autoincrement=True
    )
    ingredient_id = sa.Column(sa.Integer, sa.ForeignKey("ingredients.id"))
    ingredient = relationship("Ingredient", backref=("component"))
    amount = sa.Column("amount", sa.SmallInteger())

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
    sa.Column("recipe_id", sa.Integer, sa.ForeignKey("recipes.id")),
    sa.Column("component_id", sa.Integer, sa.ForeignKey("components.id")),
)


class Recipes(Base):
    """Модель рецептов."""

    __tablename__ = "recipes"
    id = sa.Column(
        "id", sa.Integer, primary_key=True, index=True, autoincrement=True
    )
    name = sa.Column("name", sa.String(200), nullable=False)
    description = sa.Column('description', sa.TEXT())
    ingredients = relationship(
        "Component", secondary=recipe_component, backref="recipes"
    )
    cooking_time = sa.Column(sa.SmallInteger())

    def __repr__(self) -> str:
        """Стринговое отображение объекта."""
        return f"<Recipes {self.name}>"
