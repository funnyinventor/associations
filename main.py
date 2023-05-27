import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock


class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keyword = ""

    def build(self):
        layout = BoxLayout(orientation='horizontal', padding=10, spacing=10)
        keyword_layout = BoxLayout(orientation='vertical', size_hint=(0.3, 1), spacing=10)
        self.input_text = TextInput(hint_text='Entrez le mot clé', multiline=False)
        keyword_layout.add_widget(self.input_text)

        button = Button(text='Rechercher', on_press=self.on_button_press, size_hint=(0.2, None), height=40, pos_hint={'center_x': 0.5})
        keyword_layout.add_widget(button)

        layout.add_widget(keyword_layout)
        result_layout = BoxLayout(orientation='vertical', size_hint=(0.7, 1))

        scroll_view = ScrollView()

        content_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        content_layout.bind(minimum_height=content_layout.setter('height'))

        self.result_label = Label(text='', halign='left', valign='top', text_size=(400, None), size_hint_y=None)
        content_layout.add_widget(self.result_label)

        scroll_view.add_widget(content_layout)

        result_layout.add_widget(scroll_view)
        layout.add_widget(result_layout)

        return layout

    def on_button_press(self, instance):
        self.keyword = self.input_text.text
        if self.keyword:
            self.get_associations()

    def adjust_result_label_height(self, dt):
        self.result_label.height = self.result_label.texture_size[1]

    def get_associations(self):
        response = requests.get(f"https://entreprise.data.gouv.fr/api/rna/v1/full_text/{self.keyword}")
        data = response.json()
        associations = data.get("association", [])
        associations_info = []
        for assoc in associations:
            titre = assoc.get("titre", "")
            objet = assoc.get("objet", "")
            adresse = assoc.get("adresse_gestion_libelle_voie", "")
            associations_info.append(f"Titre: {titre}\nObjet: {objet}\nAdresse: {adresse}")
        self.result_label.text = "Associations :\n\n" + "\n\n".join(associations_info)
        Clock.schedule_once(self.adjust_result_label_height, 0.1)


if __name__ == '__main__':
    MyApp().run()
