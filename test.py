import structlog


class CustomLogger:
    def __init__(self, client_id, service_name):
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.set_exc_info,
                structlog.processors.TimeStamper(
                    fmt="%Y-%m-%d %H:%M:%S", utc=False),
                structlog.dev.ConsoleRenderer()
            ],
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=False
        )

        self.logger = structlog.get_logger().bind(
            client_id=client_id, service_name=service_name)

    def info(self, message):
        self.logger.info(message)

log = CustomLogger('admin', 'mimir@manager')
log.info("aqui")
