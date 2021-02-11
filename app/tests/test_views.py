from datetime import datetime, timedelta
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.test import TestCase
from app.views import referred_obj_slug, get_aliases, replace_alias
from app.models import Object, Alias


class TestViews(TestCase):
    def setUp(self):
        self.object1 = Object.objects.create(name="types-slug-023xf")
        self.alias1 = Alias.objects.create(alias="useful-object",
                                           target=self.object1)

    def tearDown(self):
        self.object1.delete()
        self.alias1.delete()

    def test_referred_obj_slug_not_found(self):
        with self.assertRaises(ValidationError):
            referred_obj_slug("test-test")

    def test_referred_obj_slug_end_none(self):
        self.assertIn(self.object1.name, referred_obj_slug("useful-object"))

    def test_referred_obj_slug_end_date(self):
        self.alias1.to_end_alias()
        result = referred_obj_slug("useful-object", datetime.now())
        self.assertIn(self.object1.name, result)

    def test_get_aliases_type_error(self):
        with self.assertRaises(TypeError):
            get_aliases(56, "10.02.2021 01:00", "11.02.2021 02:00")

    def test_get_aliases_target_exist_error(self):
        with self.assertRaises(ObjectDoesNotExist):
            get_aliases(56, self.alias1.start, self.alias1.start)

    def test_get_aliases_alias_exist_error(self):
        with self.assertRaises(ValidationError):
            get_aliases(56, self.alias1.start, self.alias1.start)

    def test_get_aliases_alias_not_active(self):
        with self.assertRaises(ValidationError):
            get_aliases(
                self.alias1.target,
                self.alias1.start - timedelta(days=1),
                self.alias1.start - timedelta(hours=1),
            )

    def test_get_aliases_alias_active(self):
        self.assertIn(
            self.alias1.alias,
            get_aliases(
                self.alias1.target,
                self.alias1.start,
                self.alias1.start + timedelta(microseconds=1),
            ),
        )

    def test_replace_alias_type_error(self):
        with self.assertRaises(TypeError):
            replace_alias(56, "10.02.2021 01:00", 57)

    def test_replace_alias_start_gte_replace_at(self):
        replace_at = (self.alias1.start - timedelta(microseconds=1)).replace(
            tzinfo=None
        )
        with self.assertRaises(ValidationError):
            replace_alias(self.alias1.id, replace_at, "not-useful-object")

    def test_referred_obj_alias_updated(self):
        replace_at = (self.alias1.start + timedelta(hours=1))\
            .replace(tzinfo=None)
        replace_alias(self.alias1.id, replace_at, "not-useful-object")
        result = Alias.objects.get(pk=self.alias1.id).end.replace(tzinfo=None)
        self.assertEqual(result, replace_at)

    def test_referred_obj_new_alias_created(self):
        replace_at = (self.alias1.start + timedelta(hours=1))\
            .replace(tzinfo=None)
        new_alias_value = "not-useful-object"
        replace_alias(self.alias1.id, replace_at, new_alias_value)
        self.assertTrue(Alias.objects.get(alias=new_alias_value))
