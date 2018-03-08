# Sentic

Python Interface for Semantic and Sentiment Analysis using Senticnet4 (http://sentic.net/).


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
{'sentics': {'aptitude': 0.062, 'attention': 0.3695, 'pleasantness': 0.47050000000000003, 'sensitivity': 0.0115}, 'semantics': {'furry', 'labor', 'nocturnal', 'career', 'animal_furry', 'hairy', 'police_work', 'task', 'domestic_pet', 'employment'}, 'moodtags': {'#joy': 2, '#interest': 1, '#admiration': 1}, 'sentiment': 'weak positive', 'polarity': 0.29700000000000004}

>>> sp.get_sentics(text)
{'aptitude': 0.062, 'attention': 0.3695, 'pleasantness': 0.47050000000000003, 'sensitivity': 0.0115}

>>> sp.get_moodtags(text)
{'#joy': 2, '#interest': 1, '#admiration': 1}

>>> sp.get_sentiment(text)
'weak positive'

>>> sp.get_polarity(text)
0.29700000000000004

>>> sp.get_semantics(text)
{'furry', 'labor', 'nocturnal', 'career', 'animal_furry', 'hairy', 'police_work', 'task', 'domestic_pet', 'employment'}
```

Also, you can use other languages:

```python
from sentic import SenticPhrase
text = 'amour'
sp = SenticPhrase(text, "fr")
print(sp.get_semantics(text))
>>> ['beaucoup_de_fleurs', 'montrer_l’beaucoup_de_fleurs', 'rose', 'donner_des_fleurs']

print(sp.get_moodtags(text))
>>> ['#intérêt', '#admiration']

print(sp.get_sentics(text))
>>> {'aptitude': 0.071, 'sensitivity': 0.025, 'pleasantness': 0.027, 'attention': 0.093}

(Unfortunately, the French dataset and some others languages do not have positive/negative labels.)

print(sp.get_polarity(text))
>>> 0

print(sp.get_sentiment(text))
>>> neutral

You can find all supported languages here: http://sentic.net/api/

## About Senticnet

This framework was adapted from Yuri Malheiros (@yurimalheiros) https://github.com/yurimalheiros/senticnetapi.

SenticNet is an initiative conceived at the MIT Media Laboratory in 2010 within an industrial Cooperative Awards in Science and Engineering (CASE) research project, funded by the UK Engineering and Physical Sciences Research Council (EPSRC) and born from the collaboration between the University of Stirling, the Media Lab, and Sitekit Labs.

Currently, both the SenticNet knowledge base and the SenticNet framework are being maintained and further developed by the Sentic Team, a multidisciplinary research group based at the School of Computer Engineering of Nanyang Technological University in Singapore, but also by many other sentic enthusiasts around the world.

Please acknowledge the authors by citing SenticNet 4 in any research work or presentation containing results obtained in whole or in part through the use of the API:

*E. Cambria, S. Poria, R. Bajpai, and B. Schuller. SenticNet 4: A semantic resource for sentiment analysis based on conceptual primitives. In: COLING, pp. 2666-2677, Osaka (2016) http://sentic.net/senticnet-4.pdf*
