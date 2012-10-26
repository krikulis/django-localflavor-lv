# encoding: utf-8
import re
import time

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

_identity_number_re = re.compile(r'^(\d{6})\-(\d{5})$')


def validate_identity_code_checksum(code):
    """
        identity code checksum algorithm:
         (1101 – (1*PK[1] + 6*PK[2] + 3*PK[3] + 7*PK[4] + 9*PK[5] + 10*PK[6] + 5*PK[7] + 8*PK[8] + 4*PK[9] + 2*PK[10])) mod 11
    """
    date_part, other_part = code.split("-")
    code = u"%s%s" % (date_part, other_part)
    magic_numbers = [1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    checksum = 0
    for i in xrange(0, 10):
        checksum += int(code[i]) * magic_numbers[i]
    checksum = (1101 - checksum) % 11
    if checksum != int(code[10]):
        raise ValidationError(_("invalid identity code"))


def validate_identity_code(value):
    """
        Validate latvian identity code.
        Identity code validation consists of:
            - identity code must be in dddddd-ddddd format (d - digit)
            - first part of identity code must be valid date in format ddmmyy
            - last digit is valid checksum
    """
    error_message = _("identity numbers must be in ddmmgg-xxxxx format")
    if not _identity_number_re.match(value):
        raise ValidationError(error_message)
    date_part, meta_part = value.split("-")
    try:
        time.strptime(date_part, "%d%m%y")
    except ValueError:
        raise ValidationError(error_message)
    validate_identity_code_checksum(value)
