# Made by Cedric#0591

"""
Create a config.json file in the same directory as this file, that looks like the following:

{
    "exitKey":"end",

    "tR":0.8,
    "tG":0.4,
    "tB":0,
    "tA":1,

    "ctR":0,
    "ctG":0.4,
    "ctB":0.8,
    "ctA":1,

    
    "fovInt":120,
    "triggerbotDelay":0.15,

    "wallhack":1,
    "triggerbot":1,
    "bhop":1,
    "radarhack":1,
    "fov":1,
    "fovOption":1,
    "noflash":1

}
"""

import pymem
import pymem.process
import keyboard
from time import sleep
import requests
import json

offsets = requests.get("https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json").json()
configFile = open("config.json", "r")
config = json.load(configFile)
dwLocalPlayer = offsets["signatures"]["dwLocalPlayer"]
dwEntityList = offsets["signatures"]["dwEntityList"]
m_iTeamNum = offsets["netvars"]["m_iTeamNum"]
dwGlowObjectManager = offsets["signatures"]["dwGlowObjectManager"]
m_iGlowIndex = offsets["netvars"]["m_iGlowIndex"]
dwForceAttack = offsets["signatures"]["dwForceAttack"]
m_iCrosshairId = offsets["netvars"]["m_iCrosshairId"]
m_fFlags = offsets["netvars"]["m_fFlags"]
dwForceJump = offsets["signatures"]["dwForceJump"]
m_bSpotted = offsets["netvars"]["m_bSpotted"]
m_iFOV = offsets["netvars"]["m_iFOV"]
m_flFlashDuration = offsets["netvars"]["m_flFlashDuration"]
m_iDefaultFOV = offsets["netvars"]["m_iDefaultFOV"]

def main():
    # Enabled/Disabled (1/0)
    wallhack = config["wallhack"]
    triggerbot = config["triggerbot"]
    bhop = config["bhop"]
    radarhack = config["radarhack"]
    fov = config["fov"]
    noflash = config["noflash"]

    # Information
    print("")
    print(wallhack, triggerbot, bhop, radarhack, fov, noflash)
    print("exitKey: " + str(config["exitKey"]))
    print("fovInt: " + str(config["fovInt"]))
    print("triggerbotDelay: " + str(config["triggerbotDelay"]))
    print("fovOption: " + str(config["fovOption"]))
    print("")

    # Attach to csgo.exe
    try:
        pm = pymem.Pymem("csgo.exe")
        client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
        print("Cheats enabled!")
    except:
        print("Csgo was not found!")
        sleep(5)
        exit(0)

    # localPlayer
    localPlayer = pm.read_int(client + dwLocalPlayer)

    while True:
        # Exit program key
        if keyboard.is_pressed(config["exitKey"]):
            print("Exit key pressed. (" + config["exitKey"] + ")")
            exit(0)

        # Wallhack enabled
        if wallhack == 1:
            try:
                glow_manager = pm.read_int(client + dwGlowObjectManager)
                for i in range(1, 32):
                    entity = pm.read_int(client + dwEntityList + i * 0x10)

                    if entity:
                        entity_team_id = pm.read_int(entity + m_iTeamNum)
                        entity_glow = pm.read_int(entity + m_iGlowIndex)

                        if entity_team_id == 2: # Terrorist Glow
                            pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(config["tR"])) #R
                            pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(config["tG"])) #G
                            pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(config["tB"])) #B
                            pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, float(config["tA"])) #A
                            pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)
                
                        elif entity_team_id == 3: # Terrorist Glow
                            pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(config["ctR"])) #R
                            pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(config["ctG"])) #G
                            pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(config["ctB"])) #B
                            pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, float(config["ctA"])) #A
                            pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)
            except:
                pass
        
        # Triggerbot enabled
        if triggerbot == 1:
            try:
                crosshairID = pm.read_int(localPlayer + m_iCrosshairId)
                getTeam = pm.read_int(client + dwEntityList + (crosshairID - 1) * 0x10)
                localTeam = pm.read_int(localPlayer + m_iTeamNum)
                crosshairTeam = pm.read_int(getTeam + m_iTeamNum)

                if crosshairID > 0 and crosshairID < 32 and localTeam != crosshairTeam:
                    pm.write_int(client + dwForceAttack, 6)
                    sleep(config["triggerbotDelay"])
            except:
                pass
        
        # Bhop enabled
        if bhop == 1:
            try:
                if keyboard.is_pressed('space'):
                    force_jump = client + dwForceJump
                    on_ground = pm.read_int(localPlayer + m_fFlags)
                    if localPlayer and on_ground and on_ground == 257:
                        pm.write_int(force_jump, 6)
                        sleep(0.08)
                        pm.write_int(force_jump, 4)
            except:
                pass
        
        # Radarhack enabled
        if radarhack == 1:
            try:
                for i in range(1, 32):
                    entity = pm.read_int(client + dwEntityList + i * 0x10)
                    if entity:
                        pm.write_uchar(entity + m_bSpotted, 1)
            except:
                pass

        # Fov enabled
        if fov == 1:
            if config["fovOption"] == 1:
                try:
                    pm.write_int(localPlayer + m_iFOV, config["fovInt"])
                except:
                    pass
            elif config["fovOption"] == 2:
                try:
                    pm.write_int(localPlayer + m_iDefaultFOV, config["fovInt"])
                except:
                    pass
        
        # NoFlash enabled
        if noflash == 1:
            try:
                pm.write_int(localPlayer + m_flFlashDuration, 0)
            except:
                pass

if __name__ == '__main__':
    print("EzCheats by Cedric#0591")
    main()