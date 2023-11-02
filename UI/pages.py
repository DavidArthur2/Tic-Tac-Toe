import PySimpleGUI as psg
import cv2
import threading
from base_game import *

from PySimpleGUI import WIN_CLOSED

bgclr = 'light blue'
camera_index = 0
window = None


def firstpage():
    b1 = psg.Button("Login", size=(30, 2))
    b2 = psg.Button("Register", size=(30, 2))
    b3 = psg.Button("Play as Guest", size=(30, 2))
    text1 = psg.Text(text='Tic-Tac-Toe', font=('Algerian', 50), text_color='black', background_color=bgclr)
    text2 = psg.Text(text='Players online: ', font=('Algerian', 15), text_color='black', background_color=bgclr)
    text3 = psg.Text(text='10', font=('Algerian', 15), text_color='black', background_color=bgclr)
    space = psg.Text('', size=(30, 8), background_color=bgclr)
    space1 = psg.Text('', size=(30, 1), background_color=bgclr)
    space2 = psg.Text('', size=(30, 1), background_color=bgclr)
    space3 = psg.Text('', size=(30, 8), background_color=bgclr)
    col1 = [[text1]]
    col2 = [[b1], [space1], [b2], [space2], [b3]]
    col3 = [[text2]]
    layout = [[psg.Column(col1, background_color=bgclr, justification='center')],
              [space],
              [psg.Column(col2, background_color=bgclr, justification='center')],
              [space3],
              [psg.Column(col3, background_color=bgclr, justification='r'), text3]]
    window = psg.Window('Tic-Tac-Toe', layout, size=(480, 640), background_color=bgclr,
                        element_justification='c')
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break
        elif event == 'Login':
            window.close()
            secondpage()
        elif event == 'Register':
            window.close()
            thirdpage()
        elif event == 'Play as Guest':
            window.close()
            fourthpage()
    window.close()


def secondpage():
    text1 = psg.Text(text='Tic-Tac-Toe', font=('Algerian', 50), text_color='black', background_color=bgclr)
    text2 = psg.Text(text='Username:', font=('Algerian', 15), text_color='black', background_color=bgclr)
    text3 = psg.Text(text='Password:', font=('Algerian', 15), text_color='black', background_color=bgclr)
    username = psg.Input(size=20, font=('Times New Roman', 14))
    psw = psg.Input(password_char='*', size=20, font=('Times New Roman', 14))
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
        event, values = window.read()
        if event in (None, 'Exit'):
            break
        elif event == 'Show Password':
            show_password = not show_password
            psw.update(password_char='' if show_password else '*')
        elif event == 'Back':
            window.close()
            firstpage()
        elif event == 'Login':
            window.close()
            fourthpage()
    window.close()


def thirdpage():
    text1 = psg.Text(text='Tic-Tac-Toe', font=('Algerian', 50), text_color='black', background_color=bgclr)
    username = psg.Input(size=20, font=('Times New Roman', 14))
    psw = psg.Input(password_char='*', size=20, font=('Times New Roman', 14), key='-psw-')
    con_psw = psg.Input(password_char='*', size=20, font=('Times New Roman', 14), key='-conpsw-')
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
            if values['-psw-'] != values['-conpsw-']:
                psg.popup_error("Passwords not matching!", font=16)
                continue
            else:
                window.close()
                fourthpage()
    window.close()


def fourthpage():
    text1 = psg.Text(text='Tic-Tac-Toe', font=('Algerian', 50), text_color='black', background_color=bgclr)
    text2 = psg.Text(text='Ranking: ', font=('Algerian', 13), text_color='black', background_color=bgclr)
    text3 = psg.Text(text='21', font=('Algerian', 13), text_color='black', background_color=bgclr)
    text4 = psg.Text(text='Mode: ', font=('Algerian', 25), text_color='black', background_color=bgclr)
    pve = psg.Button('PVE', size=(25, 2))
    pvp = psg.Button('PVP', size=(25, 2))
    leaderboard = psg.Button('Leaderboard', size=(15, 2))
    settings = psg.Button('Settings', size=(15, 2))
    turorial = psg.Button('Tutorial', size=(15, 2))
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
              [psg.Column(col5, background_color=bgclr, justification='c'), leaderboard, turorial],
              [space5],
              [psg.Column(col6, background_color=bgclr, justification='r')]
              ]
    window = psg.Window('Tic-Tac-Toe', layout, size=(480, 640), background_color=bgclr,
                        element_justification='c')
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break
        elif event == 'Logout':
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
    window.close()


def fifthpage():
    text1 = psg.Text(text='Tic-Tac-Toe', font=('Algerian', 50), text_color='black', background_color=bgclr)
    text2 = psg.Text(text='Ranking: ', font=('Algerian', 13), text_color='black', background_color=bgclr)
    text3 = psg.Text(text='21', font=('Algerian', 13), text_color='black', background_color=bgclr)
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
        event, values = window.read()
        if event in (None, 'Exit'):
            break
        elif event == 'Back':
            window.close()
            fourthpage()
        elif event == 'Online':
            window.close()
            ninthpage()
    window.close()


def put_on_window(pos, letter):  # 1 ha X, 2 ha O, POS: 1-9 ig
    global window
    tmp = f'-{pos}-'

    window[tmp].update(letter)


def sixthpage():
    global window

    text1 = psg.Text(text='You ', font=('Algerian', 40), text_color='black', background_color=bgclr)
    text2 = psg.Text(text='vs. ', font=('Algerian', 30), text_color='black', background_color=bgclr)
    text3 = psg.Text(text='Zoli74', font=('Algerian', 40), text_color='black', background_color=bgclr)
    b1 = psg.Button('', size=(15, 6), key='-1-')
    b2 = psg.Button('', size=(15, 6), key='-2-')
    b3 = psg.Button('', size=(15, 6), key='-3-')
    b4 = psg.Button('', size=(15, 6), key='-4-')
    b5 = psg.Button('', size=(15, 6), key='-5-')
    b6 = psg.Button('', size=(15, 6), key='-6-')
    b7 = psg.Button('', size=(15, 6), key='-7-')
    b8 = psg.Button('', size=(15, 6), key='-8-')
    b9 = psg.Button('', size=(15, 6), key='-9-')
    space1 = psg.Text('', size=(30, 3), background_color=bgclr)
    col1 = [[text1]]
    col2 = [[b1], [b4], [b7]]
    col3 = [[b2], [b5], [b8]]
    col4 = [[b3], [b6], [b9]]
    layout = [[psg.Column(col1, background_color=bgclr, justification='c'), text2, text3],
              [space1],
              [psg.Column(col2, background_color=bgclr, justification='c'),
               psg.Column(col3, background_color=bgclr, justification='c'),
               psg.Column(col4, background_color=bgclr, justification='c')]
              ]
    window = psg.Window('Tic-Tac-Toe', layout, size=(480, 640), background_color=bgclr,
                        element_justification='c',finalize=True)
    x = 0
    while True:
        event, values = window.read(timeout=100)

        if event == WIN_CLOSED:
            break
        elif event == 'Back':
            window.close()
            fourthpage()
        elif not queue.empty():  # Berakja a varakozasban levo lepest a grafikus feluletre
            raw = queue.get()
            raw = raw.split()
            pos = int(raw[0])
            letter = raw[1]
            put_on_window(pos, letter)
        else:  # Ha egyiksem teljesul, megnezzuk, hogy lépett e a képernyőn a player, és azt kerjuk feldolgozasra
            for i in range(1, 10):
                tmp = f'-{i}-'
                if event == tmp and window[tmp].get_text() == '':
                    letter = LETTER_O
                    if x:
                        letter = LETTER_X
                    res = put(i, letter)
                    if res == -1:
                        print('Cell not empty')
                    elif res == 0 or res == 2:  # Spaces full already, or game end
                        break
                    request_random_step(switch_letter(letter))
                    break
    window.close()


def seventhpage():
    text1 = psg.Text(text='Leaderboard: ', font=('Algerian', 40), text_color='black', background_color=bgclr)
    text2 = psg.Text(text='1.', font=('Algerian', 20), text_color='black', background_color=bgclr)
    text3 = psg.Text(text='Zoli74', font=('Algerian', 20), text_color='black', background_color=bgclr)
    text4 = psg.Text(text='2.', font=('Algerian', 20), text_color='black', background_color=bgclr)
    text5 = psg.Text(text='Marci52', font=('Algerian', 20), text_color='black', background_color=bgclr)
    b1 = psg.Button('Back', size=(10, 1))
    space1 = psg.Text('', size=(30, 5), background_color=bgclr)
    col1 = [[text1]]
    col2 = [[text2]]
    col3 = [[text4]]
    col4 = [[b1]]
    layout = [[psg.Column(col1, background_color=bgclr, justification='c')],
              [psg.Column(col2, background_color=bgclr, justification='l'), text3],
              [psg.Column(col3, background_color=bgclr, justification='l'), text5],
              [space1],
              [psg.Column(col4, background_color=bgclr, justification='r')]
              ]
    window = psg.Window('Tic-Tac-Toe', layout, size=(480, 640), background_color=bgclr,
                        element_justification='c')
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break
        elif event == 'Back':
            window.close()
            fourthpage()
    window.close()


def get_available_cameras():
    camera_list = []
    for i in range(1):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            camera_name = cap.getBackendName()
            camera_list.append((camera_name, i))
            cap.release()
    return camera_list


camera_list = get_available_cameras()
#camera_list = (1, 1)


def eighthpage():
    global bgclr
    text1 = psg.Text(text='Settings ', font=('Algerian', 40), text_color='black', background_color=bgclr)
    text2 = psg.Text(text='Change background color:', font=('Algerian', 15), text_color='black', background_color=bgclr)
    text3 = psg.Text(text='Select preferred camera: ', font=('Algerian', 15), text_color='black',
                     background_color=bgclr)
    im = psg.Image(filename="", key="image")
    comb = psg.Combo(values=camera_list, key="camera_index")
    b1 = psg.Button('Back', size=(10, 1))
    b2 = psg.Button('', size=(3, 1), key='lightblue', button_color='light blue')
    b3 = psg.Button('', size=(3, 1), key='lightgreen', button_color='light green')
    b4 = psg.Button('', size=(3, 1), key='red', button_color='red')
    b5 = psg.Button('', size=(3, 1), key='lightyellow', button_color='light yellow')
    b6 = psg.Button('Select')
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
    layout = [[psg.Column(col1, background_color=bgclr, justification='c')],
              [psg.Column(col2, background_color=bgclr, justification='l'),
               psg.Column(col3, background_color=bgclr, justification='l'),
               psg.Column(col4, background_color=bgclr, justification='l')],
              [psg.Column(col5, background_color=bgclr, justification='l'), comb],
              [psg.Column(col7, background_color=bgclr, justification='r'), space1],
              [space2],
              [im, space3, psg.Column(col6, background_color=bgclr, justification='c')]
              ]
    window = psg.Window('Tic-Tac-Toe', layout, size=(480, 640), background_color=bgclr,
                        element_justification='c')
    cap = None
    while True:
        event, values = window.read()
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
        elif event == "Select":
            selected_camera = values["camera_index"]
            global camera_index
            camera_index = selected_camera[1]
            if cap is None:
                cap = cv2.VideoCapture(camera_index)
            while True:
                ret, frame = cap.read()
                if not ret:
                    psg.popup_error("Camera not available.")
                    cap.release()
                    cap = None
                    break
                frame = cv2.resize(frame, (194, 144))
                imgbytes = cv2.imencode(".png", frame)[1].tobytes()

                window["image"].update(data=imgbytes)

                event, values = window.read(timeout=20)
                if event == psg.WIN_CLOSED or event == "Exit":
                    cap.release()
                    cap = None
                    break
                elif event == 'Back':
                    cap.release()
                    cap = None
                    window.close()
                    fourthpage()
                    break
                elif event == 'lightblue':
                    bgclr = 'light blue'
                    cap.release()
                    cap = None
                    window.close()
                    eighthpage()
                    break
                elif event == 'lightgreen':
                    bgclr = 'light green'
                    cap.release()
                    cap = None
                    window.close()
                    eighthpage()
                    break
                elif event == 'red':
                    bgclr = 'red'
                    cap.release()
                    cap = None
                    window.close()
                    eighthpage()
                    break
                elif event == 'lightyellow':
                    bgclr = 'light yellow'
                    window.close()
                    cap.release()
                    cap = None
                    eighthpage()
                    break
    window.close()


def ninthpage():
    text1 = psg.Text(text='Tic-Tac-Toe', font=('Algerian', 50), text_color='black', background_color=bgclr)
    text2 = psg.Text(text='Players online: ', font=('Algerian', 15), text_color='black', background_color=bgclr)
    text3 = psg.Text(text='Rank: ', font=('Algerian', 15), text_color='black', background_color=bgclr)
    b1 = psg.Button('Back', size=(10, 1))
    space1 = psg.Text('', size=(30, 5), background_color=bgclr)
    space2 = psg.Text('', size=(18, 1), background_color=bgclr)
    space3 = psg.Text('', size=(15, 1), background_color=bgclr)
    space4 = psg.Text('', size=(15, 3), background_color=bgclr)
    col1 = [[text1]]
    col2 = [[psg.Button(size=(20, 2), button_text=f"Player {row + 1}", key=row)] for row in range(3)]
    col3 = [[psg.Text(text=f"{rank + 1}", font=('Algerian', 25), text_color='black',
                      background_color=bgclr)] for rank in range(3)]
    col4 = [[text2]]
    col5 = [[b1]]
    col6 = [[text3]]
    layout = [[psg.Column(col1, background_color=bgclr, justification='c')],
              [space4],
              [psg.Column(col4, background_color=bgclr, justification='l'), space3,
               psg.Column(col6, background_color=bgclr, justification='l')],
              [psg.Column(col2, background_color=bgclr, justification='l'), space2,
               psg.Column(col3, background_color=bgclr, justification='l')],
              [space1],
              [psg.Column(col5, background_color=bgclr, justification='r')]
              ]
    window = psg.Window('Tic-Tac-Toe', layout, size=(480, 640), background_color=bgclr,
                        element_justification='c')
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break
        elif event == 'Back':
            window.close()
            fifthpage()
    window.close()


#threading.Thread(target=sixthpage).start()
#threading.Thread(target=request_put, args=(3, 'X')).start()