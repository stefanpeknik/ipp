import sys


class ErrorHandler:
    @staticmethod
    def err_exit(exit_code: int, exception: Exception):
        print(exception, file=sys.stderr)
        sys.exit(exit_code)
