from django.db import models
import requests
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from university.models import UniversityModel


class UniversityUrlsModel(models.Model):
    university = models.ForeignKey(
        UniversityModel,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    api_url = models.URLField(max_length=500)
    student_url = models.URLField(max_length=500)
    employee_url = models.URLField(max_length=500)

    def __str__(self):
        return self.name

    @classmethod
    def fetch_and_save_from_api(cls, url: str):
        try:
            response = requests.get(
                "https://student.hemis.uz/rest/v1/public/university-list"
            )
            response.raise_for_status()
            data = response.json().get("data", [])
            print(data)

            def is_valid_url(url):
                if not url:
                    return False
                validator = URLValidator()
                try:
                    validator(url)
                    return True
                except ValidationError:
                    return False

            filtered_data = [
                item
                for item in data
                if is_valid_url(item.get("api_url"))
                and is_valid_url(item.get("student_url"))
                and is_valid_url(item.get("employee_url"))
            ]

            created, updated = 0, 0
            errors = []
            for item in filtered_data:
                try:
                    university, _ = UniversityModel.objects.get_or_create(
                        name=item["name"]
                    )
                    obj, created_flag = cls.objects.update_or_create(
                        code=item["code"],
                        defaults={
                            "api_url": item["api_url"],
                            "student_url": item["student_url"],
                            "employee_url": item["employee_url"],
                            "university": university,
                        },
                    )
                    if created_flag:
                        created += 1
                    else:
                        updated += 1
                except Exception as e:
                    errors.append({"code": item.get("code"), "error": str(e)})

            return {
                "status": "success" if not errors else "partial_success",
                "created": created,
                "updated": updated,
                "errors": errors,
            }
        except requests.RequestException as e:
            return {"status": "http_error", "error": str(e)}
        except Exception as e:
            return {"status": "unknown_error", "error": str(e)}
