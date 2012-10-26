# encoding: utf-8
from django.forms import ValidationError
from django.forms.fields import CharField, RegexField
from django.utils.translation import ugettext_lazy as _

from .validators import validate_identity_code

class LVPhoneField(RegexField):

    default_error_messages = {
        'invalid': _('Phone numbers must be in XXXXXXXX format.'),
    }
    def __init__(self, *args, **kwargs):
        super(LVPhoneField, self).__init__(r'^(\d{8})$',
            max_length=None, min_length=None, *args, **kwargs)

class LVPostalCodeField(RegexField):
    default_error_messages = {
        'invalid' : _('Postal code fields must be in LV-XXXX format')
    }
    def __init__(self, *args, **kwargs):
        super(LVPostalCodeField, self).__init__(r'LV-(\d{4})$',
                max_length = None, min_length = None, *args, **kwargs)

class LVIdentityNumberField(CharField):
    """
        Latvian identity number field.
        see `.validators.validate_identity_code` for validation
    """
    default_error_messages = {
        'invalid':  _('Identity numbers must be in XXXXXX-XXXXX format')
    }
    validators = [validate_identity_code, ]
