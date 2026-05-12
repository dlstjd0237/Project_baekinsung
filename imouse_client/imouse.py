from typing import Any, Optional

from .define_command import DefineCommand
from .websocket_client import IMouseWebSocket


class Imouse:
    """
    iMouse API 집합체.
    내부에서 IMouseWebSocket 을 생성/소유하며, 각 API 메소드는
    인자를 dict 로 묶어서 self._ws.call(fun, data) 로 보낸다.

    참고:
      - 공식 doc(doc.some3c.com) 기준 WebSocket 은 9911/clinet, HTTP 는 9912/api.
      - 사용자 환경에 맞춰 host/port/path 를 생성자에서 자유롭게 바꿀 수 있다.
    """

    def __init__(self, host: str = "localhost", port: int = 9912, path: str = "", auto_connect: bool = True):
        self._ws = IMouseWebSocket(host=host, port=port, path=path)
        if auto_connect:
            self._ws.connect()

    # ---------- raw / lifecycle ----------
    @property
    def ws(self) -> IMouseWebSocket:
        return self._ws

    def connect(self) -> None:
        self._ws.connect()

    def close(self) -> None:
        self._ws.close()

    def call(self, fun: str, data: Optional[dict] = None, timeout: float = 10.0) -> dict:
        """래퍼 메소드가 없는 fun 도 직접 호출하고 싶을 때."""
        return self._ws.call(fun, data or {}, timeout=timeout)

    def __enter__(self):
        if not self._ws.is_connected:
            self._ws.connect()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

    # ====================================================
    # device
    # ====================================================
    def get_device_list(self) -> dict:
        return self._ws.call(DefineCommand.GET_DEVICE_LIST, {})

    def get_devicemodel_list(self) -> dict:
        return self._ws.call(DefineCommand.GET_DEVICEMODEL_LIST, {})

    def set_dev(self, deviceid: str, **fields: Any) -> dict:
        return self._ws.call(DefineCommand.SET_DEV, {"deviceid": deviceid, **fields})

    def del_dev(self, deviceid: str) -> dict:
        return self._ws.call(DefineCommand.DEL_DEV, {"deviceid": deviceid})

    def restart_device(self, deviceid: str) -> dict:
        return self._ws.call(DefineCommand.RESTART_DEVICE, {"deviceid": deviceid})

    def save_restart_point(self, deviceid: str, **fields: Any) -> dict:
        return self._ws.call(
            DefineCommand.SAVE_RESTART_POINT, {"deviceid": deviceid, **fields}
        )

    def restart(self) -> dict:
        """서버(커널) 재시작."""
        return self._ws.call(DefineCommand.RESTART, {})

    # ---------- group ----------
    def get_group_list(self) -> dict:
        return self._ws.call(DefineCommand.GET_GROUP_LIST, {})

    def set_group(self, **fields: Any) -> dict:
        return self._ws.call(DefineCommand.SET_GROUP, fields)

    def del_group(self, gid: str) -> dict:
        return self._ws.call(DefineCommand.DEL_GROUP, {"gid": gid})

    # ---------- USB / 마우스 캘리브레이션 ----------
    def get_usb_list(self) -> dict:
        return self._ws.call(DefineCommand.GET_USB_LIST, {})

    def restart_usb(self, deviceid: str) -> dict:
        return self._ws.call(DefineCommand.RESTART_USB, {"deviceid": deviceid})

    def mouse_collection_open(self, deviceid: str) -> dict:
        return self._ws.call(
            DefineCommand.MOUSE_COLLECTION_OPEN, {"deviceid": deviceid}
        )

    def mouse_collection_close(self, deviceid: str) -> dict:
        return self._ws.call(
            DefineCommand.MOUSE_COLLECTION_CLOSE, {"deviceid": deviceid}
        )

    def mouse_collection_cfg(self, deviceid: str, **fields: Any) -> dict:
        return self._ws.call(
            DefineCommand.MOUSE_COLLECTION_CFG, {"deviceid": deviceid, **fields}
        )

    def save_dev_location(self, deviceid: str, **fields: Any) -> dict:
        return self._ws.call(
            DefineCommand.SAVE_DEV_LOCATION, {"deviceid": deviceid, **fields}
        )

    def del_dev_location(self, deviceid: str, **fields: Any) -> dict:
        return self._ws.call(
            DefineCommand.DEL_DEV_LOCATION, {"deviceid": deviceid, **fields}
        )

    # ====================================================
    # mouse
    # ====================================================
    def click(
        self,
        deviceid: str,
        x: float,
        y: float,
        button: int = 1,
        time_ms: int = 0,
    ) -> dict:
        return self._ws.call(
            DefineCommand.CLICK,
            {"deviceid": deviceid, "button": button, "x": x, "y": y, "time": time_ms},
        )

    def swipe(
        self,
        deviceid: str,
        direction: Optional[str] = None,
        length: Optional[float] = None,
        sx: Optional[float] = None,
        sy: Optional[float] = None,
        ex: Optional[float] = None,
        ey: Optional[float] = None,
        time_ms: int = 0,
    ) -> dict:
        data: dict[str, Any] = {"deviceid": deviceid, "time": time_ms}
        if direction is not None:
            data["direction"] = direction
        if length is not None:
            data["len"] = length
        if sx is not None:
            data["sx"] = sx
        if sy is not None:
            data["sy"] = sy
        if ex is not None:
            data["ex"] = ex
        if ey is not None:
            data["ey"] = ey
        return self._ws.call(DefineCommand.SWIPE, data)

    def mouse_move(self, deviceid: str, x: float, y: float) -> dict:
        return self._ws.call(
            DefineCommand.MOUSE_MOVE, {"deviceid": deviceid, "x": x, "y": y}
        )

    def mouse_down(self, deviceid: str, button: int = 1) -> dict:
        return self._ws.call(
            DefineCommand.MOUSE_DOWN, {"deviceid": deviceid, "button": button}
        )

    def mouse_up(self, deviceid: str, button: int = 1) -> dict:
        return self._ws.call(
            DefineCommand.MOUSE_UP, {"deviceid": deviceid, "button": button}
        )

    def mouse_reset_pos(self, deviceid: str) -> dict:
        return self._ws.call(DefineCommand.MOUSE_RESET_POS, {"deviceid": deviceid})

    def mouse_wheel(self, deviceid: str, direction: str, length: int) -> dict:
        return self._ws.call(
            DefineCommand.MOUSE_WHEEL,
            {"deviceid": deviceid, "direction": direction, "len": length},
        )

    # ====================================================
    # keyboard
    # ====================================================
    def send_key(self, deviceid: str, key: str) -> dict:
        return self._ws.call(
            DefineCommand.SEND_KEY, {"deviceid": deviceid, "key": key}
        )

    def key_down(self, deviceid: str, key: str) -> dict:
        return self._ws.call(
            DefineCommand.KEY_DOWN, {"deviceid": deviceid, "key": key}
        )

    def key_up(self, deviceid: str, key: str) -> dict:
        return self._ws.call(
            DefineCommand.KEY_UP, {"deviceid": deviceid, "key": key}
        )

    def key_release_all(self, deviceid: str) -> dict:
        return self._ws.call(DefineCommand.KEY_RELEASE_ALL, {"deviceid": deviceid})

    def send_text(self, deviceid: str, text: str) -> dict:
        return self._ws.call(
            DefineCommand.SEND_TEXT, {"deviceid": deviceid, "text": text}
        )

    # ====================================================
    # screenshot / streaming
    # ====================================================
    def get_device_screenshot(self, deviceid: str, **fields: Any) -> dict:
        return self._ws.call(
            DefineCommand.GET_DEVICE_SCREENSHOT, {"deviceid": deviceid, **fields}
        )

    def loop_device_screenshot(self, deviceid: str, **fields: Any) -> dict:
        return self._ws.call(
            DefineCommand.LOOP_DEVICE_SCREENSHOT, {"deviceid": deviceid, **fields}
        )

    # ====================================================
    # image / OCR
    # ====================================================
    def find_image(self, deviceid: str, **fields: Any) -> dict:
        return self._ws.call(
            DefineCommand.FIND_IMAGE, {"deviceid": deviceid, **fields}
        )

    def find_image_ex(self, deviceid: str, **fields: Any) -> dict:
        return self._ws.call(
            DefineCommand.FIND_IMAGE_EX, {"deviceid": deviceid, **fields}
        )

    def ocr(self, deviceid: str, **fields: Any) -> dict:
        return self._ws.call(DefineCommand.OCR, {"deviceid": deviceid, **fields})

    def ocr_ex(self, deviceid: str, **fields: Any) -> dict:
        return self._ws.call(DefineCommand.OCR_EX, {"deviceid": deviceid, **fields})

    def find_multi_color(self, deviceid: str, **fields: Any) -> dict:
        return self._ws.call(
            DefineCommand.FIND_MULTI_COLOR, {"deviceid": deviceid, **fields}
        )

    def find_multi_color_ex(self, deviceid: str, **fields: Any) -> dict:
        return self._ws.call(
            DefineCommand.FIND_MULTI_COLOR_EX, {"deviceid": deviceid, **fields}
        )

    # ====================================================
    # airplay
    # ====================================================
    def auto_connect_screen(self, deviceid: str) -> dict:
        return self._ws.call(
            DefineCommand.AUTO_CONNECT_SCREEN, {"deviceid": deviceid}
        )

    def auto_connect_screen_all(self) -> dict:
        return self._ws.call(DefineCommand.AUTO_CONNECT_SCREEN_ALL, {})

    def discon_airplay(self, deviceid: str) -> dict:
        return self._ws.call(DefineCommand.DISCON_AIRPLAY, {"deviceid": deviceid})

    def get_airplaysrvnum(self) -> dict:
        return self._ws.call(DefineCommand.GET_AIRPLAYSRVNUM, {})

    def set_airplaysrvnum(self, num: int) -> dict:
        return self._ws.call(DefineCommand.SET_AIRPLAYSRVNUM, {"num": num})

    def get_airplay_mode(self) -> dict:
        return self._ws.call(DefineCommand.GET_AIRPLAY_MODE, {})

    def set_airplay_mode(self, mode: int) -> dict:
        return self._ws.call(DefineCommand.SET_AIRPLAY_MODE, {"mode": mode})

    def get_usb_autoairplay(self) -> dict:
        return self._ws.call(DefineCommand.GET_USB_AUTOAIRPLAY, {})

    def set_usb_autoairplay(self, enable: bool) -> dict:
        return self._ws.call(DefineCommand.SET_USB_AUTOAIRPLAY, {"enable": enable})

    def save_autoscreen_point(self, deviceid: str, **fields: Any) -> dict:
        return self._ws.call(
            DefineCommand.SAVE_AUTOSCREEN_POINT, {"deviceid": deviceid, **fields}
        )

    # ====================================================
    # shortcut
    # ====================================================
    def shortcut(self, deviceid: str, **fields: Any) -> dict:
        return self._ws.call(
            DefineCommand.SHORTCUT, {"deviceid": deviceid, **fields}
        )
