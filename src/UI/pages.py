import PySimpleGUI as psg
import cv2
import threading
import sys
import os
import hashlib
import main
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Gesture Recognition'))
import base_game
import base_recognition
from base_game import *
from PySimpleGUI import WIN_CLOSED
from utils.config import *
import client

root_dir = os.path.dirname(os.path.abspath(__file__)) + '/'
bgclr = 'light blue'

camera_index = 0
position = None
window = None
win = None
prev_hover = 0
hover = 0
buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0]

leaderboard_list = [['Zoli74', 'Marci52', 'Jancsi', 'Arhur', 'Levi', 'Arnold', 'Janos', 'Jozsi', 'Robi', 'James'],
                    ['Jane', 'Adri', 'Valaki', 'Megvalaki'],
                    ['teszt1', 'teszt2']]
list_page = 0
leaderboard_rank = 1
players_list = [[('Zoli74', 2), ('Marci52', 5), ('Jancsi', 1), ('Arhur', 7), ('Levi', 3), ('Arnold', 4), ('Janos', 6), ('Jozsi', 10)],
                [('Jane', 12), ('Adri', 9), ('Valaki', 11), ('Megvalaki', 20)],
                [('teszt1', 30), ('teszt2', 40)]]
players_online_page = 0

player = ''
player_name = 'UN'
player_rank = -1
enemy_name = 'UN'
online_players = -1

Closed = threading.Event()
Ended = threading.Event()

Accepted = threading.Event()
Got_Inv = threading.Event()
Refused = threading.Event()
Disconnected = threading.Event()
Logout = threading.Event()
Ingame = threading.Event()
CantPut = threading.Event()
Wait_For_Request = threading.Event()
Stopped = threading.Event()
Canceled = threading.Event()

cb_last_state = False


def firstpage():
    global window, position
    Logout.clear()
    b1 = psg.Button("Login", size=(30, 2))
    b2 = psg.Button("Register", size=(30, 2))
    b3 = psg.Button("Play as Guest", size=(30, 2))
    text1 = psg.Text(text='Tic-Tac-Toe', font=('Algerian', 50), text_color='black', background_color=bgclr)
    text2 = psg.Text(text='Players online: ', font=('Algerian', 15), text_color='black', background_color=bgclr)
    timeout = 0
    while online_players == -1 and timeout < 100:
        time.sleep(0.1)
        timeout += 1
    text3 = psg.Text(text=f'{online_players}', font=('Algerian', 15), text_color='black', background_color=bgclr)
    space = psg.Text('', size=(30, 8), background_color=bgclr)
    space1 = psg.Text('', size=(30, 1), background_color=bgclr)
    space2 = psg.Text('', size=(30, 1), background_color=bgclr)
    space3 = psg.Text('', size=(30, 8), background_color=bgclr)
    space4 = psg.Text('', size=(30, 8), background_color=bgclr)
    col1 = [[text1]]
    col2 = [[b1], [space1], [b2], [space2], [space4]]
    col3 = [[text2]]
    layout = [[psg.Column(col1, background_color=bgclr, justification='center')],
              [space],
              [psg.Column(col2, background_color=bgclr, justification='center')],
              [space3],
              [psg.Column(col3, background_color=bgclr, justification='r'), text3]]
    window = psg.Window('Tic-Tac-Toe', layout, size=(480, 640), background_color=bgclr,
                        element_justification='c', finalize=True)

    while True:
        event, values = window.read(timeout=100)
        if event in (None, 'Exit'):
            break
        elif event == 'Login':
            if not client.Connected_To_Server.is_set():
                client.connect_to_server()
                client.Connected_To_Server.wait()
            window.close()
            secondpage()
        elif event == 'Register':
            if not client.Connected_To_Server.is_set():
                client.connect_to_server()
                client.Connected_To_Server.wait()
            window.close()
            thirdpage()
        elif event == 'Play as Guest':
            continue
            window.close()
            fourthpage()
    window.close()


def secondpage():
    global window, player_name
    text1 = psg.Text(text='Tic-Tac-Toe', font=('Algerian', 50), text_color='black', background_color=bgclr)
    text2 = psg.Text(text='Username:', font=('Algerian', 15), text_color='black', background_color=bgclr)
    text3 = psg.Text(text='Password:', font=('Algerian', 15), text_color='black', background_color=bgclr)
    username = psg.Input(key='username', size=20, font=('Times New Roman', 14))
    psw = psg.Input(key='pass', password_char='*', size=20, font=('Times New Roman', 14))
    show_psw = psg.Button('Show Password')
    back = psg.Button('Back', size=(10, 1))
    space1 = psg.Text('', size=(30, 9), background_color=bgclr)
    space2 = psg.Text('', size=(10, 1), background_color=bgclr)
    space3 = psg.Text('', size=(10, 1), background_color=bgclr)
    space4 = psg.Text('', size=(10, 1), background_color=bgclr)
    space5 = psg.Text('', size=(10, 10), background_color=bgclr)
    col1 = [[text1]]
    col2 = [[text2], [space2], [text3]]
    col3 = [[username], [space3], [psw, show_psw]]
    col4 = [[back]]
    b1 = psg.Button('Login', size=(15, 2))
    layout = [[psg.Column(col1, background_color=bgclr, justification='c')],
              [space1],
              [psg.Column(col2, background_color=bgclr, justification='c'),
               psg.Column(col3, background_color=bgclr, justification='c')],
              [space4],
              [b1],
              [space5],
              [psg.Column(col4, background_color=bgclr, justification='r')]]
    window = psg.Window('Login', layout, size=(480, 640), background_color=bgclr,
                        element_justification='c')

    show_password = False

    while True:
        event, values = window.read(timeout=100)
        if event in (None, 'Exit'):
            break
        elif event == 'Show Password':
            show_password = not show_password
            psw.update(password_char='' if show_password else '*')
        elif event == 'Back':
            window.close()
            firstpage()
        elif event == 'Login':
            if not client.Connected_To_Server.is_set():  #Needed connection with the server first!
                psg.popup_ok('Server unreachable!', 'You are not connected to the server!\nCheck your internet connection, and restart the game!')
                continue

            password = hashlib.md5(values['pass'].encode()).hexdigest()
            res = client.auth(values['username'], password)
            if not res:
                psg.popup_error("Could not connect to the server!", font=16, text_color='red')
                continue
            while not client.May_Login:
                continue
            if client.May_Login == 1:
                psg.popup_ok(f"Successful login!\nWelcome {values['username']}!", font=16)
                player_name = values['username']
                client.May_Login = 0
                window.close()
                fourthpage()
            elif client.May_Login == 2:
                psg.popup_ok("Incorrect credentials!", font=16, text_color='red')
                client.May_Login = 0
                continue
            elif client.May_Login == 3:
                psg.popup_ok("User already logged in!", font=16, text_color='red')
                client.May_Login = 0
                continue

    window.close()


def thirdpage():
    global window, player_name
    text1 = psg.Text(text='Tic-Tac-Toe', font=('Algerian', 50), text_color='black', background_color=bgclr)
    username = psg.Input(key='username', size=20, font=('Times New Roman', 14))
    psw = psg.Input(key='psw', password_char='*', size=20, font=('Times New Roman', 14))
    con_psw = psg.Input(key='conpsw', password_char='*', size=20, font=('Times New Roman', 14))
    show_psw = psg.Button('Show Password')
    back = psg.Button('Back', size=(10, 1))
    space1 = psg.Text('', size=(30, 5), background_color=bgclr)
    space2 = psg.Text('', size=(10, 1), background_color=bgclr)
    space3 = psg.Text('', size=(10, 1), background_color=bgclr)
    space4 = psg.Text('', size=(10, 1), background_color=bgclr)
    space5 = psg.Text('', size=(10, 1), background_color=bgclr)
    space6 = psg.Text('', size=(10, 1), background_color=bgclr)
    space7 = psg.Text('', size=(10, 1), background_color=bgclr)
    space8 = psg.Text('', size=(10, 3), background_color=bgclr)
    space9 = psg.Text('', size=(10, 3), background_color=bgclr)
    text2 = psg.Text(text='Username:', font=('Algerian', 15), text_color='black', background_color=bgclr)
    text3 = psg.Text(text='Password:', font=('Algerian', 15), text_color='black', background_color=bgclr)
    text4 = psg.Text(text='Confirm Password:', font=('Algerian', 15), text_color='black', background_color=bgclr)
    col1 = [[text1]]
    col2 = [[text2], [space2], [text3], [space5], [text4]]
    col3 = [[space8], [username], [space3], [psw], [space6], [con_psw], [space7], [show_psw]]
    col4 = [[back]]
    b1 = psg.Button('Register', size=(15, 2))
    layout = [[psg.Column(col1, background_color=bgclr, justification='c')],
              [space1],
              [psg.Column(col2, background_color=bgclr, justification='c'),
               psg.Column(col3, background_color=bgclr, justification='c')],
              [space4],
              [b1],
              [space9],
              [psg.Column(col4, background_color=bgclr, justification='r')]]
    window = psg.Window('Register', layout, size=(480, 640), background_color=bgclr,
                        element_justification='c')

    show_password = False

    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break
        elif event == 'Show Password':
            show_password = not show_password
            psw.update(password_char='' if show_password else '*')
            con_psw.update(password_char='' if show_password else '*')
        elif event == 'Back':
            window.close()
            firstpage()
        elif event == 'Register':
            if not client.Connected_To_Server.is_set():  #Needed connection with the server first!
                psg.popup_ok('Server unreachable!', 'You are not connected to the server!\nCheck your internet connection, and restart the game!')
                continue

            if values['psw'] != values['conpsw']:
                psg.popup_ok("Passwords are not matching!", font=16)
                continue
            else:
                password = hashlib.md5(values['psw'].encode()).hexdigest()
                client.auth(values['username'], password, reg=True)
                while not client.May_Login:  # Wait for response from the server
                    continue
                if client.May_Login == 1:
                    psg.popup_ok(f"Successful register!\nWelcome {values['username']}!", font=16)
                    player_name = values['username']
                    window.close()
                    fourthpage()
                elif client.May_Login == 2:
                    psg.popup_ok("Username already taken!", font=16, text_color='red')
                    continue
    window.close()


def fourthpage():
    global window, player_rank
    Logout.clear()
    text1 = psg.Text(text='Tic-Tac-Toe', font=('Algerian', 50), text_color='black', background_color=bgclr)
    text2 = psg.Text(text='Ranking: ', font=('Algerian', 13), text_color='black', background_color=bgclr)

    client.send_message('get-rank')
    timeout = 0
    player_rank = -1
    while player_rank == -1 and timeout < 100:
        time.sleep(0.1)
        timeout += 1

    text3 = psg.Text(text=f'{player_rank}', font=('Algerian', 13), text_color='black', background_color=bgclr)
    text4 = psg.Text(text='Mode: ', font=('Algerian', 25), text_color='black', background_color=bgclr)
    pve = psg.Button('PVE', size=(25, 2))
    pvp = psg.Button('PVP', size=(25, 2))
    leaderboard = psg.Button('Leaderboard', size=(15, 2))
    settings = psg.Button('Settings', size=(15, 2))
    tutorial = psg.Button('Tutorial', size=(15, 2))
    logout = psg.Button('Logout', size=(10, 1))
    space1 = psg.Text('', size=(30, 1), background_color=bgclr)
    space2 = psg.Text('', size=(10, 1), background_color=bgclr)
    space3 = psg.Text('', size=(30, 5), background_color=bgclr)
    space4 = psg.Text('', size=(10, 1), background_color=bgclr)
    space5 = psg.Text('', size=(10, 4), background_color=bgclr)
    col1 = [[text1]]
    col2 = [[text2]]
    col3 = [[text4]]
    col4 = [[pve], [space2], [pvp]]
    col5 = [[settings]]
    col6 = [[logout]]
    layout = [[psg.Column(col1, background_color=bgclr, justification='c')],
              [psg.Column(col2, background_color=bgclr, justification='r'), text3],
              [space1],
              [psg.Column(col3, background_color=bgclr, justification='l')],
              [space4],
              [psg.Column(col4, background_color=bgclr, justification='c')],
              [space3],
              [psg.Column(col5, background_color=bgclr, justification='c'), leaderboard, tutorial],
              [space5],
              [psg.Column(col6, background_color=bgclr, justification='r')]
              ]
    window = psg.Window('Tic-Tac-Toe', layout, size=(480, 640), background_color=bgclr,
                        element_justification='c')
    while True:
        event, values = window.read(timeout=100)
        if event in (None, 'Exit'):
            break
        elif event == 'Logout':
            client.May_Login = 0
            client.stop_connection()
            window.close()
            firstpage()
        elif event == 'PVP':
            window.close()
            fifthpage()
        elif event == 'Leaderboard':
            window.close()
            seventhpage()
        elif event == 'Settings':
            window.close()
            eighthpage()
        elif event == 'PVE':
            window.close()
            base_game.start_match(GAME_PVE)
        elif event == 'Tutorial':
            window.close()
            thirteenthpage()

        if Logout.is_set():
            Logout.clear()
            window.close()
            firstpage()
        if Got_Inv.is_set():
            r = psg.popup_timed("Game invitation", f"{enemy_name} invited you to play a game!\nDo you want to accept?", button_type=psg.POPUP_BUTTONS_YES_NO, auto_close_duration=20)
            if r == "Yes":
                if Canceled.set():
                    Canceled.clear()
                    psg.popup_timed('Canceled', 'The enemy canceled your invitation!\nReturning to menu.', button_type=psg.POPUP_BUTTONS_OK, auto_close_duration=2)
                    Got_Inv.clear()
                    window.close()
                    fourthpage()
                    return
                Got_Inv.clear()
                client.send_message('accept game')
            else:
                client.send_message('refuse game')
                Got_Inv.clear()

        if Accepted.is_set():
            Accepted.clear()
            window.close()
            base_game.start_match(GAME_PVP)
    window.close()


def fifthpage():
    global window, player
    text1 = psg.Text(text='Tic-Tac-Toe', font=('Algerian', 50), text_color='black', background_color=bgclr)
    text2 = psg.Text(text='Ranking: ', font=('Algerian', 13), text_color='black', background_color=bgclr)
    text3 = psg.Text(text=f'{player_rank}', font=('Algerian', 13), text_color='black', background_color=bgclr)
    text4 = psg.Text(text='How would you like to play ?', font=('Algerian', 15), text_color='black',
                     background_color=bgclr)
    b1 = psg.Button('Same PC', size=(30, 3))
    b2 = psg.Button('Online', size=(30, 3))
    b3 = psg.Button('Back', size=(10, 1))
    space1 = psg.Text('', size=(30, 5), background_color=bgclr)
    space2 = psg.Text('', size=(30, 3), background_color=bgclr)
    space3 = psg.Text('', size=(30, 6), background_color=bgclr)
    space4 = psg.Text('', size=(30, 1), background_color=bgclr)
    col1 = [[text1]]
    col2 = [[text2]]
    col3 = [[text4]]
    col4 = [[b1], [space4], [b2]]
    col5 = [[b3]]
    layout = [[psg.Column(col1, background_color=bgclr, justification='c')],
              [psg.Column(col2, background_color=bgclr, justification='r'), text3],
              [space1],
              [psg.Column(col3, background_color=bgclr, justification='l')],
              [space2],
              [psg.Column(col4, background_color=bgclr, justification='c')],
              [space3],
              [psg.Column(col5, background_color=bgclr, justification='r')]
              ]
    window = psg.Window('Tic-Tac-Toe', layout, size=(480, 640), background_color=bgclr,
                        element_justification='c')

    while True:
        event, values = window.read(timeout=100)
        if event in (None, 'Exit'):
            break
        elif event == 'Back':
            window.close()
            fourthpage()
        elif event == 'Online':
            window.close()
            ninthpage()
        elif event == 'Same PC':
            window.close()
            player = 'Player2'
            base_game.start_match(GAME_SAMEPC)

        if Got_Inv.is_set():
            r = psg.popup_timed("Game invitation", f"{enemy_name} invited you to play a game!\nDo you want to accept?", button_type=psg.POPUP_BUTTONS_YES_NO, auto_close_duration=20)
            if r == "Yes":
                if Canceled.set():
                    Canceled.clear()
                    psg.popup_timed('Canceled', 'The enemy canceled your invitation!\nReturning to menu.', button_type=psg.POPUP_BUTTONS_OK, auto_close_duration=2)
                    Got_Inv.clear()
                    window.close()
                    fourthpage()
                    return
                Got_Inv.clear()
                client.send_message('accept game')
            else:
                Got_Inv.clear()

        if Logout.is_set():
            Logout.clear()
            window.close()
            firstpage()

        if Accepted.is_set():
            Accepted.clear()
            window.close()
            base_game.start_match(GAME_PVP)

    window.close()


def put_on_window(pos, letter):  # 1 ha X, 2 ha O, POS: 1-9 ig
    global window, buttons
    tmp = f'-{pos}-'
    buttons[pos - 1] = 1
    if letter == 'X':
        window[tmp].update(image_filename=root_dir + 'X.png')
    else:
        window[tmp].update(image_filename=root_dir + 'O.png')


def change_round_icon(round, outcome):  # Ha, az outcome 0 -> lose, ha 1 -> win
    global window
    if outcome == 0:
        window[f'{round}.round'].update(image_filename=root_dir + 'roundX.png')
    else:
        window[f'{round}.round'].update(image_filename=root_dir + 'roundCheck.png')


def sixthpage():
    global window, position, hover, prev_hover
    CantPut.clear()
    if not queue.empty():
        answ = ''
        while not queue.empty():
            answ += str(queue.get())
            queue.get()
        sendError('Warning in pages.py/sixthpage', 'Queue not empty on initializing page!\n'+answ, 0)
    try:
        roundd = [None, None, None, None]
        if len(enemy_name) < 7:
            text1 = psg.Text(text='You ', font=('Algerian', 40), text_color='black', background_color=bgclr)
            text2 = psg.Text(text='vs. ', font=('Algerian', 30), text_color='black', background_color=bgclr)
            text3 = psg.Text(text=f'{enemy_name}', font=('Algerian', 40), text_color='black', background_color=bgclr)
        else:
            text1 = psg.Text(text='You ', font=('Algerian', 20), text_color='black', background_color=bgclr)
            text2 = psg.Text(text='vs. ', font=('Algerian', 10), text_color='black', background_color=bgclr)
            text3 = psg.Text(text=f'{enemy_name}', font=('Algerian', 20), text_color='black', background_color=bgclr)
        text4 = psg.Text(text='Round:', font=('Algerian', 20), text_color='black', background_color=bgclr)
        b1 = psg.Button('', key='-1-', button_color='white', image_filename=root_dir + 'background.png')
        b2 = psg.Button('', key='-2-', button_color='white', image_filename=root_dir + 'background.png')
        b3 = psg.Button('', key='-3-', button_color='white', image_filename=root_dir + 'background.png')
        b4 = psg.Button('', key='-4-', button_color='white', image_filename=root_dir + 'background.png')
        b5 = psg.Button('', key='-5-', button_color='white', image_filename=root_dir + 'background.png')
        b6 = psg.Button('', key='-6-', button_color='white', image_filename=root_dir + 'background.png')
        b7 = psg.Button('', key='-7-', button_color='white', image_filename=root_dir + 'background.png')
        b8 = psg.Button('', key='-8-', button_color='white', image_filename=root_dir + 'background.png')
        b9 = psg.Button('', key='-9-', button_color='white', image_filename=root_dir + 'background.png')
        if base_game.current_round != 1:
            for i in range(len(round_list)):
                t = 'roundBlank.png'
                kei = f'{i}.round'
                if round_list[i] != -1:
                    if round_list[i] == PLAYER_ME:
                        t = 'roundCheck.png'
                    elif round_list[i] == PLAYER_PC or round_list[i] == PLAYER_P2:
                        t = 'roundX.png'
                roundd[i] = psg.Button('', key=kei, button_color='white', image_filename=root_dir + t)
        else:
            roundd[1] = psg.Button('', key='1.round', button_color='white', image_filename=root_dir + 'roundBlank.png')
            roundd[2] = psg.Button('', key='2.round', button_color='white', image_filename=root_dir + 'roundBlank.png')
            roundd[3] = psg.Button('', key='3.round', button_color='white', image_filename=root_dir + 'roundBlank.png')

        im = psg.Image(filename="", key="image")
        space1 = psg.Text('', size=(30, 1), background_color=bgclr)
        space2 = psg.Text('', size=(30, 1), background_color=bgclr)
        col1 = [[text1]]
        col2 = [[b1], [b4], [b7]]
        col3 = [[b2], [b5], [b8]]
        col4 = [[b3], [b6], [b9]]
        col5 = [[text4]]
        layout = [[psg.Column(col1, background_color=bgclr, justification='c'), text2, text3],
                  [psg.Column(col5, background_color=bgclr, justification='l'), roundd[1], roundd[2], roundd[3]],
                  [space1],
                  [psg.Column(col2, background_color=bgclr, justification='c'),
                   psg.Column(col3, background_color=bgclr, justification='c'),
                   psg.Column(col4, background_color=bgclr, justification='c')],
                  [space2],
                  [im]
                  ]
        window = psg.Window('Tic-Tac-Toe', layout, size=(480, 640), background_color=bgclr,
                            element_justification='c')
    except Exception as e:
        sendError("Error in pages.py/sixthpage/Window-creation", str(e))

    try:
        src = base_game.current_round
        while src == base_game.current_round and not match_ended:
            event, values = window.read(timeout=100)
            if base_game.sig:  # Signal for restarting the round when it's TIE
                base_game.sig = False
                break
            position = window.current_location()

            if roundend_event.isSet():
                roundend_event.clear()
                r, _ = base_game.check_win()
                if r != TIE:
                    kei = f'{base_game.current_round}.round'
                    t = 'roundCheck.png'
                    if base_game.round_list[base_game.current_round] == PLAYER_PC or base_game.round_list[base_game.current_round] == PLAYER_P2:
                        t = 'roundX.png'
                    window[kei].update(image_filename=root_dir + t)
                else:
                    kei = f'{base_game.current_round}.round'
                    window[kei].update(image_filename=root_dir + 'roundBlank.png')
                    print('updated')
            # 194, 144
            if base_recognition.raw_frame is not None:  # Make image if it is initaialized and in use
                base_recognition.raw_frame = cv2.resize(base_recognition.raw_frame, (194, 144))
                imgbytes = cv2.imencode(".png", base_recognition.raw_frame)[1].tobytes()
                window["image"].update(data=imgbytes)

            if prev_hover != hover and prev_hover != 0:
                tmp = f'-{prev_hover}-'
                window[tmp].update(button_color='white')
                pass
            if Disconnected.is_set():
                Disconnected.clear()
                psg.popup_timed('Enemy disconnected! Returning to menu.',  auto_close_duration=5)
                window.close()
                fourthpage()
            if 0 < hover <= 9:
                tmp = f'-{hover}-'
                window[tmp].update(button_color='gray')
                prev_hover = hover
                if base_recognition.curr_gesture == OPEN_PALM:
                    event = tmp
                pass

            if event == psg.WIN_CLOSED or event == "Exit":
                window.close()
                main.stop_program()
                break
            if Logout.is_set():
                Logout.clear()
                window.close()
                firstpage()

            elif not queue.empty():  # Puts the queued step on the GUI, which has a format of: pos letter
                raw = queue.get()
                raw = raw.split()
                pos = int(raw[0])
                letter = raw[1]
                put_on_window(pos, letter)
            elif not CantPut.is_set():  # If nothing happened, then we check if the player moved on the screen
                for i in range(1, 10):
                    tmp = f'-{i}-'
                    if event == tmp:
                        if base_game.game_type == GAME_PVE:
                            request_put(i, PLAYER_ME)  # 3 means will be valid either Player1 or Player2, nor PC
                        elif base_game.game_type == GAME_SAMEPC:
                            request_put(i, base_game.current_player)
                        elif base_game.game_type == GAME_PVP:
                            request_put(i, PLAYER_ME)
                        break

        window.close()
        Closed.set()
    except Exception as e:
        sendError("Error in pages.py/sixthpage", str(e))


def update_leaderboard():
    global window, leaderboard_list, list_page, leaderboard_rank
    text1 = psg.Text(text='Leaderboard: ', font=('Algerian', 40), text_color='black', background_color=bgclr)
    b1 = psg.Button('Back', size=(10, 1), key='-back-')
    right_arrow = psg.Button('', image_filename=root_dir + 'right_arrow.png', key='-right-')
    left_arrow = psg.Button('', image_filename=root_dir + 'left_arrow.png', key='-left-')
    space1 = psg.Text('', size=(30, 1), background_color=bgclr)
    space2 = psg.Text('', size=(5, 1), background_color=bgclr)
    space3 = psg.Text('', size=(5, 1), background_color=bgclr)
    space4 = psg.Text('', size=(5, 1), background_color=bgclr)
    col1 = [[text1]]
    col2 = [[]]
    col3 = [[]]
    for user, rank in zip(leaderboard_list[list_page], range(leaderboard_rank, len(leaderboard_list[list_page]) + leaderboard_rank)):
        if user == ' ':
            col2 += [[psg.Text('', font=('Algerian', 20), background_color=bgclr)]]
            col3 += [[psg.Text('', font=('Algerian', 20), background_color=bgclr)]]
        else:
            col2 += [[psg.Text(text=user, font=('Algerian', 20), text_color='black', background_color=bgclr)]]
            col3 += [[psg.Text(text=f'{rank}.', font=('Algerian', 20), text_color='black', background_color=bgclr)]]
    col2 += [[space3], [right_arrow]]
    col3 += [[space4], [left_arrow]]
    col4 = [[b1]]
    layout = [[psg.Column(col1, background_color=bgclr, justification='c')],
              [psg.Column(col3, background_color=bgclr, justification='c'),
               space2,
               psg.Column(col2, background_color=bgclr, justification='c')],
              [space1],
              [psg.Column(col4, background_color=bgclr, justification='r')]
              ]
    window.close()
    window = psg.Window('Tic-Tac-Toe', layout, size=(480, 640), background_color=bgclr,
                        element_justification='c')


def seventhpage():
    global window, leaderboard_list, list_page, leaderboard_rank
    window = psg.Window('Tic-Tac-Toe')

    Wait_For_Request.clear()
    client.send_message('get all players')
    Wait_For_Request.wait()

    update_leaderboard()
    while True:
        event, values = window.read(timeout=100)
        if event in (None, 'Exit'):
            leaderboard_rank = 1
            list_page = 0
            break
        elif event == '-back-':
            leaderboard_rank = 1
            list_page = 0
            window.close()
            fourthpage()
        elif event == '-right-':
            if len(leaderboard_list) > list_page+1:
                leaderboard_rank += len(leaderboard_list[list_page])
                list_page += 1
                update_leaderboard()
        elif event == '-left-':
            if 0 < list_page:
                list_page -= 1
                leaderboard_rank -= len(leaderboard_list[list_page])
                update_leaderboard()
        if Got_Inv.is_set():
            r = psg.popup_timed("Game invitation", f"{enemy_name} invited you to play a game!\nDo you want to accept?", button_type=psg.POPUP_BUTTONS_YES_NO, auto_close_duration=20)
            if r == "Yes":
                if Canceled.set():
                    Canceled.clear()
                    psg.popup_timed('Canceled', 'The enemy canceled your invitation!\nReturning to menu.', button_type=psg.POPUP_BUTTONS_OK, auto_close_duration=2)
                    Got_Inv.clear()
                    window.close()
                    fourthpage()
                    return
                Got_Inv.clear()
                client.send_message('accept game')
            else:
                Got_Inv.clear()
        if Logout.is_set():
            Logout.clear()
            window.close()
            firstpage()

        if Accepted.is_set():
            Accepted.clear()
            window.close()
            base_game.start_match(GAME_PVP)
    window.close()


def get_available_cameras():
    global camera_list
    camera_list = []
    for i in range(1):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            camera_name = cap.getBackendName()
            camera_list.append((camera_name, i))
            cap.release()
    return camera_list


camera_list = get_available_cameras()


# camera_list = (1, 1)


def eighthpage():
    global bgclr, window, cb_last_state
    if base_recognition.cam_id == -1:
        psg.popup_timed("Cam scanning in progress...", auto_close_duration=3, button_type=psg.POPUP_BUTTONS_OK)
        base_recognition.list_cameras()
    text1 = psg.Text(text='Settings ', font=('Algerian', 40), text_color='black', background_color=bgclr)
    text2 = psg.Text(text='Change background color:', font=('Algerian', 15), text_color='black', background_color=bgclr)
    text4 = psg.Text(text='Show frames on camera:', font=('Algerian', 15), text_color='black', background_color=bgclr)
    text3 = psg.Text(text='Select preferred camera: ', font=('Algerian', 15), text_color='black',
                     background_color=bgclr)
    im = psg.Image(filename="", key="image")
    if base_recognition.cam_list is not None:
        if len(base_recognition.cam_list) > 0:
            comb = psg.Combo(values=base_recognition.cam_list, key="camera_index", readonly=True, default_value=base_recognition.cam_list[0])
        else:
            comb = psg.Combo(values=base_recognition.cam_list, key="camera_index", readonly=True)
    else:
        sendError('Error in pages.py/eighthpage', 'Combo box got a list of None. ')
        return
    b1 = psg.Button('Back', size=(10, 1))
    b2 = psg.Button('', size=(3, 1), key='lightblue', button_color='light blue')
    b3 = psg.Button('', size=(3, 1), key='lightgreen', button_color='light green')
    b4 = psg.Button('', size=(3, 1), key='red', button_color='red')
    b5 = psg.Button('', size=(3, 1), key='lightyellow', button_color='light yellow')
    b6 = psg.Button('Select')
    cb = psg.Checkbox('', key='grid', background_color=bgclr)
    space1 = psg.Text('', size=(7, 1), background_color=bgclr)
    space2 = psg.Text('', size=(30, 15), background_color=bgclr)
    space3 = psg.Text('', size=(20, 1), background_color=bgclr)
    col1 = [[text1]]
    col2 = [[text2]]
    col3 = [[b2], [b3]]
    col4 = [[b4], [b5]]
    col5 = [[text3]]
    col6 = [[b1]]
    col7 = [[b6]]
    col8 = [[text4]]
    layout = [[psg.Column(col1, background_color=bgclr, justification='c')],
              [psg.Column(col2, background_color=bgclr, justification='l'),
               psg.Column(col3, background_color=bgclr, justification='l'),
               psg.Column(col4, background_color=bgclr, justification='l')],
              [psg.Column(col5, background_color=bgclr, justification='l'), comb],
              [psg.Column(col8, background_color=bgclr, justification='l'), cb],
              [psg.Column(col7, background_color=bgclr, justification='r'), space1],
              [space2],
              [im, space3, psg.Column(col6, background_color=bgclr, justification='c')]
              ]
    window = psg.Window('Tic-Tac-Toe', layout, size=(480, 640), background_color=bgclr,
                        element_justification='c')
    while True:
        event, values = window.read(timeout=100)
        if Got_Inv.is_set():
            r = psg.popup_timed("Game invitation", f"{enemy_name} invited you to play a game!\nDo you want to accept?", button_type=psg.POPUP_BUTTONS_YES_NO, auto_close_duration=20)
            if r == "Yes":
                if Canceled.set():
                    Canceled.clear()
                    psg.popup_timed('Canceled', 'The enemy canceled your invitation!\nReturning to menu.', button_type=psg.POPUP_BUTTONS_OK, auto_close_duration=2)
                    Got_Inv.clear()
                    window.close()
                    fourthpage()
                    return
                Got_Inv.clear()
                client.send_message('accept game')
            else:
                Got_Inv.clear()

        if Logout.is_set():
            Logout.clear()
            window.close()
            firstpage()

        if Accepted.is_set():
            Accepted.clear()
            window.close()
            base_game.start_match(GAME_PVP)
        if event in (None, 'Exit'):
            break
        elif event == 'Back':
            window.close()
            fourthpage()
        elif event == 'lightblue':
            bgclr = 'light blue'
            window.close()
            eighthpage()
        elif event == 'lightgreen':
            bgclr = 'light green'
            window.close()
            eighthpage()
        elif event == 'red':
            bgclr = 'red'
            window.close()
            eighthpage()
        elif event == 'lightyellow':
            bgclr = 'light yellow'
            window.close()
            eighthpage()
        elif event == 'Back':
            window.close()
            fourthpage()
        elif values['grid'] != cb_last_state:
            cb_last_state = values['grid']
            base_recognition.show_grid = values['grid']
        elif event == "Select" and not len(base_recognition.cam_list):
            psg.popup_timed('No camera was found!',button_type=psg.POPUP_BUTTONS_OK, auto_close_duration=2)
        elif event == "Select" and len(base_recognition.cam_list):
            psg.popup_timed('Please wait while the camera is changing.', auto_close_duration=2)
            selected_camera = values["camera_index"]
            global camera_index
            camera_index = selected_camera[0]
            base_recognition.stop_recognition()
            if main.cam_t is not None:
                main.cam_t.join()
            base_recognition.cam_id = camera_index
            main.cam_t = threading.Thread(target=base_recognition.operate_recognition)
            main.cam_t.start()

            base_recognition.camInitFinished.wait()

            if not base_recognition.camInitialized.is_set():
                psg.popup_error("Camera not available.")
                base_recognition.stop_recognition()
                return
            psg.popup_timed('Camera changed!', auto_close_duration=2)
        if base_recognition.cam is None or base_recognition.raw_frame is None:
            continue
        frame = cv2.resize(base_recognition.raw_frame, (194, 144))
        imgbytes = cv2.imencode(".png", frame)[1].tobytes()
        window["image"].update(data=imgbytes)
    window.close()


def update_players_online():
    global window, players_online_page, players_list
    text1 = psg.Text(text='Tic-Tac-Toe', font=('Algerian', 50), text_color='black', background_color=bgclr)
    text2 = psg.Text(text='Players online: ', font=('Algerian', 15), text_color='black', background_color=bgclr)
    text3 = psg.Text(text='Rank: ', font=('Algerian', 15), text_color='black', background_color=bgclr)
    b1 = psg.Button('Back', size=(10, 1))
    right_arrow = psg.Button('', image_filename=root_dir + 'right_arrow.png', key='-right-')
    left_arrow = psg.Button('', image_filename=root_dir + 'left_arrow.png', key='-left-')
    space1 = psg.Text('', size=(5, 1), background_color=bgclr)
    space2 = psg.Text('', size=(18, 1), background_color=bgclr)
    space3 = psg.Text('', size=(15, 1), background_color=bgclr)
    space4 = psg.Text('', size=(5, 1), background_color=bgclr)
    col1 = [[text1]]
    if players_list[players_online_page][0] == ' ':
        col2 = [[psg.Text('', font=('Algerian', 25), background_color=bgclr)]
                 for _ in range(1, 9)]
        col3 = [[psg.Text('', font=('Algerian', 25), background_color=bgclr)]
                 for _ in range(1, 9)]
    else:
        col2 = [[psg.Button(size=(20, 2), button_text=player_online[0], key=f'P{key}')]
                for player_online, key in
                zip(players_list[players_online_page], range(1, len(players_list[players_online_page]) + 1))]
        col3 = [[psg.Text(text=online_rank[1], font=('Algerian', 25), text_color='black', background_color=bgclr)]
                for online_rank in players_list[players_online_page]]
        if len(players_list[players_online_page]) != 8:
            col2 += [[psg.Text('', font=('Algerian', 25), background_color=bgclr)]
                     for _ in range(1, 9-len(players_list[players_online_page]))]
            col3 += [[psg.Text('', font=('Algerian', 25), background_color=bgclr)]
                     for _ in range(1, 9-len(players_list[players_online_page]))]
    col2 += [[space1], [left_arrow]]
    col3 += [[space4], [right_arrow]]
    col4 = [[text2]]
    col5 = [[b1]]
    col6 = [[text3]]
    layout = [[psg.Column(col1, background_color=bgclr, justification='c')],
              [psg.Column(col4, background_color=bgclr, justification='l'), space3,
               psg.Column(col6, background_color=bgclr, justification='l')],
              [psg.Column(col2, background_color=bgclr, justification='l'), space2,
               psg.Column(col3, background_color=bgclr, justification='l')],
              [psg.Column(col5, background_color=bgclr, justification='r')]
              ]
    window.close()
    window = psg.Window('Tic-Tac-Toe', layout, size=(480, 640), background_color=bgclr,
                        element_justification='c')


def ninthpage():
    global window, players_online_page, players_list, enemy_name
    window = psg.Window('Tic-Tac-Toe')

    Wait_For_Request.clear()
    client.send_message('get online players')
    Wait_For_Request.wait()

    update_players_online()
    while True:
        event, values = window.read(timeout=100)
        if event in (None, 'Exit'):
            players_online_page = 0
            break
        elif event == 'Back':
            players_online_page = 0
            window.close()
            fifthpage()
        for i in range(1, 9):
            if event == f'P{i}':
                enemy_name = players_list[players_online_page][i-1][0]
                player = window[f'P{i}'].ButtonText
                if player == ' ':
                    psg.popup_ok('Hiba', 'Sajnos egyedül vagy fent!')
                    break
                window.close()
                Accepted.clear()
                client.send_message(f'req game {enemy_name}')
                eleventhpage()
                players_online_page = 0
                break

        if event == '-right-':
            if len(players_list) > players_online_page+1:
                players_online_page += 1
                update_players_online()
        elif event == '-left-':
            if 0 < players_online_page:
                players_online_page -= 1
                update_players_online()
        if Got_Inv.is_set():
            r = psg.popup_timed("Game invitation", f"{enemy_name} invited you to play a game!\nDo you want to accept?", button_type=psg.POPUP_BUTTONS_YES_NO, auto_close_duration=20)
            if r == "Yes":
                if Canceled.set():
                    Canceled.clear()
                    psg.popup_timed('Canceled', 'The enemy canceled your invitation!\nReturning to menu.', button_type=psg.POPUP_BUTTONS_OK, auto_close_duration=2)
                    Got_Inv.clear()
                    window.close()
                    fourthpage()
                    return
                Got_Inv.clear()
                client.send_message('accept game')
            else:
                Got_Inv.clear()
        if Logout.is_set():
            Logout.clear()
            window.close()
            firstpage()

        if Accepted.is_set():
            Accepted.clear()
            window.close()
            base_game.start_match(GAME_PVP)
    window.close()


def tenthpage():
    global window
    text1 = psg.Text(text='You ', font=('Algerian', 40), text_color='black', background_color=bgclr)
    text2 = psg.Text(text='vs. ', font=('Algerian', 30), text_color='black', background_color=bgclr)
    text3 = psg.Text(text=f'{enemy_name}', font=('Algerian', 40), text_color='black', background_color=bgclr)
    text4 = psg.Text(text='Round:', font=('Algerian', 20), text_color='black', background_color=bgclr)
    b1 = psg.Button('', key='-1-', button_color='white', image_filename=root_dir + 'background.png')
    b2 = psg.Button('', key='-2-', button_color='white', image_filename=root_dir + 'background.png')
    b3 = psg.Button('', key='-3-', button_color='white', image_filename=root_dir + 'background.png')
    b4 = psg.Button('', key='-4-', button_color='white', image_filename=root_dir + 'background.png')
    b5 = psg.Button('', key='-5-', button_color='white', image_filename=root_dir + 'background.png')
    b6 = psg.Button('', key='-6-', button_color='white', image_filename=root_dir + 'background.png')
    b7 = psg.Button('', key='-7-', button_color='white', image_filename=root_dir + 'background.png')
    b8 = psg.Button('', key='-8-', button_color='white', image_filename=root_dir + 'background.png')
    b9 = psg.Button('', key='-9-', button_color='white', image_filename=root_dir + 'background.png')
    round1 = psg.Button('', key='1.round', button_color='white', image_filename=root_dir + 'roundBlank.png')
    round2 = psg.Button('', key='2.round', button_color='white', image_filename=root_dir + 'roundBlank.png')
    round3 = psg.Button('', key='3.round', button_color='white', image_filename=root_dir + 'roundBlank.png')
    space1 = psg.Text('', size=(30, 1), background_color=bgclr)
    space2 = psg.Text('', size=(30, 1), background_color=bgclr)
    col1 = [[text1]]
    col2 = [[b1], [b4], [b7]]
    col3 = [[b2], [b5], [b8]]
    col4 = [[b3], [b6], [b9]]
    col5 = [[text4]]
    layout = [[psg.Column(col1, background_color=bgclr, justification='c'), text2, text3],
              [space2],
              [psg.Column(col5, background_color=bgclr, justification='l'), round1, round2, round3],
              [space1],
              [psg.Column(col2, background_color=bgclr, justification='c'),
               psg.Column(col3, background_color=bgclr, justification='c'),
               psg.Column(col4, background_color=bgclr, justification='c')]
              ]
    window = psg.Window('Tic-Tac-Toe', layout, size=(480, 640), background_color=bgclr,
                        element_justification='c', finalize=True)
    x = 0
    while True:
        event, values = window.read(timeout=100)

        if event == WIN_CLOSED:
            break
        elif event == 'Back':
            window.close()
            fourthpage()
        elif not queue.empty():  # Berakja a varakozasban levo lepest
            raw = queue.get()
            raw = raw.split()
            pos = int(raw[0])
            letter = raw[1]
            put_on_window(pos, letter)
        else:  # Ha egyiksem teljesul, megnezzuk, hogy lépett e a képernyőn a player, és azt rakjuk
            global buttons
            for i in range(1, 10):
                tmp = f'-{i}-'
                if event == tmp and buttons[i - 1] == 0:
                    letter = 'O'
                    if x:
                        letter = 'X'
                    put_on_window(i, letter)
                    x = not x
                    break

    window.close()


def eleventhpage():
    global window, player
    text1 = psg.Text(text='Waiting', font=('Algerian', 40), text_color='black', background_color=bgclr)
    text2 = psg.Text(text='for', font=('Algerian', 40), text_color='black', background_color=bgclr)
    text3 = psg.Text(text=f'{enemy_name}', font=('Algerian', 40), text_color='black', background_color=bgclr)
    text4 = psg.Text(text='to', font=('Algerian', 40), text_color='black', background_color=bgclr)
    text5 = psg.Text(text='Respond...', font=('Algerian', 40), text_color='black', background_color=bgclr)
    space1 = psg.Text('', size=(30, 7), background_color=bgclr)
    space2 = psg.Text('', size=(30, 6), background_color=bgclr)
    b1 = psg.Button('Cancel', size=(10, 1))
    col1 = [[b1]]
    layout = [[space1],
              [text1],
              [text2],
              [text3],
              [text4],
              [text5],
              [space2],
              [psg.Column(col1, background_color=bgclr, justification='r')]
              ]
    window = psg.Window('Tic-Tac-Toe', layout, size=(480, 640), background_color=bgclr,
                        element_justification='c', finalize=True)
    while True:
        event, values = window.read(timeout=100)
        if event in (None, 'Exit'):
            break
        elif event == 'Cancel':
            client.send_message('canceled')
            window.close()
            fourthpage()
        if Refused.is_set():
            Refused.clear()
            psg.popup_timed('Refused', f'{enemy_name} refused your invitation!', auto_close_duration=5)
            window.close()
            fourthpage()
        if Logout.is_set():
            Logout.clear()
            window.close()
            firstpage()
        if Ingame.is_set():
            Ingame.clear()
            psg.popup_ok('Declined', f'{enemy_name} is already in game!')
            window.close()
            fourthpage()

        if Accepted.is_set():
            Accepted.clear()
            window.close()
            base_game.start_match(GAME_PVP)

    window.close()


def twelfth():
    global win, window
    timeout = 0
    while player_rank == -1 and timeout < 100:
        time.sleep(0.1)
        timeout += 1
    j = 0
    for i in round_list:
        if base_game.decode_player(i) == 'You' and (base_game.game_type == GAME_PVP or base_game.game_type == GAME_PVE) or base_game.decode_player(i) == 'Player_1' and base_game.game_type == GAME_SAMEPC:
            j += 1
    win = True if j > 1 else False
    if base_game.game_type != GAME_SAMEPC:
        if win:
            text1 = psg.Text(text='Victory', font=('Algerian', 50), text_color='black',
                             background_color='green', border_width=50)
        else:
            text1 = psg.Text(text='Defeat', font=('Algerian', 50), text_color='black',
                             background_color='red', border_width=50)
    else:
        if win:
            text1 = psg.Text(text='Victory for Player_1', font=('Algerian', 30), text_color='black',
                             background_color='green', border_width=50)
        else:
            text1 = psg.Text(text='Victory for Player_2', font=('Algerian', 30), text_color='black',
                             background_color='green', border_width=50)
    base_game.clear_board(True)
    text2 = psg.Text(text='New Rank:', font=('Algerian', 30), text_color='black', background_color=bgclr)
    text3 = psg.Text(text=f'{player_rank}', font=('Algerian', 30), text_color='black', background_color=bgclr)
    space1 = psg.Text('', size=(30, 4), background_color=bgclr)
    space2 = psg.Text('', size=(30, 1), background_color=bgclr)
    space3 = psg.Text('', size=(30, 4), background_color=bgclr)
    space4 = psg.Text('', size=(30, 1), background_color=bgclr)
    space5 = psg.Text('', size=(30, 4), background_color=bgclr)
    new_game = psg.Button('Go to menu', size=(25, 3))
    rematch = psg.Button('Rematch', size=(25, 3))
    col1 = [[text1]]
    col2 = [[text2]]
    col3 = [[text3]]
    col4 = [[new_game]]
    if base_game.game_type == GAME_PVP:
        col5 = [[rematch]]
    else:
        col5 = [[space5]]
    layout = [[space4],
              [psg.Column(col1, background_color=bgclr, justification='c')],
              [space1],
              [psg.Column(col2, background_color=bgclr, justification='c')],
              [space2],
              [psg.Column(col3, background_color=bgclr, justification='c')],
              [space3],
              [psg.Column(col4, background_color=bgclr, justification='c'),
               psg.Column(col5, background_color=bgclr, justification='c')]
              ]
    window = psg.Window('Tic-Tac-Toe', layout, size=(480, 640), background_color=bgclr,
                        element_justification='c', finalize=True)
    while True:
        event, values = window.read(timeout=100)
        if event in (None, 'Exit'):
            break
        elif event == 'Go to menu':
            window.close()
            fourthpage()
        elif event == 'Rematch':
            Accepted.clear()
            window.close()
            client.send_message(f'req game {enemy_name}')
            eleventhpage()
        if Logout.is_set():
            Logout.clear()
            window.close()
            firstpage()
        if Got_Inv.is_set():
            r = psg.popup_timed("Game invitation", f"{enemy_name} invited you to play a game!\nDo you want to accept?", button_type=psg.POPUP_BUTTONS_YES_NO, auto_close_duration=20)
            if r == "Yes":
                if Canceled.set():
                    Canceled.clear()
                    psg.popup_timed('Canceled', 'The enemy canceled your invitation!\nReturning to menu.', button_type=psg.POPUP_BUTTONS_OK, auto_close_duration=2)
                    Got_Inv.clear()
                    window.close()
                    fourthpage()
                    return
                Got_Inv.clear()
                client.send_message('accept game')
            else:
                Got_Inv.clear()

        if Accepted.is_set():
            Accepted.clear()
            window.close()
            base_game.start_match(GAME_PVP)
    window.close()


def thirteenthpage():
    global window
    text1 = psg.Text(text='Tic-Tac-Toe', font=('Algerian', 40), text_color='black', background_color=bgclr)
    text2 = psg.Text(text='You can control the game with a mouse or using a', font=('Algerian', 12),
                     text_color='black', background_color=bgclr)
    text3 = psg.Text(text='camera. If you choose the camera, you will control', font=('Algerian', 12),
                     text_color='black', background_color=bgclr)
    text4 = psg.Text(text='the game with hand gestures. Here I will present you', font=('Algerian', 12),
                     text_color='black', background_color=bgclr)
    text5 = psg.Text(text='how you can use your hand to move the cursor on the ', font=('Algerian', 12),
                     text_color='black', background_color=bgclr)
    text6 = psg.Text(text='playfield. You can see two images below, the first', font=('Algerian', 12),
                     text_color='black', background_color=bgclr)
    text7 = psg.Text(text='one shows you how you need to keep your hand to', font=('Algerian', 12),
                     text_color='black', background_color=bgclr)
    text8 = psg.Text(text=' move the grey square around. The second image', font=('Algerian', 12),
                     text_color='black', background_color=bgclr)
    text9 = psg.Text(text=' shows you how you can lock the grey squares', font=('Algerian', 12),
                     text_color='black', background_color=bgclr)
    text10 = psg.Text(text='position and place your move.', font=('Algerian', 12),
                     text_color='black', background_color=bgclr)
    text11 = psg.Text(text='Tutorial', font=('Algerian', 20), text_color='black', background_color=bgclr)
    text12 = psg.Text(text='First image', font=('Algerian', 15), text_color='black', background_color=bgclr)
    text13 = psg.Text(text='Second image', font=('Algerian', 15), text_color='black', background_color=bgclr)
    button1 = psg.Button(image_filename=root_dir + 'fingers_closed.png')
    button2 = psg.Button(image_filename=root_dir + 'fingers_open.png')
    button3 = psg.Button('Back', size=(10, 1))
    space1 = psg.Text('', size=(30, 1), background_color=bgclr)
    col1 = [[button1], [text12]]
    col2 = [[button2], [text13]]
    col3 = [[button3]]
    layout = [[text1],
              [text11],
              [text2],
              [text3],
              [text4],
              [text5],
              [text6],
              [text7],
              [text8],
              [text9],
              [text10],
              [psg.Column(col1, background_color=bgclr, justification='c'),
               psg.Column(col2, background_color=bgclr, justification='c')],
              [space1],
              [psg.Column(col3, background_color=bgclr, justification='r')]
              ]
    window = psg.Window('Tic-Tac-Toe', layout, size=(480, 640), background_color=bgclr,
                        element_justification='c', finalize=True)
    while True:
        event, values = window.read(timeout=100)
        if event in (None, 'Exit'):
            break
        elif event == 'Back':
            window.close()
            fourthpage()
