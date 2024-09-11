import pyautogui

class OutputHandler:
    @staticmethod
    def output_to_active_window(text):
        pyautogui.write(text, interval=0.01)
        print(f"Typed: {text}")