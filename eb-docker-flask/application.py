# This is based on the Single Container Docker Environments tutorial for
# AWS Elastic Beanstalk, together with the IBM Cloud Language Translator API.
#
# https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/single-container-docker.html
# https://cloud.ibm.com/apidocs/language-translator?language=python

from flask import Flask, request
from watson_developer_cloud import LanguageTranslatorV3, WatsonApiException

import json
import os


language_translator = LanguageTranslatorV3(
    version='2018-05-01',
    iam_apikey=os.getenv('IAM_APIKEY'),
    url=os.getenv('TRANSLATOR_URL')
)

languages = language_translator.list_identifiable_languages().get_result()
languages_str = ''
for lang in languages['languages']:
    languages_str += '{} - {}<br>'.format(lang['language'], lang['name'])

models = language_translator.list_models().get_result()
model_names = [model['name'] for model in models['models']]
model_names.sort()
models_str = ''
for model in model_names:
    models_str += model + '<br>'
model_dropdown = '<select name="model" id="model">'
for model in model_names:
    if model == 'en-es':
        model_dropdown += '<option value="{0}" selected>{0}</option>'.format(
            model)
    else:
        model_dropdown += '<option value="{0}">{0}</option>'.format(model)
model_dropdown += '</select>'


# translate a word.
def translate(word, model):
    try:
        translation = language_translator.translate(
            text=word,
            model_id=model
        ).get_result()
        
    except WatsonApiException as ex:
        return "Method failed with status code " + str(ex.code)\
            + ": " + ex.message

    # return json.dumps(translation, indent=2, ensure_ascii=False)
    return translation['translations'][0]['translation']

    
# some bits of text for the page.
header_text = '''
    <html>\n<head> <title>EB Flask Test</title> </head>\n<body>'''

intro = '<p>Welcome to the word translator!</p>\n'

instructions = '''
    <p><em>Hint</em>: This is a RESTful web service! Append a word and model
    to the URL (for example: <code>/hello/en-es</code>) to see the word in
    another language. Alternatively, you may use the form.</p>\n

    <p>A model is <code>&ltsource&gt-&lttarget&gt</code> where &ltsource&gt is
    the code of the language to translate from and &lttarget&gt is the code of
    the language to translate to. The available langauge codes and models are
    listed below.</p>\n'''

form = '''
    <form action="/form-translate" method="post">
    <label for="word">Word to translate:</label>
    <input name="word" id="word" value="hello">
    <label for="model">Model:</label> {}
    <input type="submit" value="Translate">
    </form>'''.format(model_dropdown)

table = '''<table><tr><th>Language codes</th><th>Models</th></tr>
    <tr><td>{}</td><td>{}</td></tr></table>'''.format(
    languages_str, models_str)

home_link = '<p><a href="/">Back</a></p>\n'

footer_text = '</body>\n</html>'

# EB looks for an 'application' callable by default.
application = Flask(__name__)

# add a rule for the index page.
application.add_url_rule(
    '/', 'index', (lambda: header_text +
    intro + instructions + form + table + footer_text))

# add a rule to translate a word.
application.add_url_rule(
    '/<word>/<model>', 'translate', (lambda word, model:
    header_text + translate(word, model) + home_link + footer_text))

# add a rule to translate a word using the form
def form_translate():
    if request.headers.get('Content-Type')\
            == 'application/x-www-form-urlencoded':
        return header_text + translate(request.form['word'],
                                       request.form['model'])\
            + home_link + footer_text
application.add_url_rule(
    '/form-translate', 'form_translate', form_translate, methods=['POST'])

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    # application.debug = True
    application.run(host="0.0.0.0")
