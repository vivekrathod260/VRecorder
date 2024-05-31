import json
import time
from datetime import datetime
import threading
import pyautogui # type: ignore
from pynput import mouse, keyboard # type: ignore
from pynput.mouse import Button, Controller as MouseController # type: ignore
from pynput.keyboard import Controller as KeyboardController, Key # type: ignore
import keyboard as kb # type: ignore


class Recorder:
    def record_event(self, event_type, **kwargs):
        self.events.append({
            'time': (datetime.now() - self.start_time).total_seconds(),
            'event': event_type,
            **kwargs
        })

    def on_move(self, x, y):
        self.record_event('move', x=x, y=y)

    def on_click(self, x, y, button, pressed):
        self.record_event('click', x=x, y=y, button=str(button), pressed=pressed)

    def on_scroll(self, x, y, dx, dy):
        self.record_event('scroll', x=x, y=y, dx=dx, dy=dy)

    def on_press(self, key):
        if key == None:
            return
        if key == keyboard.Key.esc :
            self.stopAndSave()  # Stop recording on 'esc' key press
            return False
        try:
            self.record_event('keypress', key=key.char)
        except AttributeError:
            self.record_event('keypress', key=str(key))

    def on_release(self, key):
        if key == None:
            return
        try:
            self.record_event('keyrelease', key=key.char)
        except AttributeError:
            self.record_event('keyrelease', key=str(key))


    def start(self):
        self.events = []

        self.mouse_listener = mouse.Listener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)

        self.start_time = datetime.now()

        self.mouse_listener.start()
        self.keyboard_listener.start()
        print("Recording ...")

    def stop(self):
        self.mouse_listener.stop()
        self.keyboard_listener.stop()

        self.mouse_listener.join()
        self.keyboard_listener.join()
        print("Recording stopped")

    def save(self, filename='user_actions.json'):
        fp = open(filename, 'w')
        json.dump(self.events[2:-2], fp, indent=4)
        fp.close()
        print("Recording saved as "+str(filename))

    def stopAndSave(self, filename='user_actions.json'):
        self.stop()
        self.save(filename)


class Player:
    def __init__(self):
        self.events = []
        self.filename = "user_actions.json"
        self.idolTime = 0
        self.mouse = MouseController()
        self.keyboard = KeyboardController()
        self.status = 1 # play

    def load(self, filename='user_actions.json'):
        fp = open(filename, 'r')
        self.events = json.load(fp)
        fp.close()
        self.filename = filename
        print("Data loaded "+str(self.filename))

    def worker(self):
        start_time = datetime.now()
        for event in self.events:
            if(self.status == -1):
                return
            if(self.status == 0):
                time.sleep(1)
                continue

            elapsed_time = event['time'] - ((datetime.now() - start_time).total_seconds() - self.idolTime)
            if elapsed_time > 0:
                time.sleep(elapsed_time)

            if event['event'] == 'move':
                self.mouse.position = (event['x'], event['y'])
                # pyautogui.moveTo(event['x'], event['y'])
            elif event['event'] == 'click':
                button = Button.left if event['button'] == 'Button.left' else Button.right
                if event['pressed']:
                    self.mouse.press(button)
                else:    
                    self.mouse.release(button)
            elif event['event'] == 'scroll':
                pyautogui.scroll(-event['dy']) 
                # self.mouse.scroll(event['dx'], event['dy'])
            elif event['event'] == 'keypress':
                key = event['key']
                if len(key) > 1 and key.startswith('Key.'):
                    key = getattr(Key, key.split('.')[1])
                self.keyboard.press(key)
            elif event['event'] == 'keyrelease':
                key = event['key']
                if len(key) > 1 and key.startswith('Key.'):
                    key = getattr(Key, key.split('.')[1])
                self.keyboard.release(key)
        print("Script Ended")


    def play(self, sleep=0):
        time.sleep(sleep)
        print("Playing script => "+str(self.filename))
        runThread = threading.Thread(target=self.worker, args=())
        runThread.start()

    def pause(self):
        if self.status == 0:
            return
        self.pauseTime = datetime.now()
        self.status = 0
        print("Paused")
    
    def resume(self):
        if self.status == 1:
            return
        self.idolTime = self.idolTime + (datetime.now() - self.pauseTime).total_seconds()
        self.status = 1
        print("Resume")

    def toggle(self):
        if self.status == 1:
            self.pause()
        else:
            self.resume()

    def exit(self):
        self.status = -1
        print("Exited")


class VRecorder:
    def __init__(self):
        self.recorder = Recorder()
        self.player = Player()

    def recorderStart(self):
        self.recorder.start()

    def recorderStop(self):
        self.recorder.stop()

    def recorderSave(self, filename='./user_actions.json'):
        self.recorder.save(filename)

    def recorderStopAndSave(self, filename='./user_actions.json'):
        self.recorder.stopAndSave(filename)

    def playerPlay(self, filename='./user_actions.json'):
        self.player.load(filename)
        self.player.play()
        
    def playerPause(self):
        self.player.pause()

    def playerResume(self):
        self.player.resume()

    def playerToggle(self):
        self.player.toggle()

    def playerExit(self):
        self.player.exit()

    def activateHotkeys(self):
        kb.add_hotkey('ctrl+1', self.recorderStart)
        kb.add_hotkey('ctrl+2', self.recorderStopAndSave)
        kb.add_hotkey('ctrl+3', self.playerPlay)
        kb.add_hotkey('ctrl+4', self.playerToggle)
        kb.add_hotkey('ctrl+5', self.playerExit)
        kb.wait('esc')



# vr = VRecorder()
# vr.activateHotkeys()


# r = Recorder()
# r.start()
# time.sleep(5)
# r.stopAndSave()


# p = Player()
# p.play()
# p.pause()
# p.resume()
# p.exit()