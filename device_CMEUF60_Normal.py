# name=CME UF60 Cyzuu - Seq Remote
# url=https://www.youtube.com/@Cyzuu1

import transport
import channels

logo = r"""
 _    _ ______ __   ___              _____                      
| |  | |  ____/ /  / _ \            / ____|                     
| |  | | |__ / /_ | | | |  ______  | |    _   _ _____   _ _   _ 
| |  | |  __| '_ \| | | | |______| | |   | | | |_  / | | | | | |
| |__| | |  | (_) | |_| |          | |___| |_| |/ /| |_| | |_| |
 \____/|_|   \___/ \___/            \_____\__, /___|\__,_|\__,_|
                                           __/ |                
                                          |___/                   
"""

class CME_UF60_Cyzuu:

    CUSTOM_CC = {
        119: "PLAY",
        118: "STOP",
        114: "RECORD",
        116: "NX_PLUG",
        115: "PV_PLUG"
    }

    HANDLE_CUSTOM_CC = True

    def __init__(self):
        self.initialized = False
        self.isrecord = False
        self.debug = True

    def initialize(self):
        if self.initialized:
            return
        self.initialized = True
        self.log(logo)
        self.log("CME UF60 Cyzuu - Seq Remote")
        self.log("Script is Under BLYAT CYKA NAHUY, uhhhm i mean... script is ok raight now blyat!")
        self.log("  CC 119 -> Play")
        self.log("  CC 118 -> Stop")
        self.log("  CC 114 -> Record")
        self.log("  CC 116 -> Next Channel")
        self.log("  CC 115 -> Prev Channel")

    def shutdown(self):
        if not self.initialized:
            return
        self.log("CME UF60 shutting down")
        self.log("GOOD BYE BLYAT")
        self.initialized = False

    def process_midi_event(self, event):
        if not self.initialized:
            return

        try:
            status = event.status
            cc = event.data1
            value = event.data2

            if (status & 0xF0) != 0xB0:
                return

            self.log("CC cc=%d value=%d" % (cc, value))

            action = self.CUSTOM_CC.get(cc)

            if action is not None and self.HANDLE_CUSTOM_CC:
                if value > 0:
                    if self.execute_action(action, value):
                        event.handled = True
                        return

        except Exception as e:
            self.log("MIDI error: %s" % str(e))

    def execute_action(self, action, value):
        if action == "PLAY":
            self.log("PLAY")
            transport.start()
            return True

        if action == "STOP":
            self.log("STOP")
            transport.stop()
            if self.isrecord:
                transport.record()
                self.isrecord = False
            return True

        if action == "RECORD":
            if not self.isrecord:
                self.isrecord = True
                transport.record()
                transport.start()
                self.log("RECORD ON")
            else:
                self.isrecord = False
                transport.record()
                self.log("RECORD OFF")
            return True

        if action == "PV_PLUG":
            current = channels.selectedChannel()
            total = channels.channelCount()
            new_idx = (current - 1) % total
            channels.selectOneChannel(new_idx)
            return True
        
        if action == "NX_PLUG":
            current = channels.selectedChannel()
            total = channels.channelCount()
            new_idx = (current + 1) % total
            channels.selectOneChannel(new_idx)
            return True

        return False

    def log(self, message):
        if self.debug:
            try:
                print("[CME UF60]   %s" % message)
            except Exception:
                pass


_cyzuu = CME_UF60_Cyzuu()

def OnInit():
    _cyzuu.initialize()

def OnDeInit():
    _cyzuu.shutdown()

def OnMidiIn(event):
    _cyzuu.process_midi_event(event)

def OnIdle():
    pass   