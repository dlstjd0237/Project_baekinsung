class DefineCommand:
    """
    API Doc: https://www.imouse.cc/API%E6%96%87%E6%A1%A3/
    - fun 명세는 위 API 문서 참고. 
    """

    # ---------- device ----------
    GET_DEVICE_LIST = "get_device_list"
    GET_DEVICEMODEL_LIST = "get_devicemodel_list"

    # ---------- USB / 하드웨어 ----------
    GET_USB_LIST = "get_usb_list"
    RESTART_USB = "restart_usb"

    # ---------- mouse ----------
    CLICK = "click"
    SWIPE = "swipe"
    MOUSE_MOVE = "mouse_move"
    MOUSE_DOWN = "mouse_down"
    MOUSE_UP = "mouse_up"
    MOUSE_RESET_POS = "mouse_reset_pos"
    MOUSE_WHEEL = "mouse_wheel"

    # ---------- keyboard ----------
    SEND_KEY = "send_key"
    KEY_DOWN = "key_down"
    KEY_UP = "key_up"
    KEY_RELEASE_ALL = "key_release_all"
    SEND_TEXT = "send_text"

    # ---------- screenshot / streaming ----------
    GET_DEVICE_SCREENSHOT = "get_device_screenshot"
    LOOP_DEVICE_SCREENSHOT = "loop_device_screenshot"


    # ---------- device 조작 ----------
    SAVE_RESTART_POINT = "save_restart_point"
    RESTART_DEVICE = "restart_device"
    RESTART = "restart" 

    # ---------- shortcut ----------
    SHORTCUT = "shortcut"
