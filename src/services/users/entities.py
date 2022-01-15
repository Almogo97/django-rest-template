"""
Using another file allows the IDE to recognize the type 
of the fields defined in models.pyi, this does not happen
when inside the models.py file

I think it may also prove useful to define the logic in
a separate place and not inside the model. Or not, what 
do I know, just testing the waters.
"""

from .models import UserModel


class User(UserModel):
    class Meta:
        proxy = True
