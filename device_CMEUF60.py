# name=CME UF60 Cyzuu
# url=https://www.youtube.com/@Cyzuu1

from main_controller import CME_UF60_Cyzuu

controller = CME_UF60_Cyzuu()

def OnInit():
    controller.initialize()

def OnDeInit():
    controller.shutdown()

def OnMidiIn(event):
    controller.process_midi_event(event)

def OnIdle():
    controller.update_idle()

def OnRefresh(flags):
    if not controller.initialized:
        controller.initialize()
