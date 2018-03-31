# daliu.github.io


import importlib
STOPWORDS = ['i', 'me', 'my', 'myself', 'we', 'our',
             'ours', 'ourselves', 'you', 'your', 'yours',
             'yourself', 'yourselves', 'he', 'him', 'his',
             'himself', 'she', 'her', 'hers', 'herself',
             'it', 'its', 'itself', 'they', 'them', 'their',
             'theirs', 'themselves', 'what', 'which', 'who',
             'whom', 'this', 'that', 'these', 'those', 'am',
             'is', 'are', 'was', 'were', 'be', 'been', 'being',
             'have', 'has', 'had', 'having', 'do', 'does', 'did',
             'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or',
             'because', 'as', 'until', 'while', 'of', 'at', 'by',
             'for', 'with', 'about', 'against', 'between', 'into',
             'through', 'during', 'before', 'after', 'above', 'below',
             'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over',
             'under', 'again', 'further', 'then', 'once', 'here', 'there',
             'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each',
             'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
             'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's',
             't', 'can', 'will', 'just', 'don', 'should', 'now']


class SenticWord(object):
    """
    Python Interface for Words/Concepts in Senticnet4
    """
    def __init__(self, language="en"):
        data_module = importlib.import_module("sentic.babel.data_" + language)
        self.data = data_module.senticnet

    def info(self, concept = ""):
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

    def get_sentics(self, concept = ""):
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

    def get_moodtags(self, concept = ""):
        """
        :param concept: phrase/word to examine
        :return list: moodtags of a concept.
        """
        concept = concept.replace(" ", "_")
        concept_info = self.data[concept]
        return concept_info[4:6]

    def get_sentiment(self, concept = ""):
        """
        :param concept: phrase/word to examine
        :return string: sentiment of a concept.
        """
        concept = concept.replace(" ", "_")
        concept_info = self.data[concept]
        return concept_info[6]

    def get_polarity(self, concept = ""):
        """
        :param concept: phrase/word to examine
        :return float: polarity of a concept, scaled from -1 (most negative) to 1 (most positive)
        """
        concept = concept.replace(" ", "_")
        concept_info = self.data[concept]
        try:
            return float(concept_info[7])
        except ValueError:
            return 0

    def get_semantics(self, concept = ""):
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
    def __init__(self, text, language = "en", stopwords = True):
        super().__init__(language)
        if stopwords:
            self.text = ''.join([word for word in text.lower() if word not in STOPWORDS])
        else:
            self.text = text.lower()

        self.is_phrase = True if text in self.data else False
        self.results = self.info(text)

    def info(self, text = ""):
        # Prevent repeated computations
        if not text:
            if not self.results:
                text = self.text
            else:
                return self.results

        result = {}
        result["sentics"] = self.get_sentics(text)
        result["moodtags"] = self.get_moodtags(text)
        result["sentiment"] = self.get_sentiment(text)
        result["polarity"] = self.get_polarity(text)
        result["semantics"] = self.get_semantics(text)

        return result

    def get_sentics(self, text = ""):
        """
        :param text: the input string
        :return: Averaged values cross all sentics in text
        """
        if not text:
            text = self.text

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


    def get_moodtags(self, text = ""):
        """
        :param text: the input string
        :return: dictionary of moods with frequency of each in the text.
        """
        if not text:
            text = self.text

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


    def get_polarity(self, text = ""):
        """
        If text is in senticnet, use SenticWord method. Otherwise, use a cumulative average.
        :param text: the input string
        :return: 
        """
        if not text:
            text = self.text

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

            if total_phrases:
                return sum_polarity / total_phrases
            else:
                return 0

    def get_sentiment(self, text = ""):
        """
        :param text: the input string
        :return: sentiment of word or cumulative average across text
        """
        if not text:
            text = self.text

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


    def get_semantics(self, text = "", limit = -1):
        """
        If text is in senticnet, use SenticWord method. Otherwise, use a cumulative average.
        :param text: the input string
        :param limit: the 
        :return: all relevant semantics
        """
        if not text:
            text = self.text

        if self.is_phrase:
            return super().get_semantics(text)

        else:
            all_semantics = set()
            count = 0
            for word in text.split():

                if count > limit:
                    return all_semantics

                try:
                    all_semantics = all_semantics.union(super().get_semantics(word))
                    count += 1
                except KeyError:
                    continue

            return all_semantics

