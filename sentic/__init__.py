# daliu.github.io

import importlib


class SenticWord(object):
    """
    Python Interface for Words/Concepts in Senticnet4
    """
    def __init__(self, language="en"):
        data_module = importlib.import_module("senticnet.babel.data_" + language)
        self.data = data_module.senticnet

    def info(self, concept):
        """
        Return all the information about a concept: semantics,
        sentics and polarity.
        :return dict:
        """
        result = {}
        result["sentics"] = self.get_sentics(concept)
        result["moodtags"] = self.get_moodtags(concept)
        result["sentiment"] = self.get_sentiment(concept)
        result["polarity"] = self.get_polarity(concept)
        result["semantics"] = self.get_semantics(concept)
        return result

    def get_sentics(self, concept):
        """
        :return dict: sentics(pleasantness, attention, sensitivity, aptitude) of a concept.
        """
        concept = concept.replace(" ", "_")
        concept_info = self.data[concept]

        sentics = {"pleasantness": concept_info[0],
                   "attention": concept_info[1],
                   "sensitivity": concept_info[2],
                   "aptitude": concept_info[3]}
        return sentics

    def get_moodtags(self, concept):
        """
        :param concept: phrase/word to examine
        :return list: moodtags of a concept.
        """
        concept = concept.replace(" ", "_")
        concept_info = self.data[concept]
        return concept_info[4:6]

    def get_sentiment(self, concept):
        """
        :param concept: phrase/word to examine
        :return string: sentiment of a concept.
        """
        concept = concept.replace(" ", "_")
        concept_info = self.data[concept]
        return concept_info[6]

    def get_polarity(self, concept):
        """
        :param concept: phrase/word to examine
        :return float: polarity of a concept, scaled from -1 (most negative) to 1 (most positive)
        """
        concept = concept.replace(" ", "_")
        concept_info = self.data[concept]
        return float(concept_info[7])

    def get_semantics(self, concept):
        """
        :param concept: phrase/word to examine
        :return list: Phrases/words associated with 
        """
        concept = concept.replace(" ", "_")
        concept_info = self.data[concept]
        return concept_info[8:]




class SenticPhrase(SenticWord):
    """
    An interface for blocks of text, holding/retrieving info.
    We use self.is_phrase to postpone throwing KeyError too soon, when evaluating large block of text.
    We also use a 'total' counter sometimes because results may be skewed from non-words like '1, 2, 3...' etc
    """
    def __init__(self, text, language="en"):
        super().__init__(language)
        self.text = text
        self.is_phrase = True if text in self.data else False


    def get_sentics(self, text):
        """
        :param text: the input string
        :return: Averaged values cross all sentics in text
        """
        if self.is_phrase:
            return super().get_sentics(text)
        else:
            lst_of_sentics = {}
            total_phrases = 0.0
            for word in text.split():
                try:
                    sentic_values = super().get_sentics(word)
                    total_phrases += 1
                    for sentic in sentic_values:
                        lst_of_sentics[sentic] = lst_of_sentics.get(sentic, 0) + float(sentic_values[sentic])
                except KeyError:
                    continue

            for s in lst_of_sentics:
                if total_phrases:
                    lst_of_sentics[s] /= total_phrases

            return lst_of_sentics


    def get_moodtags(self, text):
        """
        :param text: the input string
        :return: dictionary of moods with frequency of each in the text.
        """
        if self.is_phrase:
            return super().get_moodtags(text)
        else:
            mood_frequencies = {}
            for word in text.split():
                moods = {}
                try:
                    for mood in super().get_moodtags(word):
                        mood_frequencies[mood] = mood_frequencies.get(mood, 0) + 1
                except KeyError:
                    continue

            return mood_frequencies


    def get_polarity(self, text):
        """
        If text is in senticnet, use SenticWord method. Otherwise, use a cumulative average.
        :param text: the input string
        :return: 
        """
        if self.is_phrase:
            return super().get_polarity(text)
        else:
            sum_polarity = 0
            total_phrases = 0.0
            for word in text.split():
                try:
                    sum_polarity += super().get_polarity(word)
                    total_phrases += 1
                except KeyError:
                    continue

            return sum_polarity / total_phrases

    def get_sentiment(self, text):
        """
        :param text: the input string
        :return: sentiment of word or cumulative average across text
        """
        polarity = self.get_polarity(text)
        if polarity > .5:
            return 'strong positive'
        elif polarity > .05:
            return 'weak positive'
        elif polarity > -.05:
            return 'neutral'
        elif polarity > -.05:
            return 'weak negative'
        else:
            return 'strong negative'


    def get_semantics(self, text, limit = -1):
        """
        If text is in senticnet, use SenticWord method. Otherwise, use a cumulative average.
        :param text: the input string
        :return: all relevant semantics
        """
        if self.is_phrase:
            return super().get_semantics(text)
        else:
            all_semantics = set()
            for word in text.split():
                associations = {}
                try:
                    all_semantics = all_semantics.union(super().get_semantics(word))
                except KeyError:
                    continue

            return all_semantics
            


