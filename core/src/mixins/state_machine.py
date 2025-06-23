from transitions import Machine


class StateMachineMixin:
    machine: Machine

    @property
    def state(self):
        return self.status

    @state.setter
    def state(self, value):
        if self.status != value:
            self.status = value

    def after_state_change(self):
        if self._commit_fn:
            self._commit_fn()
