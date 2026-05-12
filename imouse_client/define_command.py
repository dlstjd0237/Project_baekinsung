class DefineCommand:
    """
    doc.some3c.com / iMouse API 의 fun 값.
    메시지 포맷: {"fun": <이 값>, "msgid": <int>, "data": {...}}
    """

    # ---------- device ----------
    SET_DEV = "set_dev"
    DEL_DEV = "del_dev"
    GET_DEVICE_LIST = "get_device_list"
    GET_DEVICEMODEL_LIST = "get_devicemodel_list"

    # ---------- group ----------
    SET_GROUP = "set_group"
    DEL_GROUP = "del_group"
    GET_GROUP_LIST = "get_group_list"

    # ---------- USB / 하드웨어 ----------
    GET_USB_LIST = "get_usb_list"
    RESTART_USB = "restart_usb"

    MOUSE_COLLECTION_OPEN = "mouse_collection_open"
    MOUSE_COLLECTION_CLOSE = "mouse_collection_close"
    MOUSE_COLLECTION_CFG = "mouse_collection_cfg"
    SAVE_DEV_LOCATION = "save_dev_location"
    DEL_DEV_LOCATION = "del_dev_location"

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

    # ---------- image / text recognition ----------
    FIND_IMAGE = "find_image"
    FIND_IMAGE_EX = "find_image_ex"
    OCR = "ocr"
    OCR_EX = "ocr_ex"
    FIND_MULTI_COLOR = "find_multi_color"
    FIND_MULTI_COLOR_EX = "find_multi_color_ex"

    # ---------- airplay ----------
    AUTO_CONNECT_SCREEN = "auto_connect_screen"
    AUTO_CONNECT_SCREEN_ALL = "auto_connect_screen_all"
    DISCON_AIRPLAY = "discon_airplay"
    GET_AIRPLAYSRVNUM = "get_airplaysrvnum"
    SET_AIRPLAYSRVNUM = "set_airplaysrvnum"
    GET_AIRPLAY_MODE = "get_airplay_mode"
    SET_AIRPLAY_MODE = "set_airplay_mode"
    GET_USB_AUTOAIRPLAY = "get_usb_autoairplay"
    SET_USB_AUTOAIRPLAY = "set_usb_autoairplay"
    SAVE_AUTOSCREEN_POINT = "save_autoscreen_point"

    # ---------- device 조작 ----------
    SAVE_RESTART_POINT = "save_restart_point"
    RESTART_DEVICE = "restart_device"
    RESTART = "restart"  # 서버(커널) 재시작

    # ---------- shortcut ----------
    SHORTCUT = "shortcut"
