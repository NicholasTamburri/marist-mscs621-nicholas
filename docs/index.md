# Word Translator
### by Nicholas Tamburri

Word Translator is a plain and simple word translator on the web. All
you need is a word and a language. Try it out
[here](http://language-translator-env.vihuhsbm6k.us-west-2.elasticbeanstalk.com).

Need to know how to spell "mustache" in French? All you need to know
is how to spell `/mustache/en-fr` at the end of your browser's address
field. Wondering if there's an English word for "baguette"?
[This link](http://language-translator-env.vihuhsbm6k.us-west-2.elasticbeanstalk.com/baguette/fr-en)
will suggest one. Want to translate multiple words at once? Use `%20`
[between the words](http://language-translator-env.vihuhsbm6k.us-west-2.elasticbeanstalk.com/between%20the%20words/en-fr).

Word Translator draws its information from the IBM Cloud Language
Translator service. When you visit one of the links in the above
paragraph, the web application makes a call to an IBM Cloud API with
the given text and translation model. The above links translate
between English and French, but there are many other models for
translating between many other languages. You can find them all listed on
the app's home page.
