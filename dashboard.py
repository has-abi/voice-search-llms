import logging
import json

import pandas as pd
import streamlit as st
from streamlit_mic_recorder import mic_recorder

from src.transcribe import Transcribe
from src.parser import Parser
from src.pandas_search import PandasSearch

search_text = ""
parsed_filters = {}

@st.cache_data
def load_profiles():
    with open("data/profiles.json", "r", encoding="UTF-8") as f:
        return json.load(f)

all_profiles = load_profiles()
profiles_pd = pd.DataFrame.from_dict(all_profiles)

st.title("Recherche de profils par voix 🎙️")
st.markdown("Rechercher avec la localisation, le niveau d'étude, l'expérience, les compétences et les langues parlées.")

audio = mic_recorder(
    start_prompt="Commençer l'enregistrement",
    stop_prompt="Arrêter l'enregistrement",
    just_once=False,
    use_container_width=False,
    format="wav",
    callback=None,
    args=(),
    kwargs={},
    key=None
)

if audio:
    response = Transcribe.transcribe(audio['bytes'])
    if response.status_code == 200:
        json_response = response.json()
        search_text = st.text_area("Votre requête", value=json_response['text'])
    else:
        st.error("Erreur dans la transcription")


if search_text:
    if st.button("Envoyer"):
        try:
            parsed_filters = Parser().parse(search_text)
            st.markdown("**Les filtres de recherche**")
            st.json(parsed_filters)
            st.markdown("### Les profils après l'application des filtres de recherche")
            search_results = PandasSearch(profiles_pd).search(parsed_filters)
            st.dataframe(search_results)
        except Exception as ex:
            print(ex)
            st.error("Erreur dans la structuration de la requête")

st.markdown("### Tous les profils de la base")
st.dataframe(profiles_pd)
