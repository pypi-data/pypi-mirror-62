import spacy
from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter
from nltk.sentiment import SentimentIntensityAnalyzer

from sugaroid.brain.constants import GREET
from sugaroid.brain.postprocessor import cosine_similarity, random_response, raw_in, raw_lower_in
from sugaroid.brain.preprocessors import normalize


class MeAdapter(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.chatbot = chatbot
        self.normalized = None
        self.tokenized = None
        self.nlp = spacy.load("en_core_web_sm")

    def can_process(self, statement):
        # TODO Fix this
        self.tokenized = self.nlp(str(statement))

        for i in range(len(self.tokenized)-2):
            print(self.tokenized[i].pos_, self.tokenized[i+1].pos_)
            if self.tokenized[i].pos_ == 'PRON' and self.tokenized[i+1].tag_ == 'VBP':
                return True
        else:
            return False

    def process(self, statement, additional_response_selection_parameters=None):
        response = 'ok'
        confidence = 0

        if raw_in('I', self.tokenized):
            print("I TEST")
            for i in self.tokenized:
                if i.pos_ == 'PROPN':
                    nn = i.text
                    if self.chatbot.username:
                        response = "Are you sure you are {n}? I thought you were {u}".format(n=nn, u=self.chatbot.username)
                        confidence = 0.95
                        self.chatbot.nn = nn
                        self.chatbot.next = 30000000001
                        self.chatbot.next_type = bool
                        self.chatbot.reverse = True
                    else:
                        response = random_response(GREET).format(str(nn).capitalize())
                        confidence = 0.9
                        self.chatbot.username = nn
                elif i.lower_ == 'sugaroid':
                    response = 'Lol! I thought I am Sugaroid. have you lost your mind?'
                    confidence = 0.95
                else:
                    sia = SentimentIntensityAnalyzer()
                    ps = sia.polarity_scores(str(i.sent))
                    confidence = 0.75
                    if ps['neu'] == 1:
                        response = 'Ok! Thats great to hear from you'
                    elif ps['pos'] > ps['neg']:
                        response = 'Yay! I agree to you'
                    else:
                        confidence = 0.2
                        response = 'Think again'
        elif raw_lower_in('you', self.tokenized):
            nn = ''
            for i in self.tokenized:

                if i.pos_ == 'ADJ':
                    confidence = 0.9
                    cos = cosine_similarity([str(i.lower_)], ['sugaroid'])
                    if i.lower_ == 'sugaroid':
                        nn = i.text
                        response = "Yup, that's my name. I am sugaroid"
                        break
                    elif cos > 0.9:
                        response = "Yes, you were close! My name is sugaroid"
                        break
                    else:
                        if i.lower_ in ['human', 'animal', 'bird']:
                            response = 'No, I am not a {adj}. I am a robot'.format(adj=i.lower_)
                        else:
                            response = 'seriously?'
                            confidence = 0.1

                elif i.pos_ == 'PROPN':
                    nn = i.text
                    response = "Nope, I am not {n}, I am sugaroid".format(n=nn)
                    confidence = 0.9

                elif i.tag_ == 'NN':
                    if i.lower_ in ['bot', 'robot', 'computer', 'silicon', 'infant']:
                        response = 'You are right! I am a {}'.format(i.lower_)
                        confidence = 0.9
                    elif i.lower_ in ['human', 'bird', 'animal', 'tree', 'politician', 'player', 'liar', 'priest']:
                        response = 'No way! I can\'t imagine myself to be a {}'.format(i.lower_)
                        confidence = 0.9
                    else:
                        confidence = 0.9
                        sia = SentimentIntensityAnalyzer()
                        ps = sia.polarity_scores(str(i.sent))
                        if ps['neu'] == 1.0:
                            response = 'I will need more time to learn if that actually makes sense with respect to ' \
                                       'myself. '
                        elif ps['pos'] > ps['neg']:
                            response = 'I guess I am {}. Thanks!'.format(i.text)
                        else:
                            response = 'I am not {}! I am Sugaroid'.format(i.lower_)
        else:
            # FIXME : Add more logic here
            response = 'Ok'
            confidence = 0.8

        selected_statement = Statement(response)
        selected_statement.confidence = confidence
        return selected_statement
