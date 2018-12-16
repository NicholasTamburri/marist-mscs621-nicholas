# This is based on the Single Container Docker Environments tutorial for
# AWS Elastic Beanstalk, together with the IBM Cloud Language Tranlator API

from flask import Flask
from watson_developer_cloud import LanguageTranslatorV3, WatsonApiException

import json
import os


language_translator = LanguageTranslatorV3(
    version='2018-05-01',
    iam_apikey=os.getenv('IAM_APIKEY'),
    url=os.getenv('TRANSLATOR_URL')
)


# print a nice greeting.
def say_hello(username = "World"):
    return '<p>Hello %s!</p>\n' % username


# translate a word.
def translate(word = "hello"):
    try:
        translation = language_translator.translate(
            text=word,
            # model_id='en-it'
            source='en',
            target='it'
        ).get_result()
        
    except WatsonApiException as ex:
        return "Method failed with status code " + str(ex.code)\
            + ": " + ex.message

    return json.dumps(translation, indent=2, ensure_ascii=False)

    
# some bits of text for the page.
header_text = '''
    <html>\n<head> <title>EB Flask Test</title> </head>\n<body>'''
instructions = '''
    <p><em>Hint</em>: This is a RESTful web service! Append a word
    to the URL (for example: <code>/hello</code>) to see the word in
    another language.</p>\n'''
home_link = '<p><a href="/">Back</a></p>\n'
footer_text = '</body>\n</html>'

# EB looks for an 'application' callable by default.
application = Flask(__name__)

# add a rule for the index page.
application.add_url_rule(
    '/', 'index', (lambda: header_text +
    say_hello() + instructions + footer_text))

# add a rule to translate a word.
application.add_url_rule(
    '/<word>', 'translate', (lambda word:
    header_text + translate(word) + home_link + footer_text))

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    # application.debug = True
    application.run(host="0.0.0.0")
