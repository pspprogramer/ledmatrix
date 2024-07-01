import serial
import keyboard
import time

# Serial port settings for different modules
MODULE_PORTS = {
    'module1': "COM3",
    'module2': "COM4",
}

# Game configurations
GAME_CONFIGS = {
    0x00: {  # Game 00 (Snake)
        'controls': {
            'up':    0x00,
            'down':  0x01,
            'left':  0x02,
            'right': 0x03,
            'w':     0x00,
            's':     0x01,
            'a':     0x02,
            'd':     0x03
        },
        'keys': ['up', 'down', 'left', 'right', 'w', 's', 'a', 'd']  # Arrow keys and WASD
    },
    0x01: {  # Game 01 (Pong)
        'controls': {
            'player_top_left':  0x02,
            'player_top_right': 0x03,
            'player_bottom_left':  0x05,
            'player_bottom_right': 0x06
        },
        'keys_top': ['a', 'd'],  # Player top controls
        'keys_bottom': ['left', 'right']  # Player bottom controls
    }
}

BAUD_RATE = 115200

# Magic bytes for command initiation
MAGIC_BYTE_1 = 0x32
MAGIC_BYTE_2 = 0xAC

# Command IDs
CMD_START_GAME = 0x10
CMD_GAME_CTRL = 0x11
CMD_GAME_STATUS = 0x12
CMD_SLEEP = 0x03

# Current game ID to test (e.g., 0x00 for Snake)
game_id = 0x01

# Number of modules to use
NUM_MODULES = 1  # Adjust this number as needed

# Buffer for last control pressed
last_control_pressed = None

def is_port_ready(port):
    """Check if the port is ready to be opened."""
    try:
        with serial.Serial(port) as ser:
            return ser.isOpen()
    except serial.SerialException:
        return False

def send_command(command_id, parameters=None, with_response=False, port=MODULE_PORTS['module1']):
    if parameters is None:
        parameters = []
    
    try:
        with serial.Serial(port, BAUD_RATE) as ser:
            command = [MAGIC_BYTE_1, MAGIC_BYTE_2, command_id] + parameters
            ser.write(bytearray(command))
            
            if with_response:
                res = ser.read(32)
                return res
    except serial.SerialException as e:
        print(f"Failed to send command on port {port}: {e}")

def start_game(game_id, port):
    """Start an embedded game on a specific module."""
    send_command(CMD_START_GAME, [game_id], port=port)
    time.sleep(1)  # Give some time for the game to start

def send_control(control_byte, ports):
    """Send a control byte to the game on multiple ports."""
    global last_control_pressed
    
    # Try to send control byte to each port, with retry if port is not ready
    for port in ports:
        while True:
            if is_port_ready(port):
                send_command(CMD_GAME_CTRL, [control_byte], port=port)
                last_control_pressed = control_byte
                break
            else:
                print(f"Port {port} not ready, waiting...")
                time.sleep(0.1)

def report_controls():
    """Report current controls to the player."""
    if game_id in GAME_CONFIGS:
        print(f"Controls for Game {game_id:02X}:")
        if game_id == 0x00:  # Snake
            print("Use arrow keys or WASD")
        elif game_id == 0x01:  # Pong
            print("Player Top: A and D")
            print("Player Bottom: left and right arrow keys")

def get_game_status():
    """Get game status from the modules."""
    res = send_command(CMD_GAME_STATUS, with_response=True, port=MODULE_PORTS['module1'])
    if res:
        print(f"Game Status Response: {res}")
    else:
        print("No response received.")

def put_modules_to_sleep():
    """Put modules to sleep to turn off LEDs."""
    for port in MODULE_PORTS.values():
        send_command(CMD_SLEEP, port=port)

def on_key_event(event):
    global last_control_pressed
    if event.event_type == keyboard.KEY_DOWN:
        key = event.name.lower()
        
        # Check if the key is mapped for the current game
        if key == 'esc':
            print("Exiting the script.")
            put_modules_to_sleep()  # Put modules to sleep when exiting
            keyboard.unhook_all()
            quit()
        
        if game_id in GAME_CONFIGS:
            if 'keys' in GAME_CONFIGS[game_id] and key in GAME_CONFIGS[game_id]['keys']:
                control_byte = GAME_CONFIGS[game_id]['controls'][key]
                send_control(control_byte, list(MODULE_PORTS.values())[:NUM_MODULES])
            elif 'keys_top' in GAME_CONFIGS[game_id] and key in GAME_CONFIGS[game_id]['keys_top']:
                control_byte = GAME_CONFIGS[game_id]['controls']['player_top_left'] if key == 'a' else GAME_CONFIGS[game_id]['controls']['player_top_right']
                send_control(control_byte, list(MODULE_PORTS.values())[:NUM_MODULES])
            elif 'keys_bottom' in GAME_CONFIGS[game_id] and key in GAME_CONFIGS[game_id]['keys_bottom']:
                control_byte = GAME_CONFIGS[game_id]['controls']['player_bottom_left'] if key == 'left' else GAME_CONFIGS[game_id]['controls']['player_bottom_right']
                send_control(control_byte, list(MODULE_PORTS.values())[:NUM_MODULES])

if __name__ == "__main__":
    # Start the desired game on the specified number of modules
    for port in list(MODULE_PORTS.values())[:NUM_MODULES]:
        start_game(game_id, port)
    
    # Register key events
    keyboard.hook(on_key_event)

    # Keep the program running
    print(f"Started game with ID {game_id:02X}.")
    print(f"Using {NUM_MODULES} module(s).")
    print("Press Esc to exit.")
    report_controls()
    
    # Faster polling loop
    while True:
        # get_game_status()
        time.sleep(.1)  # Adjust as needed
