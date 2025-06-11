import PySimpleGUI as sg
import asyncio
from .query import query_openrouter_async as query

sg.theme('DarkAmber')   # Add a touch of color

fast_query_result_field = sg.Text(
    size=(70, 10), 
    key='-SHORT RESULT-', 
    text_color="white",
)

descriptive_query_result_field = sg.Text(
    size=(70, 10), 
    key='-DESCRIPTIVE RESULT-', 
    text_color="white",
)

# All the stuff inside your window.
layout = [  [sg.Text("Write your request to the AI")],
            [sg.InputText()],
            [sg.Button('Ok'), sg.Button('Cancel')],
            [fast_query_result_field],
            [descriptive_query_result_field],
    ]

# Create the Window
window = sg.Window('Hello Example', layout, size=(600, 600))

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    # if event in ('r', 'R', 'к','К'):
        

    if event in ('Enter'):
        event = 'Ok'

    if event == 'Ok':
        def fast_sync_query():
            return asyncio.run(query(values[0], short_answer=True, temperature=0))
        
        def descriptive_sync_query():
            return asyncio.run(query(values[0], short_answer=False, temperature=0.7))

        window.perform_long_operation(
            fast_sync_query,
            "-CHAT_GPT SHORT ANSWER-",
        )

        window.perform_long_operation(
            descriptive_sync_query,
            "-CHAT_GPT DESCRIPTIVE ANSWER-",
        )

    elif event == "-CHAT_GPT SHORT ANSWER-":
        # print(values["-CHAT_GPT SHORT ANSWER-"])
        window["-SHORT RESULT-"].update(values["-CHAT_GPT SHORT ANSWER-"])

    elif event == "-CHAT_GPT DESCRIPTIVE ANSWER-":
        window["-DESCRIPTIVE RESULT-"].update(values["-CHAT_GPT DESCRIPTIVE ANSWER-"])

    # if user closes window or clicks cancel
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break

    # print('Hello', values[0], '!')

window.close()