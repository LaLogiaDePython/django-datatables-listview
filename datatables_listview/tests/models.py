from django.db import models


class TestCat(models.Model):
    """
    Author: Milton Lenis
    Date: 16 April 2017
    Model to represent a Test Dog, just for test purposes
    """
    name = models.CharField(max_length=30)
    hate_level = models.IntegerField()


class TestDog(models.Model):
    """
    Author: Milton Lenis
    Date: 16 April 2017
    Model to represent a Test Cat, just for test purposes
    """
    name = models.CharField(max_length=30)
    age = models.IntegerField()


class TestPerson(models.Model):
    """
    Author: Milton Lenis
    Date: 16 April 2017
    Model to represent a Test Person, just for test purposes
    """
    GENDERS = (
        (0, 'MALE'),
        (1, 'FEMALE')
    )
    name = models.CharField(max_length=30)
    birth_date = models.DateField(auto_now_add=True)
    gender = models.IntegerField(choices=GENDERS)
    dog = models.ForeignKey(TestDog)
    cats = models.ManyToManyField(TestCat)

