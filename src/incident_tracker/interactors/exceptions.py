from incident_tracker.common.exceptions.base import BaseDetailException


class NewIncidentException(BaseDetailException):
    pass


class ListIncidentException(BaseDetailException):
    pass


class ChangeIncidentStatusException(BaseDetailException):
    pass


class NewServiceException(BaseDetailException):
    pass
