import PySimpleGUI as psg


def firstpage():
    b1 = psg.Button("Login", size=(30, 2))
    b2 = psg.Button("Register", size=(30, 2))
    b3 = psg.Button("Play as Guest", size=(30, 2))
    text1 = psg.Text(text='Tic-Tac-Toe', font=('Algerian', 50), text_color='black', background_color='light blue')
    text2 = psg.Text(text='Players online: ', font=('Algerian', 15), text_color='black', background_color='light blue')
    text3 = psg.Text(text='10', font=('Algerian', 15), text_color='black', background_color='light blue')
    space = psg.Text('', size=(30, 8), background_color='light blue')
    space1 = psg.Text('', size=(30, 1), background_color='light blue')
    space2 = psg.Text('', size=(30, 1), background_color='light blue')
    space3 = psg.Text('', size=(30, 8), background_color='light blue')
    col1 = [[text1]]
    col2 = [[b1], [space1], [b2], [space2], [b3]]
    col3 = [[text2]]
    layout = [[psg.Column(col1, background_color='light blue', justification='center')],
              [space],
              [psg.Column(col2, background_color='light blue', justification='center')],
              [space3],
              [psg.Column(col3, background_color='light blue', justification='r'), text3]]
    window = psg.Window('Tic-Tac-Toe', layout, size=(480, 640), background_color='light blue',
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
    text1 = psg.Text(text='Tic-Tac-Toe', font=('Algerian', 50), text_color='black', background_color='light blue')
    text2 = psg.Text(text='Username:', font=('Algerian', 15), text_color='black', background_color='light blue')
    text3 = psg.Text(text='Password:', font=('Algerian', 15), text_color='black', background_color='light blue')
    username = psg.Input(size=20, font=('Times New Roman', 14))
    psw = psg.Input(password_char='*', size=20, font=('Times New Roman', 14))
    show_psw = psg.Button('Show Password')
    back = psg.Button('Back')
    space1 = psg.Text('', size=(30, 9), background_color='light blue')
    space2 = psg.Text('', size=(10, 1), background_color='light blue')
    space3 = psg.Text('', size=(10, 1), background_color='light blue')
    space4 = psg.Text('', size=(10, 1), background_color='light blue')
    space5 = psg.Text('', size=(10, 10), background_color='light blue')
    col1 = [[text1]]
    col2 = [[text2], [space2], [text3]]
    col3 = [[username], [space3], [psw, show_psw]]
    col4 = [[back]]
    b1 = psg.Button('Login', size=(15, 2))
    layout = [[psg.Column(col1, background_color='light blue', justification='c')],
              [space1],
              [psg.Column(col2, background_color='light blue', justification='c'),
               psg.Column(col3, background_color='light blue', justification='c')],
              [space4],
              [b1],
              [space5],
              [psg.Column(col4, background_color='light blue', justification='r')]]
    window = psg.Window('Login', layout, size=(480, 640), background_color='light blue',
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
    text1 = psg.Text(text='Tic-Tac-Toe', font=('Algerian', 50), text_color='black', background_color='light blue')
    username = psg.Input(size=20, font=('Times New Roman', 14))
    psw = psg.Input(password_char='*', size=20, font=('Times New Roman', 14), key='-psw-')
    con_psw = psg.Input(password_char='*', size=20, font=('Times New Roman', 14), key='-conpsw-')
    show_psw = psg.Button('Show Password')
    back = psg.Button('Back')
    space1 = psg.Text('', size=(30, 5), background_color='light blue')
    space2 = psg.Text('', size=(10, 1), background_color='light blue')
    space3 = psg.Text('', size=(10, 1), background_color='light blue')
    space4 = psg.Text('', size=(10, 1), background_color='light blue')
    space5 = psg.Text('', size=(10, 1), background_color='light blue')
    space6 = psg.Text('', size=(10, 1), background_color='light blue')
    space7 = psg.Text('', size=(10, 1), background_color='light blue')
    space8 = psg.Text('', size=(10, 3), background_color='light blue')
    space9 = psg.Text('', size=(10, 3), background_color='light blue')
    text2 = psg.Text(text='Username:', font=('Algerian', 15), text_color='black', background_color='light blue')
    text3 = psg.Text(text='Password:', font=('Algerian', 15), text_color='black', background_color='light blue')
    text4 = psg.Text(text='Confirm Password:', font=('Algerian', 15), text_color='black', background_color='light blue')
    col1 = [[text1]]
    col2 = [[text2], [space2], [text3], [space5], [text4]]
    col3 = [[space8], [username], [space3], [psw], [space6], [con_psw], [space7], [show_psw]]
    col4 = [[back]]
    b1 = psg.Button('Register', size=(15, 2))
    layout = [[psg.Column(col1, background_color='light blue', justification='c')],
              [space1],
              [psg.Column(col2, background_color='light blue', justification='c'),
               psg.Column(col3, background_color='light blue', justification='c')],
              [space4],
              [b1],
              [space9],
              [psg.Column(col4, background_color='light blue', justification='r')]]
    window = psg.Window('Register', layout, size=(480, 640), background_color='light blue',
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
    text1 = psg.Text(text='Tic-Tac-Toe', font=('Algerian', 50), text_color='black', background_color='light blue')
    text2 = psg.Text(text='Ranking: ', font=('Algerian', 13), text_color='black', background_color='light blue')
    text3 = psg.Text(text='21', font=('Algerian', 13), text_color='black', background_color='light blue')
    text4 = psg.Text(text='Mode: ', font=('Algerian', 25), text_color='black', background_color='light blue')
    pve = psg.Button('PVE', size=(25, 2))
    pvp = psg.Button('PVP', size=(25, 2))
    leaderboard = psg.Button('Leaderboard', size=(15, 2))
    settings = psg.Button('Settings', size=(15, 2))
    turorial = psg.Button('Tutorial', size=(15, 2))
    logout = psg.Button('Logout', size=(10, 1))
    space1 = psg.Text('', size=(30, 1), background_color='light blue')
    space2 = psg.Text('', size=(10, 1), background_color='light blue')
    space3 = psg.Text('', size=(30, 5), background_color='light blue')
    space4 = psg.Text('', size=(10, 1), background_color='light blue')
    space5 = psg.Text('', size=(10, 4), background_color='light blue')
    col1 = [[text1]]
    col2 = [[text2]]
    col3 = [[text4]]
    col4 = [[pve], [space2], [pvp]]
    col5 = [[settings]]
    col6 = [[logout]]
    layout = [[psg.Column(col1, background_color='light blue', justification='c')],
              [psg.Column(col2, background_color='light blue', justification='r'), text3],
              [space1],
              [psg.Column(col3, background_color='light blue', justification='l')],
              [space4],
              [psg.Column(col4, background_color='light blue', justification='c')],
              [space3],
              [psg.Column(col5, background_color='light blue', justification='c'), leaderboard, turorial],
              [space5],
              [psg.Column(col6, background_color='light blue', justification='r')]
              ]
    window = psg.Window('Tic-Tac-Toe', layout, size=(480, 640), background_color='light blue',
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
    window.close()


def fifthpage():
    text1 = psg.Text(text='Tic-Tac-Toe', font=('Algerian', 50), text_color='black', background_color='light blue')
    text2 = psg.Text(text='Ranking: ', font=('Algerian', 13), text_color='black', background_color='light blue')
    text3 = psg.Text(text='21', font=('Algerian', 13), text_color='black', background_color='light blue')
    text4 = psg.Text(text='How would you like to play ?', font=('Algerian', 15), text_color='black',
                     background_color='light blue')
    b1 = psg.Button('Same PC', size=(30, 3))
    b2 = psg.Button('Online', size=(30, 3))
    b3 = psg.Button('Back', size=(8, 1))
    space1 = psg.Text('', size=(30, 5), background_color='light blue')
    space2 = psg.Text('', size=(30, 3), background_color='light blue')
    space3 = psg.Text('', size=(30, 6), background_color='light blue')
    space4 = psg.Text('', size=(30, 1), background_color='light blue')
    col1 = [[text1]]
    col2 = [[text2]]
    col3 = [[text4]]
    col4 = [[b1], [space4], [b2]]
    col5 = [[b3]]
    layout = [[psg.Column(col1, background_color='light blue', justification='c')],
              [psg.Column(col2, background_color='light blue', justification='r'), text3],
              [space1],
              [psg.Column(col3, background_color='light blue', justification='l')],
              [space2],
              [psg.Column(col4, background_color='light blue', justification='c')],
              [space3],
              [psg.Column(col5, background_color='light blue', justification='r')]
              ]
    window = psg.Window('Tic-Tac-Toe', layout, size=(480, 640), background_color='light blue',
                        element_justification='c')

    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break
        elif event == 'Back':
            window.close()
            fourthpage()
    window.close()


fifthpage()
