class CurrentUserMixin:
    @property
    def current_user(self):
        request = self.context.get("request", None)
        if request:
            return request.user
        return None
