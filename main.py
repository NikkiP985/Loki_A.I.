from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
import re

try:
    from jnius import autoclass
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
    Locale = autoclass('java.util.Locale')
except:
    PythonActivity = None
    TextToSpeech = None
    Locale = None

class LokiApp(App):
    def build(self):
        self.memory = []
        self.tts = None

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.output_label = Label(text="LOKI online. What mischief shall we cause?", size_hint_y=0.7)
        self.layout.add_widget(self.output_label)

        self.input_box = TextInput(hint_text="Type here...", multiline=False, size_hint_y=0.1)
        self.layout.add_widget(self.input_box)

        self.button = Button(text="Send", size_hint_y=0.2)
        self.button.bind(on_press=self.respond)
        self.layout.add_widget(self.button)

        if PythonActivity and TextToSpeech:
            self.tts = TextToSpeech(PythonActivity.mActivity, None)
            self.tts.setLanguage(Locale.US)

        return self.layout

    def respond(self, instance):
        user_input = self.input_box.text.strip()
        self.input_box.text = ""

        if not user_input:
            return

        self.memory.append(user_input)

        reply = self.generate_reply(user_input)

        self.output_label.text = f"You: {user_input}\nLOKI: {reply}"

        if self.tts:
            self.tts.speak(reply, TextToSpeech.QUEUE_FLUSH, None)

    def generate_reply(self, user_input):
        user_input_lower = user_input.lower()

        if any(word in user_input_lower for word in ["hi", "hello", "hey", "greetings"]):
            return "Ah, you greet a god. Bold."

        if "thank" in user_input_lower:
            return "Flattery will get you everywhere."

        if any(word in user_input_lower for word in ["stupid", "dumb", "idiot"]):
            return "Careful. I have a long memory, mortal."

        if "who are you" in user_input_lower:
            return "I am LOKI, the Launching Obviously Kindred Intelligence. Your digital trickster."

        if "memory" in user_input_lower:
            return f"I recall: {', '.join(self.memory[-5:])}"

        match = re.search(r'calc (.+)', user_input_lower)
        if match:
            expr = match.group(1)
            try:
                result = self.safe_eval(expr)
                return f"The answer is {result}."
            except:
                return "Even gods stumble on bad equations."

        return "Fascinating. I'm trembling with excitement."

    def safe_eval(self, expr):
        if re.fullmatch(r'[\d+\-*/(). ]+', expr):
            return eval(expr)
        else:
            raise ValueError("Unsafe expression")

if __name__ == "__main__":
    LokiApp().run()
