from datetime import datetime

class Utils:
    @staticmethod
    def format_date():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")