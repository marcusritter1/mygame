import wx

def get_current_resolution() -> tuple[int, int]:
    _ = wx.App(False)
    display = wx.Display(0)
    current_mode = display.GetCurrentMode()
    return (current_mode.w, current_mode.h)

def get_possible_resolutions() -> list[tuple[int, int]]:
    _ = wx.App(False)
    display = wx.Display(0)
    modes = display.GetModes()
    possible_resolutions = [(mode.w, mode.h) for mode in modes]
    return possible_resolutions
