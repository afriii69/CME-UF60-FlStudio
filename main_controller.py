import midi
import transport
import channels
import mixer
import general
import ui
import device

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
    MIDI_CHANNEL = 0

    CUSTOM_CC = {
        119: "PLAY",
        118: "STOP",
        114: "RECORD",
        116: "NX_PLUG",
        115: "PV_PLUG"
    }

    HANDLE_CUSTOM_CC = True

    MASTER_FADER_CC  = 7
    TRACK_FADER_CC_L1 = [11, 76, 77, 78, 98, 99, 0, 32]
    TRACK_KNOB_CC_L1  = [74, 71, 73, 75, 72, 10, 91, 93]
    L1_TRACK_OFFSET   = 1

    def __init__(self):
        self.initialized = False
        self.last_cc = {}
        self.last_note = None
        self.last_channel = None
        self.last_value = None
        self.debug = True
        self.isrecord = False

    def initialize(self):
        if self.initialized:
            return
        self.initialized = True
        self.log(logo)
        self.log("CME UF60 Cyzuu")
        self.log("Script is Under BLYAT CYKA NAHUY, uhhhm i mean... script is ok raight now blyat!")
        self.log("  Fader 9   -> Master Vol")
        self.log("  L1 Fader  -> Track 1-8 Vol")
        self.log("  L1 Knob   -> Track 1-8 Pan")
        self.log("  L2 Fader  -> Track 9-16 Vol")
        self.log("  L2 Knob   -> Track 9-16 Pan")

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
            data1 = event.data1
            data2 = event.data2
            message_type = status & 0xF0
            channel = status & 0x0F

            self.last_channel = channel
            self.last_value = data2

            if message_type == 0x90:
                if data2 == 0:
                    self.handle_note_off(channel, data1, data2)
                else:
                    self.handle_note_on(channel, data1, data2)
                return

            if message_type == 0x80:
                self.handle_note_off(channel, data1, data2)
                return

            if message_type == 0xB0:
                self.handle_cc(event, channel, data1, data2)
                return

            if message_type == 0xE0:
                self.handle_pitch_bend(event, channel, data1, data2)
                return

            self.forward_event(event)

        except Exception as e:
            self.log("MIDI error: %s" % str(e))

    def handle_note_on(self, channel, note, velocity):
        self.last_note = note

    def handle_note_off(self, channel, note, velocity):
        pass

    def handle_cc(self, event, channel, cc, value):
        self.last_cc[cc] = value

        self.log(
            "CC ch=%d cc=%d value=%d"
            % (channel + 1, cc, value)
        )

        if cc == self.MASTER_FADER_CC:
            mixer.setTrackVolume(0, value / 127.0)  
            event.handled = True
            return

        if cc in self.TRACK_FADER_CC_L1:
            track_idx = self.TRACK_FADER_CC_L1.index(cc) + self.L1_TRACK_OFFSET
            mixer.setTrackVolume(track_idx, value / 127.0)
            event.handled = True
            return

        if cc in self.TRACK_KNOB_CC_L1:
            track_idx = self.TRACK_KNOB_CC_L1.index(cc) + self.L1_TRACK_OFFSET
            pan = (value - 64) / 64.0
            mixer.setTrackPan(track_idx, pan)
            event.handled = True
            return


        action = self.CUSTOM_CC.get(cc)

        if action is not None and self.HANDLE_CUSTOM_CC:
            if value > 0:
                if self.execute_action(action, value):
                    event.handled = True
                    return

        self.forward_event(event)

    def handle_pitch_bend(self, event, channel, data1, data2):
        self.forward_event(event)

    def execute_action(self, action, value):
        if action == "PLAY":
            transport.start()
            return True

        if action == "STOP":
            transport.stop()
            if self.isrecord == True:
                transport.record()
                self.isrecord = False
            return True

        if action == "RECORD":
            if self.isrecord == False:
                self.isrecord = True
                transport.record()
                transport.start()
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

    def update_idle(self):
        if not self.initialized:
            return

    def forward_event(self, event):
        try:
            event.handled = False
        except Exception:
            pass

    def log(self, message):
        if self.debug:
            try:
                print("[CME UF60]   %s" % message)
            except Exception:
                pass   