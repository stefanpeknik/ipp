import sys


class ErrorHandler:
    @staticmethod
    def err_exit(exit_code: int, e: Exception):
        print(e, file=sys.stderr)
        sys.exit(exit_code)
