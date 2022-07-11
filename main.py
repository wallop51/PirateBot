import logging
import logging.config

if __name__ == "__main__":
    # load the logging configuration
    debug = True
    logging_config_file = ('logging.conf' if not debug else 'logging_debug.conf')
    logging.config.fileConfig(
        fname=logging_config_file,
        disable_existing_loggers=False,
    )

    # start the app
    import pirategame
    app = pirategame.App()
    app.start_client()