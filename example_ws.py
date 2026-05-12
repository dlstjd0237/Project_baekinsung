from imouse_client import Imouse


def main() -> None:
    with Imouse(host="localhost", port=9912) as im:
        print(im.get_device_list())
        deviceid = "FA:9E:10:3A:FE:E8"
        print(im.swipe(deviceid, direction="up", length=0.9))
        print(im.click(deviceid, x=200, y=400))
        # 래퍼가 없는 fun 도 raw call 로 가능
        # print(im.call("get_device_screenshot", {"deviceid": deviceid}))


if __name__ == "__main__":
    main()
