import requests
import geocoder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window


class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keyword = ""
        self.location = ""

    def build(self):
        Window.clearcolor = (0.0, 0.2, 0.4, 1.0)  # Couleur de fond bleu roi
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        keyword_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40, spacing=10)
        self.input_text = TextInput(hint_text='Entrez le mot clé', multiline=False)
        keyword_layout.add_widget(self.input_text)

        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40, spacing=10)
        location_button = Button(text='Localiser', on_press=self.get_location, size_hint=(0.5, 1))
        button_layout.add_widget(location_button)

        search_button = Button(text='Rechercher', on_press=self.on_button_press, size_hint=(0.5, 1))
        button_layout.add_widget(search_button)

        result_layout = BoxLayout(orientation='vertical', size_hint=(1, 1))

        scroll_view = ScrollView()

        content_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        content_layout.bind(minimum_height=content_layout.setter('height'))

        self.location_label = Label(text='', halign='left', valign='top', text_size=(400, None), size_hint_y=None)
        content_layout.add_widget(self.location_label)

        self.result_label = Label(text='', halign='left', valign='top', text_size=(400, None), size_hint_y=None)
        content_layout.add_widget(self.result_label)

        scroll_view.add_widget(content_layout)

        result_layout.add_widget(scroll_view)

        layout.add_widget(keyword_layout)
        layout.add_widget(button_layout)
        layout.add_widget(result_layout)

        return layout

    def get_location(self, instance):
        g = geocoder.ip('me')
        if g.city:
            city = g.city
            self.keyword = city
            self.location = city
            self.get_associations()

    def on_button_press(self, instance):
        self.keyword = self.input_text.text
        if self.keyword:
            self.location = self.keyword
            self.get_associations()

    def adjust_result_label_height(self, dt):
        self.location_label.height = self.location_label.texture_size[1]
        self.result_label.height = self.result_label.texture_size[1]

    def get_associations(self):
        response = requests.get(f"https://entreprise.data.gouv.fr/api/rna/v1/full_text/{self.keyword}")
        if response.ok and response.status_code == 200:
            data = response.json()
            associations = data.get("association", [])
            associations_info = []
            for assoc in associations:
                titre = assoc.get("titre", "")
                objet = assoc.get("objet", "")
                adresse = assoc.get("adresse_gestion_libelle_voie", "")
                associations_info.append(f"Titre: {titre}\nObjet: {objet}\nAdresse: {adresse}")
            self.location_label.text = f"Localisation : {self.location}"
            self.result_label.text = "Associations :\n\n" + "\n\n".join(associations_info)
            Clock.schedule_once(self.adjust_result_label_height, 0.1)
        else:
            self.result_label.text = "Une erreur s'est produite lors de la récupération des données."

    def on_stop(self):
        if self.location:
            print(f"Localisation enregistrée : {self.location}")


if __name__ == '__main__':
    MyApp().run()
