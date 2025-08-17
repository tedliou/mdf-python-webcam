# 導入設定檔工具
from tools.module import Config
from tools.ndi import NDI
import cv2
import time

def main():
    # 讀取設定檔
    cfg = Config()
    
    # 若沒有檔案，則建立新檔
    if cfg.is_new_file:
        cfg.set_name("Webcam Module")
        cfg.set_version("1.0.0")
        cfg.set_inputs(["camera"])
        cfg.set_input_params("camera_id", 0)
        cfg.set_outputs(["ndi"])
        cfg.set_output_params("ndi_name", "camera_ndi")

    # TODO: 取得輸入參數
    if "camera" in cfg.get_inputs():
        camera_id = cfg.get_input_params("camera_id")
    else:
        print("找不到可用的輸入方法")
        return
    
    # TODO: 取得輸出參數
    if "ndi" in cfg.get_outputs():
        ndi = NDI()
        sender = ndi.set_sender(cfg.get_output_params("ndi_name"))
    else:
        print("找不到可用的輸出方法")
        return

    # TODO: 主循環
    try:
        while True:
            # 啟動攝影機
            camera = cv2.VideoCapture(camera_id, cv2.CAP_ANY)
            if camera is None or not camera.isOpened():
                camera.release()
                print("攝影機連線失敗，將於 1 秒後重試")
                time.sleep(1)
                continue
            print("已連接攝影機")

            # 讀取攝影機影像
            while True:
                ret, frame = camera.read()
                if not ret:
                    # 失去攝影機連線，釋放資源並於 1 秒後嘗試重連
                    camera.release()
                    cv2.destroyAllWindows()
                    print("與攝影機失去連線，將於 1 秒後重試")
                    time.sleep(1)
                    break

                else:
                    # 發送影像
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
                    ndi.send(sender, frame)

                # 加入短暫延遲
                cv2.waitKey(1)

    except KeyboardInterrupt:
        print("停止 YOLO 模組")

    except Exception as e:
        print("發生未知錯誤")
        print(e)

    finally:
        if camera is not None:
            camera.release()
        cv2.destroyAllWindows()
        ndi.release(sender)


if __name__ == "__main__":
    main()
