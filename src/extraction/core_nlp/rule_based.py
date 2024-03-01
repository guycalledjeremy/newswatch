"""Rule-based NLP model for news event extarction.
"""

import spacy

from model import NLPModel

class RuleBasedModel(NLPModel):
    """The rule based model parse predicates as events based on linguistic rules.
    """
    
    def __init__(self) -> None:
        """Initiates the rule base model with spacy tokenizer.
        """
        super().__init__()
        self.tokenizer = spacy.load("en_core_web_sm")

    def _is_clause(self, token) -> bool:
        """Checks if the current token is head of a clause.
        """
        return token.dep_[-2:] == 'cl'

    def _is_prep(self, token) -> bool:
        """Checks if the current token is head of a presupposition.
        """
        return token.dep_ == 'prep'

    def _is_mark(self, token) -> bool:
        """Checks if the current token is head of a marker.
        """
        return token.dep_ == 'mark'

    def _is_cc(self, token) -> bool:
        """Checks if the current token is head of a coordinating conjunction.
        """
        return token.dep_ == 'cc'

    def _is_verb(self, token) -> bool:
        """Checks if the current token is head of a adverbial compliments.
        """
        # exclude verb from phrase building, but not if they are clausal/adverbial compliments
        return token.pos_ == 'VERB' and token.dep_ != 'acomp'

    def _is_punc(self, token) -> bool:
        """Checks if the current token is a punctuation that should be filtered out.
        """
        return token.is_sent_end or token.text in [',', ';']

    def _phrase_filter(self, children_tokens: list) -> list:
        """Check the head of the phrase to filter out phrases of particular kinds.

        Args:
            children_tokens: A list of tokens that are children nodes to the current node.

        Returns:
            A list of filtered children tokens based on linguistic rules.
        """
        filtered_children = []
        for child in children_tokens:
            if not self._is_clause(child) and \
                not self._is_prep(child) and \
                not self._is_mark(child) and \
                not self._is_cc(child) and \
                not self._is_verb(child) and \
                not self._is_punc(child):
                filtered_children.append(child)

        return filtered_children

    # To exclude from phrase building:
    # - verb makes up whole phrase
    # - phrases being a subset of another phrase
    def _phrase_builder(self, token) -> str:
        """Build a phrase from a parsed (by spaCy) syntax tree root node.

        Args:
            token: The spacy word token that is the root of a parsed tree.

        Returns:
            A string that represents the built tree.
        """
        # first filter out unwanted phrases in the child nodes
        children = self._phrase_filter(list(token.children))

        if children == []:
            return token.text
        else:
            # initiate a list to store all elements of the outcome phrase for final phrase building
            phrase = ['' for _ in range(len(children) + 1)]

            phrase_counter = 0
            for child_counter, child in enumerate(children):
                # if the root of this phrase is in the middle/beginning of the phrase,
                # find its location, and add the root token
                if child.idx > token.idx and phrase_counter == child_counter:
                    phrase[phrase_counter] = token.text
                    phrase_counter += 1
                    phrase[phrase_counter] = self._phrase_builder(child)
                else:
                    phrase[phrase_counter] = self._phrase_builder(child)
                phrase_counter += 1

            # if the root of this phrase is at the end of the phrase,
            # append the root token to the end of the lits
            # notice that if all children and the root are already accounted for,
            # phrase_counter sould have an extra count
            if (phrase_counter) == len(children):
                phrase[phrase_counter] = token.text

            return ' '.join(phrase)

    def _filter_duplicate_phrases(self, phrases: list) -> list:
        """From a list of phrases, exclude phrases that makes up another phrase.

        Args:
            phrases: A list of phrases that might have duplicate contents.

        Returns:
            A list of phrases without duplicate contents.
        """
        filtered_phrases = []
        for target_phrase in phrases:
            # exclude phrases with only one verb
            if len(target_phrase.split(' ')) == 1:
                pass
            # exclude phrases being a subset of another phrase
            elif any((target_phrase in phrase and target_phrase != phrase) for phrase in phrases):
                pass
            else:
                filtered_phrases.append(target_phrase)

        return filtered_phrases

    def find_events(self, text: str) -> list:
        """Given some text, find the event phrases and return them in a list.

        Args:
            text: A string that is the article to be extracted from.

        Returns:
            A list of extracted events represented as strings.
        """
        # Process the sentence using spaCy
        doc = self.tokenizer(text)

        # Extract verbs and their related nouns
        sub_sentences = []
        for sent in doc.sents:
            # print()
            # print(sent)
            for token in sent:
                # print(f"{token.text} -- {token.pos_} -- {token.dep_} -- {[child.text for child in token.children]}")
                if token.pos_ == "VERB" or token.dep_ == 'ROOT':
                    # print(f"verb: {token.text} \nphrase: {self._phrase_builder(token)}\n")

                    sub_sentences.append(self._phrase_builder(token))

        return self._filter_duplicate_phrases(sub_sentences)

if __name__ == "__main__":
    result = {
    "processed_text": [
        "wall street stocks finished lower on tuesday as apple kicked off its highly anticipated fall event and investors counted down to wednesday's key inflation data.",
        "tech stocks took center stage on tuesday, with apple (aapl) announcing the launch of the iphone 15 at its annual event. apple stock was down 1.7% on the day. that was coupled with building anticipation for the blockbuster arm ipo. the chip designer will close its order book early, by tuesday afternoon; the listing is up to 10 times oversubscribed, reports said."
    ]}

    model = RuleBasedModel()
    for text in result['processed_text']:
        events = model.find_events(model.tokenizer, text)
        for subsentence in events:
            print(f"Subsentence: {subsentence}")

        print()