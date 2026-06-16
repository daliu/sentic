# Sentic

Python Interface for Semantic and Sentiment Analysis using SenticNet 9 (https://sentic.net/).


## Install

Using pip:

```
$ pip install sentic
```

Using the repository code:

```
$ python setup.py install
```

## How to use

```python
from sentic import SenticPhrase
text = "Shirley is such a cute girl."
sp = SenticPhrase(text)
sp.info(text)
>>> {'sentics': {'pleasantness': 0.0, 'attention': 0.0, 'sensitivity': 0.995, 'aptitude': 0.0}, 'moodtags': {'#delight': 1}, 'sentiment': 'strong positive', 'polarity': 0.995, 'semantics': {'aww', 'adore', 'petite', 'beaut', 'kute'}}

>>> sp.get_sentics(text)
{'pleasantness': 0.0, 'attention': 0.0, 'sensitivity': 0.995, 'aptitude': 0.0}

>>> sp.get_moodtags(text)
{'#delight': 1}

>>> sp.get_sentiment(text)
'strong positive'

>>> sp.get_polarity(text)
0.995

>>> sp.get_semantics(text)
{'aww', 'adore', 'petite', 'beaut', 'kute'}
```

Additionally, if you want to, you can just use the same SenticPhrase class object to make method calls on other bodies of text. This manner of functionality was introduced because creating new objects for every different body of text could be cumbersome and memory-inefficient.

```python
# Word not in Sentic word set
>>> sp.info("asdkfjalsfknqsf")
{'sentics': {}, 'moodtags': {}, 'sentiment': 'neutral', 'polarity': 0, 'semantics': set()}

>>> sp.info("Humans are such an interesting species.")
{'sentics': {'pleasantness': 0.0, 'attention': 0.0, 'sensitivity': 0.659, 'aptitude': 0.0}, 'moodtags': {'#pleasantness': 1}, 'sentiment': 'strong positive', 'polarity': 0.659, 'semantics': {'plot_twist', 'food_for_thought', 'fond', 'appreciate', 'get_eyeball'}}

>>> sp.get_polarity("Use same object to get polarity on another text")
0.953
```

Also, you can use other languages:

```python
from sentic import SenticPhrase
text = 'amour'
sp = SenticPhrase(text, "fr")
sp.get_semantics()
>>> [‘ramjet’, ‘economiste_hellenique’, ‘armuriere’, ‘job_explore’, ‘rayonnant’]

sp.get_moodtags()
>>> [‘#joy’, ‘#pleasantness’]

sp.get_sentics()
>>> {‘pleasantness’: 0.659, ‘attention’: 0, ‘sensitivity’: 0.659, ‘aptitude’: 0}

(In SenticNet 9, mood tags are standardized in English across all languages, and every language now carries polarity labels.)

sp.get_polarity()
>>> 0.659

sp.get_sentiment()
>>> strong positive
```

You can find all supported languages here: http://sentic.net/api/

## About Senticnet

This framework was adapted from Yuri Malheiros (@yurimalheiros) https://github.com/yurimalheiros/senticnetapi.

SenticNet is an initiative conceived at the MIT Media Laboratory in 2010 within an industrial Cooperative Awards in Science and Engineering (CASE) research project, funded by the UK Engineering and Physical Sciences Research Council (EPSRC) and born from the collaboration between the University of Stirling, the Media Lab, and Sitekit Labs.

Currently, both the SenticNet knowledge base and the SenticNet framework are being maintained and further developed by the Sentic Team, a multidisciplinary research group based at the School of Computer Engineering of Nanyang Technological University in Singapore, but also by many other sentic enthusiasts around the world.

Please acknowledge the authors by citing SenticNet 9 in any research work or presentation containing results obtained in whole or in part through the use of the API:

*E Cambria, R Mao, X Zhang, L Xiao, T Shen, A Anand. SenticNet 9: Generative Commonsense for Emotion AI via Conceptual Primitive Discovery and Time Shift Mechanism. IEEE Transactions on Computational Social Systems 13 (2026)*

## License

Copyright © 2026 SenticNet.

This software is provided for **non-commercial use only**. Commercial use — including selling, licensing, sublicensing, offering paid services, or integrating the Software into commercial products or services — is permitted only for users who hold an active [Sentic Membership](https://sentic.net/), or who obtain prior written permission from the copyright holder. See the [LICENSE](LICENSE) file for the full terms.
