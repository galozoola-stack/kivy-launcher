import os
from kivy.app import App
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

KV = r'''
<EditorRoot>:
    orientation: 'vertical'
    padding: '10dp'
    spacing: '7dp'
    BoxLayout:
        size_hint_y: None
        height: '44dp'
        Label:
            text: 'Python Code Editor'
            bold: True
            font_size: '20sp'
        Button:
            text: 'Paste'
            size_hint_x: None
            width: '75dp'
            on_release: root.paste_clipboard()
        Button:
            text: 'Save'
            size_hint_x: None
            width: '70dp'
            on_release: root.save_code()
    TextInput:
        id: editor
        text: root.initial_code
        hint_text: 'Write Python code here…'
        multiline: True
        font_name: 'RobotoMono'
        font_size: '14sp'
        background_color: 0.08, 0.09, 0.11, 1
        foreground_color: 0.9, 0.93, 0.96, 1
        cursor_color: 0.3, 0.8, 1, 1
        selection_color: 0.2, 0.45, 0.7, 0.8
        padding: '10dp'
    BoxLayout:
        size_hint_y: None
        height: '48dp'
        spacing: '8dp'
        Button:
            text: 'Copy'
            on_release: root.copy_code()
        Button:
            text: 'Run code'
            on_release: root.run_code()
        Button:
            text: 'Clear'
            on_release: root.clear_code()
    Label:
        text: root.status
        size_hint_y: None
        height: '42dp'
        text_size: self.width, None
        halign: 'left'
        valign: 'middle'

EditorRoot:
'''

class EditorRoot(BoxLayout):
    initial_code = 'print("Hello from your code editor!")\n'
    status = 'Ready. Save stores your code on this device.'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.store = JsonStore(os.path.join(App.get_running_app().user_data_dir, 'editor.json'))
        if self.store.exists('document'):
            self.initial_code = self.store.get('document').get('code', self.initial_code)

    def _code(self):
        return self.ids.editor.text

    def copy_code(self):
        from kivy.core.clipboard import Clipboard
        Clipboard.copy(self._code())
        self.status = 'Copied code to clipboard.'

    def paste_clipboard(self):
        from kivy.core.clipboard import Clipboard
        self.ids.editor.insert_text(Clipboard.paste())
        self.status = 'Pasted clipboard text.'

    def save_code(self):
        self.store.put('document', code=self._code())
        self.status = 'Saved locally on this device.'

    def clear_code(self):
        self.ids.editor.text = ''
        self.status = 'Editor cleared.'

    def run_code(self):
        # Executes Python entered by the user. This is not a sandbox: only run trusted code.
        output = []
        def capture_print(*args, **kwargs):
            output.append(' '.join(str(x) for x in args))
        safe_builtins = dict(__builtins__) if isinstance(__builtins__, dict) else vars(__builtins__).copy()
        safe_builtins['print'] = capture_print
        try:
            exec(compile(self._code(), '<editor>', 'exec'), {'__builtins__': safe_builtins}, {})
            self.status = ('\n'.join(output) or 'Code ran successfully (no printed output).')[-500:]
        except Exception as exc:
            self.status = f'{type(exc).__name__}: {exc}'

class CodeEditorApp(App):
    def build(self):
        Builder.load_string(KV)
        return EditorRoot()

if __name__ == '__main__':
    CodeEditorApp().run()
