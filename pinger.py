import socket
import time
import os
import sys
import random
import threading

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

color_step = 0

def interpolate_color(start_rgb, end_rgb, factor):
    r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * factor)
    g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * factor)
    b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * factor)
    return r, g, b

def rgb_to_ansi(r, g, b):
    codes = ['\033[91m', '\033[93m', '\033[92m', '\033[96m', '\033[94m', '\033[95m']
    if r > 200 and g < 100 and b < 100: return codes[0]
    elif r > 200 and g > 200 and b < 100: return codes[1]
    elif r < 100 and g > 200 and b < 100: return codes[2]
    elif r < 100 and g > 200 and b > 200: return codes[3]
    elif r < 100 and g < 100 and b > 200: return codes[4]
    else: return codes[5]

def gradient_banner():
    global color_step
    banner_text = [


"           ░██                         ░██   ░██    ",
"                                             ░██    ",
"░████████  ░██░████████   ░████████    ░██░████████ ",
"░██    ░██ ░██░██    ░██ ░██    ░██    ░██   ░██    ",
"░██    ░██ ░██░██    ░██ ░██    ░██    ░██   ░██    ",
"░███   ░██ ░██░██    ░██ ░██   ░███    ░██   ░██    ",
"░██░█████  ░██░██    ░██  ░█████░██    ░██    ░████ ",
"░██                             ░██                 ",
"░██                       ░███████                  ",
"",
"",
                                             
                                                                                                                                       
    ]
    
    colors = [(255,0,0), (255,255,0), (0,255,0), (0,255,255), (0,0,255), (255,0,255)]
    
    for i, line in enumerate(banner_text):
        if i == 7:
            print(f"\033[97m{line}\033[0m")
        else:
            phase = (color_step * 0.1 + i * 0.5) % 1.0
            start_idx = int(phase * (len(colors) - 1))
            end_idx = (start_idx + 1) % len(colors)
            local_factor = (phase * (len(colors) - 1)) % 1.0
            
            gradient_rgb = interpolate_color(colors[start_idx], colors[end_idx], local_factor)
            ansi_color = rgb_to_ansi(*gradient_rgb)
            print(f"{ansi_color}{line}\033[0m")
    
    color_step += 1

def animate_header():
    for _ in range(10):
        clear()
        gradient_banner()
        time.sleep(0.1)

def ping_loop(ip, port):
    while True:
        try:
            start = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, port))
            end = time.time()
            
            current_time = time.strftime("%H:%M:%S")
            
            if result == 0:
                ms = (end - start) * 1000
                print(f"\033[92m[{current_time}] Connected to {ip}:{port} - {ms:.0f}ms\033[0m")
            else:
                print(f"\033[91m[{current_time}] Connection timeout to {ip}:{port}\033[0m")
            
            sock.close()
            time.sleep(0)
            
        except KeyboardInterrupt:
            print(f"\n\033[93mPing stopped\033[0m")
            break
        except:
            current_time = time.strftime("%H:%M:%S")
            print(f"\033[91m[{current_time}] Server timeout {ip}:{port}\033[0m")
            time.sleep(0)

def main():
    animate_header()
    
    try:
        ip = input("IP or domain: ")
        if not ip:
            return
            
        port = input("port: ")
        if not port:
            return
            
        port = int(port)
        print(f"\nconnected {ip}:{port}")
        print()
        
        ping_loop(ip, port)
        
    except ValueError:
        print("invalid port")
    except KeyboardInterrupt:
        print("\nquitting")

if __name__ == "__main__":
    main()
