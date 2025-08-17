import NDIlib as ndi

class NDI:
    def __init__(self):
        ndi.initialize()

    def set_sender(self, sender_name):
        sender_setting = ndi.SendCreate()
        sender_setting.ndi_name = sender_name
        sender = ndi.send_create(sender_setting)
        sender_frame = ndi.VideoFrameV2()
        
        return [sender, sender_frame]
    
    def send(self, sender, frame):
        sender[1].data = frame
        sender[1].FourCC = ndi.FOURCC_VIDEO_TYPE_BGRX
        ndi.send_send_video_v2(sender[0], sender[1])

    def release(self, sender):
        ndi.send_destroy(sender[0])
        ndi.destroy()
