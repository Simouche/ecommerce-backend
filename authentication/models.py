from base_backend.models import User as bUser, Profile as bProfile, Region as bRegion, State as bState, City as bCity, \
    PasswordReset as bPasswordReset, SmsVerification as bSmsVerification


# Create your models here.

class User(bUser):

    def __str__(self):
        return self.username


class Profile(bProfile):
    OWNER_FIELD = 'get_owner'

    @property
    def get_owner(self):
        return self.user

    def __str__(self):
        return self.user.full_name


class Region(bRegion):
    def __str__(self):
        return self.name


class State(bState):
    def __str__(self):
        return self.name


class City(bCity):
    def __str__(self):
        return self.name


class PasswordReset(bPasswordReset):
    pass


class SmsVerification(bSmsVerification):
    pass
