# utils.py
import os
import sys
import win32gui
import win32con
import win32api
import platform
from plyer import notification

class_atom = None

# Windows-specific notification function
def notify_in_windows(title, message, app_name="App", app_icon=None, timeout=10):
    global class_atom

    # Only register the class if it's not already registered
    if class_atom is None:
        def wndproc(hwnd, msg, wparam, lparam):
            if msg == win32con.WM_DESTROY:
                win32api.PostQuitMessage(0)
            return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = wndproc
        wc.lpszClassName = 'NotificationClass'
        wc.hInstance = win32api.GetModuleHandle(None)
        class_atom = win32gui.RegisterClass(wc)

    hwnd = win32gui.CreateWindow(
        class_atom, "Notification", win32con.WS_OVERLAPPEDWINDOW, 
        0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, 
        0, 0, win32api.GetModuleHandle(None), None
    )

    # Load the icon, or use None if no valid icon is provided
    hicon = None
    if app_icon and os.path.exists(app_icon):
        hicon = win32gui.LoadImage(
            None, app_icon, win32con.IMAGE_ICON, 0, 0, win32con.LR_LOADFROMFILE
        )

    # Prepare the NID (Notification Icon Data) structure
    nid = (hwnd, 0, win32gui.NIF_INFO | win32gui.NIF_ICON | win32gui.NIF_TIP,
           win32con.WM_USER + 20, hicon, title, message, 200, title)

    # Display the notification
    win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)

    # Remove the notification after displaying it
    win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)

# General send_notification function
def send_notification(title, message):
    current_os = platform.system()
    icon_path = resource_path("./assets/app.ico")

    if current_os == "Windows":
        notify_in_windows(
            title=title,
            message=message,
            app_name="Voice Typer",
            app_icon=icon_path,
            timeout=10
        )
    elif current_os == "Linux":
        notification.notify(
            title=title,
            message=message,
            app_name="Voice Typer",
            app_icon=icon_path,
            timeout=10
        )
    elif current_os == "Darwin":  # macOS
        os.system(f"""
                  osascript -e 'display notification "{message}" with title "{title}"'
                  """)
    else:
        print("Platform not supported for notifications")

def resource_path(relative_path):
    """ Get the absolute path to a resource, works for development and when using PyInstaller """
    try:
        # PyInstaller stores files in a temporary folder at runtime
        base_path = sys._MEIPASS
    except AttributeError:
        # In development, use the current directory
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)