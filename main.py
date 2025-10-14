"""Entry point"""
from src.app import App
from src.core.logger.logger import setup_logger

IS_DEV = True
logger = setup_logger(log_to_console=IS_DEV)

def main():
    """Main function"""
    logger.info("Application started")
    try:
        app = App()
        app.run()
    except RuntimeError as e:
        logger.exception("Critical error in main loop: %s", e)


if __name__ == '__main__':
    main()
