from django.core.exceptions import ValidationError
from django.test import TestCase
from app.models import Object, Alias


class TestModels(TestCase):
    def setUp(self):
        self.object1 = Object.objects.create(name="types-slug-023xf")
        self.alias1 = Alias.objects.create(alias="useful-object",
                                           target=self.object1)

    def tearDown(self):
        self.object1.delete()
        self.alias1.delete()

    def test_alias_object(self):
        self.assertEqual(self.alias1.target, self.object1)

    def test_alias_end_is_none(self):
        self.assertEqual(self.alias1.end, None)

    def test_alias_save_validation_error(self):
        with self.assertRaises(ValidationError):
            Alias.objects.create(alias="useful-object", target=self.object1)

    def test_alias_to_end_alias(self):
        self.alias1.to_end_alias()
        self.assertIsNotNone(self.alias1.end)

    def test_alias_save_success(self):
        self.alias1.to_end_alias()
        alias3 = Alias.objects.create(alias="useful-object",
                                      target=self.object1)
        self.assertEqual(alias3, Alias.objects.get(id=alias3.id))
