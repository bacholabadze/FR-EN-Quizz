class Word:
    def __init__(self, fr_word, en_word):
        self.fr_word = fr_word
        self.en_word = en_word

    def __str__(self):
        return f"{self.fr_word}     -   {self.en_word}"

    def __getitem__(self, item):
        return getattr(self, item)
    # def __dict__(self):
    #     mydict = {"fr_word": self.fr_word,
    #               "en_word": self.en_word}
    #     return mydict


class DetailedWord(Word):
    def __init__(self,fr_word, en_word, word_class, frq_ranking):
        super().__init__(fr_word, en_word)
        self.word_class = word_class
        self.frequency_ranking = str(frq_ranking)

    def __getitem__(self, item):
        return getattr(self, item)

    def __str__(self):
        return f"({self.word_class})[{self.frequency_ranking}] || {self.fr_word}     -   {self.en_word}"

    # def __dict__(self):
    #     mydict = {"fr_word": self.fr_word,
    #               "en_word": self.en_word,
    #               "word_class": self.word_class,
    #               "frequency_ranking": self.frequency_ranking}
    #     return mydict


# a = DetailedWord("bonjour", "hello", "noun", "1")
# print(a)