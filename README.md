# CME UF60 Cyzuu

MIDI controller script for CME UF60 in FL Studio.
Maps faders, knobs, and transport buttons on the UF60 directly to FL Studio's mixer and transport without manual mapping.

## Features

- **Fader Volume** → Master Volume
- **Faders** → Track 1–8 Volume
- **Knobs** → Track 1–8 Pan
- **Transport** → Play / Stop / Record via custom CC
- **Channel Switch** → Next / Previous channel plugin

> do not use layer A or B on fader and knob

## Scripts

Two scripts included — pick whichever you need:

| File | What it does |
|------|-------------|
| `device_CMEUF60.py` + `main_controller.py` | Full: faders, knobs, transport, channel switch |
| `device_CMEUF60_Normal.py` | Transport + channel switch only (no mixer control) |

> You can install **both** at the same time — FL Studio supports multiple scripts per device. Just copy all `.py` files into the same folder.

## Installation

### Requirements

- 1 PC of course😹
- FL Studio 21.1+ (with Python scripting support)
- CME UF60 i u bought it 💔
- CME UF60 connected via USB

### Steps

1. **Clone or download** this repo:
   ```
   git clone https://github.com/USERNAME/CME_UF60_Cyzuu.git
   ```
   Or download the ZIP via the "Code > Download ZIP" button on GitHub.

2. **Copy all `.py` files** to:
   ```
   Documents/Image-Line/FL Studio/Settings/Hardware/CME UF60 Cyzuu/
   ```

3. **Open FL Studio** → **Options > MIDI settings** → **MIDI input** tab.

4. **Add** → select `CME UF60 Cyzuu` → **Enable**.

5. **Test** — move a fader/knob, check **View > Script Output** for logs.

### Easy Step using Command Prompt
copy this code and paste it to command prompt
```bash 
@echo off
set REPO=https://github.com/afriii69/CME-UF60-FlStudio
set DEST=%USERPROFILE%\Documents\Image-Line\FL Studio\Settings\Hardware\CME UF60 Cyzuu
curl -L -o %TEMP%\CME_UF60.zip %REPO%/archive/refs/heads/main.zip
powershell -command "Expand-Archive -Path %TEMP%\CME_UF60.zip -DestinationPath %TEMP%\CME_UF60_extract -Force"
if not exist "%DEST%" mkdir "%DEST%"
copy /Y "%TEMP%\CME_UF60_extract\CME-UF60-FlStudio-main\*.py" "%DEST%\"
echo Done! Open FL Studio and check MIDI settings.
timeout /t 2
```

> **Note:** Make sure each `.py` file has its `# name=` header on the first line. This is what FL Studio uses to identify the device.

## MIDI CC Mapping

### Transport & Channel

| CC | Function | Trigger |
|----|----------|---------|
| 119 | Play | value > 0 |
| 118 | Stop | value > 0 |
| 114 | Record | value > 0 (toggle) |
| 116 | Next Channel | value > 0 (use Rewind button) |
| 115 | Previous Channel | value > 0 (use Return to Start button) |

### Mixer

| Function | CC |
|----------|-----|
| Master Volume | 7 |
| Track 1 Vol | 11 |
| Track 2 Vol | 76 |
| Track 3 Vol | 77 |
| Track 4 Vol | 78 |
| Track 5 Vol | 98 |
| Track 6 Vol | 99 |
| Track 7 Vol | 0 |
| Track 8 Vol | 32 |
| Track 1 Pan | 74 |
| Track 2 Pan | 71 |
| Track 3 Pan | 73 |
| Track 4 Pan | 75 |
| Track 5 Pan | 72 |
| Track 6 Pan | 10 |
| Track 7 Pan | 91 |
| Track 8 Pan | 93 |

> Mixer mapping only applies to `CME UF60 Cyzuu`. And `CME UF60 Cyzuu - Seq Remote` ignores faders/knobs.

## Pedals

| Pedal | Default CC | Function |
|-------|-----------|----------|
| Pedal A (Sustain) | 64 | Sustain (forwarded to DAW) |
| Pedal B (Expression) | 11 | Expression (forwarded to DAW) |

> Pedal B conflicts with CC 11 (Track 1 Volume). You can reassign it using **Custom CC Assignment** below.

> CC 64 and 11 are **not handled** by the script. They are forwarded directly to FL Studio.

## Custom CC Assignment

To change a CC number on the UF60:

1. Press **SHIFT**, then **D#1 (Controller)**, and press the button you want to reassign
2. Turn the **encoder** to select a CC number
3. Press **ENTER** to confirm

Use the **CC 102–119** range for custom assignments to avoid conflicts with standard CCs.

## File Structure

```
CME_UF60_Cyzuu/
├── device_CMEUF60_Normal.py
├── device_CMEUF60.py
├── main_controller.py
└── README.md
```

## Debugging

- **Live log:** View > Script Output
- **Raw MIDI:** Options > Debugging log
- **Set `self.debug = True`** in `__init__` to enable logging

## License

MIT   
