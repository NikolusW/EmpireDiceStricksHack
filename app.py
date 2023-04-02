import PySimpleGUI as sg
from OpenAI import *
import random
import urllib.request
import io
from PIL import Image

sg.theme('DarkBlue')
roll_mode = False

def send_text(user_index):
    global roll_mode
    if roll_mode:
        return

    user_input = window[f'entry_{user_index}'].get()
    user_name = user_names[user_index]
    console.print(f"{user_name}: {user_input}")
    response = CustomChatGPT(user_input)
    # if "ROLL MODE" in response:
    #     roll_mode = True
    #     console.print("DM: Roll expected")
    #     for i in range(num_players):
    #         window[f'entry_{i}'].update(disabled=True)
    #         window[f'send_{i}'].update(disabled=True)
    #     window['roll_entry'].update(disabled=False)
    #     window['roll_send'].update(disabled=False)
    console.print(f"DM: {response}")
    window[f'entry_{user_index}'].update('')

    # if user_input.lower() == "roll mode":
    #     roll_mode = True
    #     console.print("DM: Roll expected")
    #     for i in range(num_players):
    #         window[f'entry_{i}'].update(disabled=True)
    #         window[f'send_{i}'].update(disabled=True)
    #     window['roll_entry'].update(disabled=False)
    #     window['roll_send'].update(disabled=False)

# First window to ask the number of players
num_players_layout = [
    [sg.Text("Welcome to 'The Empire Dice Strikes Hack: A Star Wars RPG Adventure!'\nPlease enter the number of players:")],
    [sg.InputText(key='num_players')],
    [sg.Button("OK")]
]

num_players_window = sg.Window("The Empire Dice Strikes Hack: A Star Wars RPG Adventure!", num_players_layout)

while True:
    event, values = num_players_window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == "OK":
        try:
            num_players = int(values['num_players'])
            break
        except ValueError:
            sg.popup_error("Please enter a valid integer for the number of players")

num_players_window.close()

if event != sg.WIN_CLOSED:
    # Second window to ask for user names and descriptions
    instructions = sg.Text("Please enter your name and a brief description for each player:")
    user_info_layout = [
        
        [sg.Text(f"Player {i + 1} name:"), sg.InputText(key=f'name_{i}'), sg.Text("Description:"), sg.Multiline(size=(20, 5), key=f'description_{i}') ] for i in range(num_players)
    ] + [[sg.Button("OK")]]

    user_info_window = sg.Window("The Empire Dice Strikes Hack: A Star Wars RPG Adventure!", user_info_layout)

    while True:
        event, values = user_info_window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == "OK":
            user_names = [values[f'name_{i}'] for i in range(num_players)]
            user_descriptions = [values[f'description_{i}'] for i in range(num_players)]
            break

    user_info_window.close()

    if event != sg.WIN_CLOSED:
        # Third window with the scrollable console
        console = sg.Multiline(size=(60, 20), autoscroll=True, key='console', disabled=True)
        entry_elements = [sg.InputText(size=(50, 1), key=f'entry_{i}') for i in range(num_players)]
        send_buttons = [sg.Button(f"Send {user_names[i]}", key=f'send_{i}', bind_return_key=True) for i in range(num_players)]

        health_bars = [sg.ProgressBar(100, orientation='h', size=(20, 20), key=f'health_bar_{i}', pad=((0, 0), (20, 0))) for i in range(num_players)]

        layout = [
            [console],
            *[[entry_elements[i], send_buttons[i]] for i in range(num_players)],
            # [sg.InputText(size=(50, 1), key='roll_entry', disabled=True), sg.Button("Roll Send", key='roll_send', disabled=True, bind_return_key=True)],
            [sg.Button("Generate Random")],
            [[sg.Text(f"{user_names[i]}'s health:"), health_bars[i]] for i in range(num_players)]
    
        ]
        # Create the main window
        window = sg.Window("The Empire Dice Strikes Hack: A Star Wars RPG Adventure!", layout, finalize=True)
        for i in range(num_players):
            window[f'health_bar_{i}'].update_bar(75)
        response = OpeningMessage(user_names,user_descriptions)
        # if "ROLL MODE" in response:
        #     roll_mode = True
        #     console.print("DM: Roll expected")
        #     for i in range(num_players):
        #         window[f'entry_{i}'].update(disabled=True)
        #         window[f'send_{i}'].update(disabled=True)
        #     window['roll_entry'].update(disabled=False)
        #     window['roll_send'].update(disabled=False)
        console.print(f"DM: {response}")

        # Run the main event loop
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            elif event.startswith('send_'):
                user_index = int(event.split('_')[1])
                send_text(user_index)
            elif event == 'Generate Random':
                random_number = random.randint(1, 20)
                console.print(f"App: Generated random number: {random_number}")
            # elif event == 'roll_send':
            #     if not roll_mode:
            #         continue

            #     roll_input = window['roll_entry'].get()
            #     console.print(f"Roll: {roll_input}")
            #     window['roll_entry'].update('')

            #     message = CustomChatGPT(roll_input)
            #     if "ROLL MODE" not in message:
            #         roll_mode = False
            #         for i in range(num_players):
            #             window[f'entry_{i}'].update(disabled=False)
            #             window[f'send_{i}'].update(disabled=False)
            #         window['roll_entry'].update(disabled=True)
            #         window['roll_send'].update(disabled=True)
            #     console.print(f"DM: {message}")

        window.close()
