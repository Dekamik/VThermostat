class Formats:

    @staticmethod
    def on_off(on_off_condition):
        return "ON" if on_off_condition else "OFF"

    @staticmethod
    def on_off_na(on_off_condition, is_available_condition):
        return "N/A" if not is_available_condition else Formats.on_off(on_off_condition)
