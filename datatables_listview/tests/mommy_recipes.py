from datetime import date
from model_mommy.recipe import Recipe, foreign_key, related, seq
from tests.models import TestCat, TestDog, TestPerson

# Here we define the model_mommy recipes for more semantic tests
# For more info go to: http://model-mommy.readthedocs.io/en/latest/recipes.html

test_dog = Recipe(
    TestDog,
    name=seq("Dog"),
    age=seq(1)
)

test_cat = Recipe(
    TestCat,
    name=seq("Cat"),
    hate_level=seq(1)
)

test_person = Recipe(
    TestPerson,
    name=seq("Name"),
    birth_date=date.today(),
    dog=foreign_key(test_dog),
    cats=related(test_cat, test_cat, test_cat)
)
