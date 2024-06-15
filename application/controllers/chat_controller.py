#!/usr/bin/python3

import asyncio
import json
import websockets
import datetime
import PySimpleGUI as sg

global_message_queue = asyncio.Queue()
global_websock = None
GLOBAL_my_name = ''
PORT = 8050


def today_date():
    return datetime.datetime.now().strftime('%m-%d %H:%M:%S')


enable_print = True


def my_print(*args):
    if enable_print:
        print(*args)


def ui():
    global GLOBAL_my_name
    T_css = dict(font=("Helvetica", 12))

    users = sg.Listbox([], size=(30 - 5, 16), enable_events=True, key='users')
    message_board = sg.ML(size=(50 - 5, 15), key='messages_board')
    pm_board = sg.ML(size=(30 - 5, 16), key='pm_board')

    users_column = sg.Col([[sg.T('Users:', **T_css)], [users]])
    message_board_column = sg.Col([
        [sg.T('Message board', **T_css)], [message_board],
        [sg.I(key='message', size=(15, 1)), sg.B('▲ Public', key='public-msg'),
         sg.B('▲ User', disabled=True, key='private-msg')]
    ])
    pm_column = sg.Col([[sg.T('PM messages', **T_css)], [pm_board]])

    layout = [
        [sg.T('Your name'),
         sg.Input(GLOBAL_my_name, **T_css, disabled=True, use_readonly_for_disable=True, size=(30, 1), key='my_name'),
         sg.B('Change my name...', key='change-my-name')],
        [users_column, message_board_column, pm_column]
    ]
    return layout


async def gui_application():
    global global_message_queue, global_websock
    global GLOBAL_my_name
    while not GLOBAL_my_name:
        await asyncio.sleep(0.1)
        break

    try:
        window = sg.Window('Chat', ui(), finalize=True)
    except Exception as e:
        raise e

    while True:
        event, values = window(timeout=20)
        await asyncio.sleep(0.00001)
        if event in ('Exit', None):
            break
        if '__TIMEOUT__' != event:
            my_print(event)

        try:
            if not global_message_queue.empty():
                while not global_message_queue.empty():
                    item = await global_message_queue.get()

                    my_print(f'Handle message ▼▼▼')

                    if not item or item is None:
                        my_print('Bad queue item', item)
                        break

                    elif item['type'] == 'get-your-name':
                        my_name = item['name']
                        window['my_name'](my_name)
                        values['my_name'] = my_name
                        my_print(f'❄❄❄ my will be {my_name}')
                        global_message_queue.task_done()
                        my_print('Task done -=-=- (get-your-name)')

                    elif item['type'] == 'new_public_messages':
                        if item['messages_board']:
                            my_print('❄❄❄ new_public_messages')

                            mess = sorted(item['messages_board'], key=lambda x: x[0])
                            messages = '\n'.join(['{}: {}'.format(m[1], m[2]) for m in mess])

                            window['messages_board'].update(messages)
                            global_message_queue.task_done()
                            my_print('Task done -=-=- (new_public_messages)')

                    elif item['type'] == 'new_user_state':
                        my_print('\n', '❄❄❄ new_user_state')

                        my_name_val = values['my_name']
                        users_ = item['users']
                        filtered_users = [user_name for user_name in item['users'] if user_name != my_name_val]
                        window['users'].update(values=filtered_users)

                        my_print(
                            '''my_name:   {}\nall_users: {}\nfiltered: {}\n'''.format(my_name_val, ','.join(users_),
                                                                                      ','.join(filtered_users)))
                        global_message_queue.task_done()
                        my_print('Task done -=-=- (new_user_state)')

                    elif item['type'] == 'pm_message':
                        my_print('\n', '❄❄❄ pm_message')

                        params = today_date(), item['author'], item['text']
                        window['pm_board'].print("{}  {: <30} : {}".format(*params))
                        global_message_queue.task_done()
                        my_print('Task done -=-=- (pm_message)')

                    elif item['type'] == 'change-my-name':
                        if item['status'] == 'ok':
                            new_name = item['new_name']
                            window['my_name'](new_name)
                            my_print('\n', '❄❄❄ change-my-name', f'\nnew name will be: {new_name}')

                        elif item['status'] == 'no':
                            sg.Popup(item['message'])

                        global_message_queue.task_done()
                        my_print('Task done -=-=- (change-my-name)')

                    elif item['type'] == 'exit':
                        my_print('\n', '❄❄❄ exit')
                        global_message_queue.task_done()
                        my_print('Task done exit -=-=- (exit)')
                        break
                    my_print(f'▲▲▲')

        except Exception as e:
            my_print(e, '-' * 30)

        if values['users']:
            window['private-msg'](disabled=False)

        if event == 'change-my-name':
            new_name = sg.PopupGetText('New Name')
            if new_name:
                await global_websock.send(json.dumps({'action': 'change-my-name', "new_name": new_name}))

        if event == 'public-msg':
            message = json.dumps({'action': 'post-public-message', "text": values['message']})

            my_print(f"let's send public\nI will send: {message}")
            await global_websock.send(message)

            window['message']('')

        if event == 'private-msg':

            if not values['users']:
                window['message'].update('Please, select the user first.')
                continue

            if not values['message'].strip():
                window['message'].update('Please, type a non-empty message.')
                continue

            my_print("Let's send pm")
            text = values['message']
            which_user_name = values['users'][0]
            message = json.dumps({
                'action': 'send-a-pm',
                "which_user_name": which_user_name,
                'text': text})

            my_print(f'I will send: {message}')
            await global_websock.send(message)

            window['pm_board'].print("{}  {: <30} : {}".format(today_date(), 'to:' + which_user_name, text))
            window['message']('')

    window.close()

    if global_websock and not global_websock.closed:
        await global_websock.send(json.dumps({'action': 'exit'}))


async def websocket_reading():
    global PORT, global_message_queue, global_websock, GLOBAL_my_name
    try:
        a_ws = await websockets.connect(f"ws://localhost:{PORT}")
        global_websock = a_ws
        GLOBAL_my_name = json.loads(await a_ws.recv())['name']

        async for result in a_ws:
            json_msg = json.loads(result)

            if json_msg['type'] == 'exit':
                break

            await global_message_queue.put(json_msg)

        try:
            await a_ws.close()
        except Exception as e:
            print('Exception. cant close ws:', e)

    except Exception as e:
        print('Exception. ws died: ', e)


async def client():
    websocket_task = asyncio.create_task(websocket_reading())
    gui_task = asyncio.create_task(gui_application())

    await asyncio.wait([websocket_task, gui_task])


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client())
    loop.close()


if __name__ == '__main__':
    print('started')
    main()
    print('ended')
