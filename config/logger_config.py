import logging

def setup_logger():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filename='project.log',
                        filemode='a')
