"""GPT-based model for news event extraction.
"""

import ast
import os

from openai import OpenAI

from core_nlp.model import NLPModel
class GPTModel(NLPModel):
    """The gpt-based model utilizes conversational ai's pre-traiend LLM to extract events from news.
    """

    def __init__(self, model_name: str="gpt-4-turbo-preview") -> None:
        """Initiates the openai client.

        Args:
            model_name: The name of the GPT model to be used, 'gpt-4-turbo-preview' by default. Alternative: 'gpt-3.5-turbo'.
        """
        self.client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY")
        )
        self.model_name = model_name

    def _get_prompt(self, text: str, keyword: str) -> str:
        """Generates prompt for event extraction given a text paragraph.

        Args:
            text: A string representation of the text to be extracted from.
            keyword: A string representation of the keyword that the event extraction is about.

        Returns:
            A string representation of the prompt to be sent to the GPT model.
        """
        text_block = f"I have selected paragraph(s) from a news article: {text}"
        question_block = f"Can you give me a list of events about {keyword} in this article? Please only return results in a list as follow: ['event1', 'event2', ...] without any other textual descriptions, and make sure each event is only 1-2 sentences long."

        return f"{text_block}\n{question_block}"

    def find_events(self, text: str, keyword: str) -> list:
        """Given a sentence, find the event phrases and return them in a list.

        Args:
            text: A string representation of the text to be extracted from.
            keyword: A string representation of the keyword that the event extraction is about.

        Returns:
            A list of string representations of events extracted from text.
        """
        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": self._get_prompt(text, keyword)
                }
            ]
        )

        try:
            return ast.literal_eval(completion.choices[0].message.content)
        except:
            return completion.choices[0].message.content

if __name__ == '__main__':
    test_model = GPTModel()
    test_paragraph = 'the change, which goes into effect later this month, stems from a 2022 app store update where apple extended its typical 30 percent cut of digital purchases to boosted posts, which are essentially ads. the change particularly targeted meta and other social apps that let people pay in app to increase the reach of their content. meta notes in a statement shared with the verge that small business owners and influencers who want to purchase a boost on ios will now be billed through apple, “which retains a 30 percent service charge on the total ad payment, before any applicable taxes.”'
    response = test_model.find_events(test_paragraph)
    print(response)
    print(type(response))