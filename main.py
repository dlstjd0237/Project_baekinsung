import imouse
from imouse.types import MouseSwipeParams

#이건 그냥 테스트용 
def main():
    api = imouse.api(host="localhost")
    helper = imouse.helper(api)
    console = helper.console

    device_list = console.device.list_by_id()
    print(f"device list,{device_list}")


    device = helper.device("FA:9E:10:3A:FE:E8") #device id

    #screenShot
    screen_img = device.image.screenshot()
    if screen_img:
        print(f"screen image,{screen_img}")
        with open("screenshot.png", "wb") as f:
            f.write(screen_img)


    #swipe
    swipe_result = device.mouse.swipe(MouseSwipeParams(direction="up", len=0.9))
    if swipe_result:
        print(f"swipe result,{swipe_result}")
    else: 
        print("swipe failed")

    #api.mouse_swipe("FA:9E:10:3A:FE:E8", params=MouseSwipeParams(direction="up", len=0.9))
    
    
if __name__ == "__main__":
    main()