
import logging
#logger = None # st the logger to none
#Logging
#capturing the config level logging from the enviroment if not there then capturing info
#circular dependenies
def setup_logging(app):
    numeric_level = getattr(logging, app.config['LOG_LEVEL'].upper(), logging.INFO)
    logging.basicConfig(
        format='[%(asctime)s] %(levelname)s: %(message)s',
        level=numeric_level,
        filename='dashboard.log',
        encoding='utf-8'
    )
#Add logging to console also
    console_handler = logging.StreamHandler()
    console_handler.setLevel(numeric_level)
    logging.getLogger().addHandler(console_handler)
#Configure Flask logging to the same level
    app.logger.setLevel(numeric_level)

logger = logging.getLogger()