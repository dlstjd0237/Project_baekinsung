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

    def __init__(self, host: str = "localhost", port: int = 9911, path: str = "/clinet", auto_connect: bool = True):
        self._ws = IMouseWebSocket(host=host, port=port, path=path)
        if auto_connect:
            self._ws.connect()
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


    # API Methods
    def get_device_list(self) -> dict:
        return self._ws.call(DefineCommand.GET_DEVICE_LIST, {})

    def get_devicemodel_list(self) -> dict:
        return self._ws.call(DefineCommand.GET_DEVICEMODEL_LIST, {})

    def restart_device(self, deviceid: str) -> dict:
        return self._ws.call(DefineCommand.RESTART_DEVICE, {"deviceid": deviceid})

    def save_restart_point(self, deviceid: str, **fields: Any) -> dict:
        return self._ws.call(DefineCommand.SAVE_RESTART_POINT, {"deviceid": deviceid, **fields})

    def restart(self) -> dict:
        return self._ws.call(DefineCommand.RESTART, {})

    # ---------- USB ----------
    def get_usb_list(self) -> dict:
        return self._ws.call(DefineCommand.GET_USB_LIST, {})

    def restart_usb(self, deviceid: str) -> dict:
        return self._ws.call(DefineCommand.RESTART_USB, {"deviceid": deviceid})

    def click(self, deviceid: str, x: float, y: float, button: int = 1,time_ms: int = 0) -> dict:
        return self._ws.call(DefineCommand.CLICK,{"deviceid": deviceid, "button": button, "x": x, "y": y, "time": time_ms})

    def swipe(self,deviceid: str, direction: Optional[str] = None,  length: Optional[float] = None, 
              start_pos_x: Optional[float] = None,start_pos_y: Optional[float] = None,
              end_pos_x: Optional[float] = None,end_pos_y: Optional[float] = None,
            time_ms: int = 0,) -> dict:
        data: dict[str, Any] = {"deviceid": deviceid, "time": time_ms}
        if direction is not None: 
            data["direction"] = direction
        if length is not None:
            data["len"] = length
        if start_pos_x is not None:
            data["sx"] = start_pos_x
        if start_pos_y is not None:
            data["sy"] = start_pos_y
        if end_pos_x is not None:
            data["ex"] = end_pos_x
        if end_pos_y is not None:
            data["ey"] = end_pos_y
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

    def get_device_screenshot(self, deviceid: str, **fields: Any) -> dict:
        return self._ws.call(
            DefineCommand.GET_DEVICE_SCREENSHOT, {"deviceid": deviceid, **fields}
        )

    def loop_device_screenshot(self, deviceid: str, **fields: Any) -> dict:
        return self._ws.call(
            DefineCommand.LOOP_DEVICE_SCREENSHOT, {"deviceid": deviceid, **fields}
        )

    def shortcut(self, deviceid: str, **fields: Any) -> dict:
        return self._ws.call(
            DefineCommand.SHORTCUT, {"deviceid": deviceid, **fields}
        )
