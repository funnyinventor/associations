import streamlit as st
import geocoder
import requests

def main():
    st.title("Cherchez les associations près de chez vous !")
    st.header("Bienvenue !")
    keyword = st.text_input("Entrez le mot clé")
    if st.button("Localiser"):
        location = get_location()
        st.write(f"Localisation : {location}")
        associations = get_associations(location)
        st.subheader("Associations :")
        for assoc in associations:
            st.write(f"Titre: {assoc['titre']}")
            st.write(f"Objet: {assoc['objet']}")
            st.write(f"Adresse: {assoc['adresse_gestion_libelle_voie']}")
            st.write("---")

    if st.button("Rechercher"):
        associations = get_associations(keyword)
        st.subheader("Associations :")
        for assoc in associations:
            st.write(f"Titre: {assoc['titre']}")
            st.write(f"Objet: {assoc['objet']}")
            st.write(f"Adresse: {assoc['adresse_gestion_libelle_voie']}")
            st.write("---")

def get_location():
    g = geocoder.ip('me')
    if g.city:
        return g.city
    else:
        return "Localisation inconnue"

def get_associations(keyword):
    url = f"https://entreprise.data.gouv.fr/api/rna/v1/full_text/{keyword}"
    response = requests.get(url)
    if response.ok and response.status_code == 200:
        data = response.json()
        associations = data.get("association", [])
        associations_info = []
        for assoc in associations:
            titre = assoc.get("titre", "")
            objet = assoc.get("objet", "")
            adresse = assoc.get("adresse_gestion_libelle_voie", "")
            associations_info.append(f"Titre: {titre}\nObjet: {objet}\nAdresse: {adresse}")
        return associations
    else:
        return []

if __name__ == '__main__':
    main()
