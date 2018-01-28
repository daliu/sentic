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

sp.get_sentics(text)
sp.get_moodtags(text)
sp.get_sentiment(text)
sp.get_polarity(text)
sp.get_semantics(text)
```

Also, you can use other languages (TODO: EDIT BELOW):

```python
from sentic import SenticPhrase
text = 'amor'
sp = SenticPhrase(text, "pt")

sp.get_sentics(text)
sp.get_moodtags(text)
sp.get_sentiment(text)
sp.get_polarity(text)
sp.get_semantics(text)
```

You can find all supported languages here: http://sentic.net/api/

## About Senticnet

SenticNet is an initiative conceived at the MIT Media Laboratory in 2010 within an industrial Cooperative Awards in Science and Engineering (CASE) research project, funded by the UK Engineering and Physical Sciences Research Council (EPSRC) and born from the collaboration between the University of Stirling, the Media Lab, and Sitekit Labs.

Currently, both the SenticNet knowledge base and the SenticNet framework are being maintained and further developed by the Sentic Team, a multidisciplinary research group based at the School of Computer Engineering of Nanyang Technological University in Singapore, but also by many other sentic enthusiasts around the world.

Please acknowledge the authors by citing SenticNet 4 in any research work or presentation containing results obtained in whole or in part through the use of the API:

*E. Cambria, S. Poria, R. Bajpai, and B. Schuller. SenticNet 4: A semantic resource for sentiment analysis based on conceptual primitives. In: COLING, pp. 2666-2677, Osaka (2016)*
