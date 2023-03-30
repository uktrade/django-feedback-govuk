from django.apps import AppConfig


class DjangoFeedbackGovukConfig(AppConfig):
    name = 'django_feedback_govuk'

    def ready(self):
        from .settings import DJANGO_FEEDBACK_GOVUK as defaults
        from django.conf import settings

        overrides = getattr(settings, "DJANGO_FEEDBACK_GOVUK", {})
        settings.DJANGO_FEEDBACK_GOVUK = self._deep_merge_dicts(defaults, overrides)

    def _deep_merge_dicts(self, defaults, overrides):
        """
        >>> a = { 'first' : { 'all_rows' : { 'pass' : 'dog', 'number' : '1' } } }
        >>> b = { 'first' : { 'all_rows' : { 'fail' : 'cat', 'number' : '5' } } }
        >>> merge(b, a) == { 'first' : { 'all_rows' : { 'pass' : 'dog', 'fail' : 'cat', 'number' : '5' } } }
        True
        """
        for key, value in defaults.items():
            if isinstance(value, dict):
                self._deep_merge_dicts(value, overrides.get(key, {}))
            else:
                defaults[key] = overrides.get(key, value)
        return defaults
