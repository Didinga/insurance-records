from django.test import TestCase
from django.urls import reverse

from .models import User, Insurance, InsuranceDetail, InsuredPerson


class UserManagerTests(TestCase):
    def test_create_user_requires_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="pass1234")

    def test_create_user_requires_password(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email="a@example.com", password="")

    def test_create_user_success(self):
        user = User.objects.create_user(email="a@example.com", password="pass1234")
        self.assertEqual(user.email, "a@example.com")
        self.assertFalse(user.is_admin)
        self.assertTrue(user.check_password("pass1234"))

    def test_create_superuser_is_admin(self):
        admin = User.objects.create_superuser(email="admin@example.com", password="pass1234")
        self.assertTrue(admin.is_admin)
        self.assertTrue(admin.is_staff)

    def test_user_str(self):
        user = User.objects.create_user(email="a@example.com", password="pass1234")
        self.assertEqual(str(user), "Email: a@example.com")


class InsuredPersonModelTests(TestCase):
    def setUp(self):
        self.insurance = Insurance.objects.create(insurance_name="Health")
        self.detail = InsuranceDetail.objects.create(detail_title="Dental")

    def test_str_with_insurance_and_details(self):
        person = InsuredPerson.objects.create(
            first_name="Jan", last_name="Novak", age=30, address="Praha", insurance=self.insurance
        )
        person.detail_insurance.add(self.detail)
        self.assertIn("Jan", str(person))
        self.assertIn("Health", str(person))
        self.assertIn("Dental", str(person))

    def test_str_without_insurance_does_not_crash(self):
        # insurance is nullable (SET_NULL), __str__ must handle None gracefully
        person = InsuredPerson.objects.create(
            first_name="Eva", last_name="Svoboda", age=25, address="Brno", insurance=None
        )
        self.assertIn("None", str(person))

    def test_insurance_deletion_sets_null(self):
        person = InsuredPerson.objects.create(
            first_name="Petr", last_name="Dvorak", age=40, address="Ostrava", insurance=self.insurance
        )
        self.insurance.delete()
        person.refresh_from_db()
        self.assertIsNone(person.insurance)


class InsuredPersonIndexViewTests(TestCase):
    def setUp(self):
        self.insurance = Insurance.objects.create(insurance_name="Health")
        self.person = InsuredPerson.objects.create(
            first_name="Jan", last_name="Novak", age=30, address="Praha", insurance=self.insurance
        )

    def test_index_accessible_without_login(self):
        response = self.client.get(reverse("insured_person_index"))
        self.assertEqual(response.status_code, 200)

    def test_index_lists_person(self):
        response = self.client.get(reverse("insured_person_index"))
        self.assertContains(response, "Jan")
        self.assertContains(response, "Novak")

    def test_index_sorted_by_last_name(self):
        InsuredPerson.objects.create(first_name="Adam", last_name="Adamek", age=20, address="X", insurance=self.insurance)
        response = self.client.get(reverse("insured_person_index"))
        names = [p.last_name for p in response.context["insured_persons"]]
        self.assertEqual(names, sorted(names))


class InsuredPersonDetailViewTests(TestCase):
    def setUp(self):
        self.insurance = Insurance.objects.create(insurance_name="Health")
        self.person = InsuredPerson.objects.create(
            first_name="Jan", last_name="Novak", age=30, address="Praha", insurance=self.insurance
        )
        self.admin = User.objects.create_superuser(email="admin@example.com", password="pass1234")
        self.regular_user = User.objects.create_user(email="user@example.com", password="pass1234")

    def test_detail_accessible_without_login(self):
        response = self.client.get(reverse("insured_person_detail", args=[self.person.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Jan")

    def test_detail_invalid_pk_redirects_to_index(self):
        response = self.client.get(reverse("insured_person_detail", args=[9999]))
        self.assertRedirects(response, reverse("insured_person_index"))

    def test_non_admin_cannot_delete(self):
        self.client.login(email="user@example.com", password="pass1234")
        response = self.client.post(reverse("insured_person_detail", args=[self.person.pk]), {"delete": ""})
        self.assertRedirects(response, reverse("insured_person_index"))
        self.assertTrue(InsuredPerson.objects.filter(pk=self.person.pk).exists())

    def test_admin_can_delete(self):
        self.client.login(email="admin@example.com", password="pass1234")
        self.client.post(reverse("insured_person_detail", args=[self.person.pk]), {"delete": ""})
        self.assertFalse(InsuredPerson.objects.filter(pk=self.person.pk).exists())

    def test_admin_edit_button_redirects_to_edit_page(self):
        self.client.login(email="admin@example.com", password="pass1234")
        response = self.client.post(reverse("insured_person_detail", args=[self.person.pk]), {"edit": ""})
        self.assertRedirects(response, reverse("edit_insured_person", args=[self.person.pk]))


class CreateInsuredPersonViewTests(TestCase):
    def setUp(self):
        self.insurance = Insurance.objects.create(insurance_name="Health")
        self.admin = User.objects.create_superuser(email="admin@example.com", password="pass1234")
        self.regular_user = User.objects.create_user(email="user@example.com", password="pass1234")

    def test_requires_login(self):
        response = self.client.get(reverse("create_insured_person"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_non_admin_redirected(self):
        self.client.login(email="user@example.com", password="pass1234")
        response = self.client.get(reverse("create_insured_person"))
        self.assertRedirects(response, reverse("insured_person_index"))

    def test_admin_can_view_form(self):
        self.client.login(email="admin@example.com", password="pass1234")
        response = self.client.get(reverse("create_insured_person"))
        self.assertEqual(response.status_code, 200)

    def test_admin_can_create_person(self):
        self.client.login(email="admin@example.com", password="pass1234")
        response = self.client.post(reverse("create_insured_person"), {
            "first_name": "Nova", "last_name": "Osoba", "age": 22,
            "address": "Praha", "insurance": self.insurance.pk, "detail_insurance": [],
        })
        self.assertRedirects(response, reverse("insured_person_index"))
        self.assertTrue(InsuredPerson.objects.filter(first_name="Nova").exists())


class EditInsuredPersonViewTests(TestCase):
    def setUp(self):
        self.insurance = Insurance.objects.create(insurance_name="Health")
        self.person = InsuredPerson.objects.create(
            first_name="Jan", last_name="Novak", age=30, address="Praha", insurance=self.insurance
        )
        self.admin = User.objects.create_superuser(email="admin@example.com", password="pass1234")

    def test_edit_updates_person(self):
        self.client.login(email="admin@example.com", password="pass1234")
        response = self.client.post(reverse("edit_insured_person", args=[self.person.pk]), {
            "first_name": "Jan", "last_name": "Novotny", "age": 31,
            "address": "Praha", "insurance": self.insurance.pk, "detail_insurance": [],
        })
        self.assertRedirects(response, reverse("insured_person_detail", args=[self.person.pk]))
        self.person.refresh_from_db()
        self.assertEqual(self.person.last_name, "Novotny")

    def test_edit_invalid_form_does_not_crash(self):
        # age is required as an integer; omitting it should re-render the form, not raise NameError
        self.client.login(email="admin@example.com", password="pass1234")
        response = self.client.post(reverse("edit_insured_person", args=[self.person.pk]), {
            "first_name": "Jan", "last_name": "Novak",
            "address": "Praha", "insurance": self.insurance.pk, "detail_insurance": [],
        })
        self.assertEqual(response.status_code, 200)


class AuthFlowTests(TestCase):
    def test_register_creates_user_and_logs_in(self):
        response = self.client.post(reverse("registration"), {
            "email": "new@example.com", "password": "pass1234",
        })
        self.assertRedirects(response, reverse("insured_person_index"))
        self.assertTrue(User.objects.filter(email="new@example.com").exists())

    def test_login_success(self):
        User.objects.create_user(email="a@example.com", password="pass1234")
        response = self.client.post(reverse("login"), {"email": "a@example.com", "password": "pass1234"})
        self.assertRedirects(response, reverse("insured_person_index"))

    def test_login_wrong_password(self):
        User.objects.create_user(email="a@example.com", password="pass1234")
        response = self.client.post(reverse("login"), {"email": "a@example.com", "password": "wrong"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This account does not exist.")

    def test_logout(self):
        user = User.objects.create_user(email="a@example.com", password="pass1234")
        self.client.login(email="a@example.com", password="pass1234")
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("login"))

    def test_root_redirects_to_index(self):
        response = self.client.get("/")
        self.assertRedirects(response, reverse("insured_person_index"))
