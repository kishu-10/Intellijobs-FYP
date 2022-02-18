from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator


# function to validate size and extension of file
def validate_file(fieldfile_obj):
    valid_file_extensions = ['doc', 'docx', 'docm', 'pdf', 'odt']
    filesize = fieldfile_obj.size  # filesize in bytes
    kilobyte_limit = 500
    if filesize > kilobyte_limit * 1024:
        raise ValidationError(_("Max file size is %sKB" % str(kilobyte_limit)))
    filename = fieldfile_obj.name
    file_extension = filename.split('.')[1]
    if file_extension in valid_file_extensions:
        pass
    else:
        raise ValidationError(_("Please upload pdf/doc file only"))


class MobileNumberValidator(RegexValidator):
    regex = '^(\+*977[- ]?)?\d{10}$'
    message = (
        'Invalid Mobile Number. Eg.: +977-1234567890/+977 1234567890/977 1234567890/977-1234567890/9874563201')
