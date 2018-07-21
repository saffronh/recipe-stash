from registration.backends.simple.views import RegistrationView

# overriding so after registration we go to create recipe page.
class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        #url we want to redirect to
        return('registration_create_recipe')
