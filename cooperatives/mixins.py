from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

class CustomLoginRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please log in to access this page.', extra_tags='login_required')
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs) 