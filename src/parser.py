from langchain_core.output_parsers import PydanticOutputParser, BaseOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from config import PARSING_API_URL, PARSING_API_KEY
from src.search_query import SearchQuery

PARSING_MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"
PARSING_PARAMS = {
    "max_tokens": 512,
    "temperature": 0,
}


class Parser:
    """Structurer la requête de recherche"""
    def __init__(self):
        self.llm = self._get_lmm()
        self.parser = self._get_parser()
        self.prompt = self._get_template().partial(schema=self.parser.get_format_instructions())
        self.chain = self.prompt | self.llm | self.parser

    def parse(self, query: str) -> SearchQuery:
        return self.chain.invoke({"text": query})

    @staticmethod
    def _get_lmm() -> ChatOpenAI:
        return ChatOpenAI(
            base_url=PARSING_API_URL,
            api_key=PARSING_API_KEY,
            model=PARSING_MODEL,
            max_tokens=PARSING_PARAMS["max_tokens"],
            temperature=PARSING_PARAMS["temperature"],
        )

    @staticmethod
    def _get_template() -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Analyser et extraire les informations pertinentes de la requête de recherche suivante et les structurer selon le schéma ci-dessous en format JSON :\n"
                    "`json\n{schema}\n`\n"
                    "Instructions :\n"
                    "- Niveau d'études : Déterminer le niveau d'éducation (ex. : 'Licence', 'Master', 'Doctorat').\n"
                    "- Expérience : Extraire les années d’expérience minimum et maximum. Si la forme de plus X ans "
                    "est utilisée remplacer mettez la valeur X dans le min et le max null. Le contraire pour la form de moins X ans.\n"
                    "- Compétences : Identifier les compétences techniques et comportementales (ex. : 'Python', 'gestion de projet').\n"
                    "- Langues parlées : Extraire les langues parlées mentionnées dans la requête (ex. : 'Anglais', 'Français', 'Allemand').\n"
                    "- Répondez avec la sortie structurée selon le schéma donné sans explications.\n"
                    "- N'ajoutez pas de \ aux champs du schéma de sortie comme langues\_parlees il faut préserver le format langues_parlees.\n"
                    "- Répondez sans explications."
                ),
                ("human", "{text}"),
            ]
        )

    @staticmethod
    def _get_parser() -> BaseOutputParser:
        return PydanticOutputParser(pydantic_object=SearchQuery)
