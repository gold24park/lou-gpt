import traceback
from sys import exit, argv
from datetime import datetime
import os
import threading

import openai
from dotenv import load_dotenv

load_dotenv()

model = os.getenv("MODEL")
commands = ['/clear', '/token', '/quit', '/help']


def func_timeout(func, args=(), kwargs={}, timeout=5):
    class FuncThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = None

        def run(self):
            try:
                self.result = func(*args, **kwargs)
            except Exception as e:
                self.result = e

    thread = FuncThread()
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        raise TimeoutError()
    else:
        return thread.result


def prompt_gpt(messages: list, msg: str):
    messages.append({
        "role": "user",
        "content": msg
    })
    return openai.ChatCompletion.create(
        model=model,
        messages=messages,
    )


def prompt_command(messages: list, msg: str):
    cmd, arg = (msg + ' ').split(' ')
    if cmd == '/help':
        print_help()
    elif cmd == '/token':
        change_token(arg.strip())
    elif cmd == '/clear':
        clear_messages(messages)
    else:
        print('Bye!')
        exit(0)


def print_help():
    [print(m) for m in [
        '/clear: Remove all chat histories\n'
        '/token <token>: Change token',
        '/quit: Quit program'
    ]]


def change_token(token: str):
    if len(token) == 0:
        print('Please provide token.')
        return
    openai.api_key = token.strip()
    print(f'Token has been changed: {token}')


def clear_messages(messages: list):
    size = len(messages)
    messages.clear()
    print(f'All histories have been cleared. ({size} histories)')


if __name__ == '__main__':
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY") or argv[1]
    except IndexError as e:
        print('You must provide your OpenAI API key as argument')
        os.system("pause")
        exit(-1)

    max_timeout = int(os.getenv("MAX_TIMEOUT"))
    print(f'Model: {model}, Enter "/help" for help')
    messages = []
    while True:
        try:
            msg = input('>>> YOU: ')
            if msg.split(' ')[0] in commands:
                prompt_command(messages=messages, msg=msg)
            else:
                response = func_timeout(prompt_gpt, args=(messages, msg), timeout=max_timeout)
                gpt_msg = response.choices[0].message["content"].strip()
                print(f'>>> GPT: ({datetime.now()})')
                print(gpt_msg)
        except Exception as e:
            traceback.format_exc()
