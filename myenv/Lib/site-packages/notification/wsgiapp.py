def filter_factory(global_conf, **local_conf):
    from notification.service import NotificationService
    return _filter_factory(NotificationService, global_conf, local_conf)


def filter_factory_mako(global_conf, **local_conf):
    from notification.mako.service import NotificationService
    return _filter_factory(NotificationService, global_conf, local_conf)


def _filter_factory(service_factory, global_conf, local_conf):
    notification_service = service_factory(**local_conf)
    def filter(app):
        return NotificationServiceApp(app, notification_service)
    return filter


class NotificationServiceApp(object):

    def __init__(self, app, service):
        self.app = app
        self.service = service

    def __call__(self, environ, start_response):
        environ['service.NotificationService'] = self.service
        return self.app(environ, start_response)

