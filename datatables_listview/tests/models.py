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
    test_bigautofield = models.BigAutoField()
    test_bigintegerfield = models.BigAutoField()
    test_booleanfield = models.BooleanField()
    test_datetimefield = models.DateTimeField()
    test_decimalfield = models.DecimalField(max_digits=2, decimal_places=3)
    test_durationfield = models.DurationField()
    test_emailfield = models.EmailField()
    test_filefield = models.FileField()
    test_filepathfield = models.FilePathField(path='test/files')
    test_floatfield = models.FloatField()
    test_imagefield = models.ImageField()
    test_genericipaddressfield = models.GenericIPAddressField()
    test_nullbooleanfield = models.NullBooleanField()
    test_positiveintegerfield = models.PositiveIntegerField()
    test_positivesmallintegerfield = models.PositiveSmallIntegerField()
    test_slugfield = models.SlugField()
    test_smallintegerfield = models.SmallIntegerField()
    test_textfield = models.TextField()
    test_timefield = models.TimeField()
    test_urlfield = models.URLField()
    test_uuidfield = models.UUIDField()
    dog = models.ForeignKey(TestDog)
    cats = models.ManyToManyField(TestCat)

