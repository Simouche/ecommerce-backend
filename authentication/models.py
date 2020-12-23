from base_backend.models import User as bUser, Profile as bProfile, Region as bRegion, State as bState, City as bCity, \
    PasswordReset as bPasswordReset, SmsVerification as bSmsVerification


# Create your models here.

class User(bUser):

    def __str__(self):
        return self.username


class Profile(bProfile):
    pass


class Region(bRegion):
    pass


class State(bState):
    pass


class City(bCity):
    pass


class PasswordReset(bPasswordReset):
    pass


class SmsVerification(bSmsVerification):
    pass
