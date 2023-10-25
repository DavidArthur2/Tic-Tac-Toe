import PySimpleGUI as psg

b1 = psg.Button("Login")
b2 = psg.Button("Register")
layout = [[psg.Text(text='Tic-Tac-Toe',
    font=('Algerian', 50),
    text_color='black',
    background_color='light blue',
    expand_x=True)], [b1], [b2]
]
window = psg.Window('Tic-Tac-Toe', layout, size=(500, 600), background_color='light blue', element_justification='c')
while True:
   event, values = window.read()
   print(event, values)
   if event in (None, 'Exit'):
      break
window.close()