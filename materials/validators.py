from urllib.parse import urlparse

from rest_framework.serializers import ValidationError


class LinkValidator:

    def __call__(self, value):
        if not value:
            return

        domain = urlparse(value).netloc.lower()

        allowed_domains = ["youtube.com", "youtu.be"]

        if not any(domain.endswith(d) for d in allowed_domains):
            raise ValidationError("Можно добавлять только ссылки с youtube.com")
