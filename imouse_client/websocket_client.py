import json
import logging
import threading
import itertools
from concurrent.futures import Future
from typing import Any, Dict, Optional

import websocket  # pip install websocket-client

logger = logging.getLogger(__name__)


class IMouseWebSocket:
    """
    iMouse 서버에 직접 WebSocket으로 붙는 저수준 클라이언트.

    - 메시지 포맷: {"fun": "<route>", "msgid": <int>, "data": {...}}
    - msgid 로 요청/응답을 매칭해 sync 호출처럼 동작하도록 래핑
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 9911,
        path: str = "/clinet",
        ping_interval: int = 10,
    ):
        self.url = f"ws://{host}:{port}{path}"
        self._ping_interval = ping_interval

        self._ws: Optional[websocket.WebSocketApp] = None
        self._thread: Optional[threading.Thread] = None
        self._connected = threading.Event()
        self._stopping = False

        self._msgid_iter = itertools.count(1)
        self._pending: Dict[int, Future] = {}
        self._lock = threading.Lock()

    # ---------- 연결 관리 ----------
    def connect(self, timeout: float = 5.0) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stopping = False
        self._ws = websocket.WebSocketApp(
            self.url,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
        )
        self._thread = threading.Thread(
            target=self._ws.run_forever,
            kwargs={"ping_interval": self._ping_interval},
            daemon=True,
        )
        self._thread.start()
        if not self._connected.wait(timeout):
            raise TimeoutError(f"WebSocket connect timeout: {self.url}")

    def close(self) -> None:
        self._stopping = True
        if self._ws:
            self._ws.close()
        if self._thread:
            self._thread.join(timeout=2)
        self._connected.clear()
        with self._lock:
            for fut in self._pending.values():
                if not fut.done():
                    fut.set_exception(ConnectionError("WebSocket closed"))
            self._pending.clear()

    @property
    def is_connected(self) -> bool:
        return self._connected.is_set()


    def call(self, fun: str, data: Optional[dict] = None, timeout: float = 10.0) -> dict:
        """API 한 번 호출. 응답을 dict 그대로 반환."""
        if not self.is_connected:
            raise ConnectionError("WebSocket not connected. Call connect() first.")

        msgid = next(self._msgid_iter)
        future: Future = Future()
        with self._lock:
            self._pending[msgid] = future

        payload = {"fun": fun, "msgid": msgid, "data": data or {}}
        try:
            raw = json.dumps(payload, ensure_ascii=False)
            logger.debug("REQ msgid=%d fun=%s data=%s", msgid, fun, payload["data"])
            self._ws.send(raw)
        except Exception as e:
            with self._lock:
                self._pending.pop(msgid, None)
            logger.exception("REQ msgid=%d fun=%s send failed", msgid, fun)
            raise ConnectionError(f"send failed: {e}") from e

        try:
            return future.result(timeout=timeout)
        except Exception:
            with self._lock:
                self._pending.pop(msgid, None)
            raise

    # ---------- 콜백 ----------
    def _on_open(self, _ws):
        self._connected.set()

    def _on_close(self, _ws, _status, _msg):
        self._connected.clear()
        with self._lock:
            for fut in self._pending.values():
                if not fut.done():
                    fut.set_exception(ConnectionError("WebSocket closed"))
            self._pending.clear()

    def _on_error(self, _ws, error):
        logger.error("WebSocket error: %s", error)

    def _on_message(self, _ws, message: Any):
        if isinstance(message, (bytes, bytearray)):
            logger.debug("RES binary len=%d (dropped)", len(message))
            return

        try:
            data = json.loads(message)
        except json.JSONDecodeError:
            logger.warning("RES non-JSON dropped: %r", message)
            return

        msgid = data.get("msgid")
        logger.debug(
            "RES msgid=%s fun=%s status=%s data=%s",
            msgid, data.get("fun"), data.get("status"), data.get("data"),
        )
        if isinstance(msgid, int) and msgid > 0:
            with self._lock:
                fut = self._pending.pop(msgid, None)
            if fut and not fut.done():
                fut.set_result(data)
