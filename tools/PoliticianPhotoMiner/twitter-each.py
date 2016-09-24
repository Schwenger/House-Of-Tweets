#!/usr/bin/env python3

import json

KNOWN_TWITTER = {
    # Found by fetch-twitter:
    'Inge Höger': 'Scheringer_W',
    'Wolfgang Stefinger': 'StefingerMdB',
    'Florian Oßner': 'Florian_Ossner',
    'Anette Kramme': 'AnetteKramme',
    'Gerd Müller': 'Gerdbillen',
    'Heiko Schmelzle': 'HeikoMaas',
    # Found by hand:
    'Maria Böhmer': 'MariaBoehmer',
    'Susanne Mittag': 'susanne_mittag',
    'Marcus Held': 'MarcusHeld_SPD',
    'Udo Schiefner': 'UdoSchiefner',
    'Katarina Barley': 'katarinabarley',
    'Gabriela Heinrich': 'GaHeinrich',
    'Angelika Glöckner': 'A_Gloeckner',
    'Claudia Roth': 'GreenClaudia',  # Inactive since 2009
    'Franz-Josef Holzenkamp': 'fj_josef',  # Inactive since 2013
    'Astrid Freudenstein': 'dieFreudenstein',
    'Matern von Marschall': 'Von_Marschall',  # Inactive since 2014
}

KNOWN_NEGATIVE = {
    'Petra Crone',
    'Sabine Dittmar',
    'Stephan Albani',
    'Norbert Brackmann',
    'Sybille Benning',
    'Katharina Landgraf',
    'Ursula Groden-Kranich',
    'Norbert Schindler',
    'Christoph Bergner',
    'Fritz Güntzler',
    'André Hahn',  # Too many candidates!
    'Birgit Wöllert',
    'Sabine Poschmann',
    'Pia Zimmermann',  # too many!
    'Norbert Barthle',
    'Peter Ramsauer',
    'Wolfgang Schäuble',  # @WolfgaSchaeuble looks like the real one, but it's inactive anyway.
    'Michelle Müntefering',  # @M_Muentefering, but blocked tweets
    'Rudolf Henke',
    'Ulrich Petzold',  # No tweets since 2013
    'Ole Schröder',
    'Lena Strothmann',
    'Burkhard Blienert',
    'Jeannine Pflugradt',  # Too many similar ones, no exact
    'Andreas Jung',  # Too many
    'Emmi Zeulner',
    'Thomas Stritzl',
    'Martin Pätzold',  # Too many
    'Patricia Lips',  # What the
    'Sylvia Jörrißen',
    'Sascha Raabe',
    'Gernot Erler',  # Curiously, taken by a Russian.
    'Michael Donth',
    'Maria Flachsbarth',
    'Thomas de Maizière',  # Aww
    'Dirk Heidenblut',
    'Iris Ripsam',  # Unsurprisingly
    'Gülistan Yüksel',  # Wow that's many!
    'Axel Knoerig',
    'Ursula Schulte',
    'Frank-Walter Steinmeier',  # Aww
    'Karl A. Lamers',
    'Josef Rief',
    'Sarah Ryglewski',
    'Axel Schäfer',
    'Sabine Weiss',  # Way too many
    'Angela Merkel',  # Aww. 'AngelaMerkeICDU' -- with a capital 'i' not a lower-case 'L'.  I'm wary.
    'Stephan Mayer',  # Oh god
    'Josef Göppel',  # Empty account
    'Detlef Seif',  # Empty account
    'Carola Reimann',  # Two empty accounts (?)
    'Astrid Timmermann-Fechter',
    'Veronika Bellmann',
    'Alois Karl',
    'Daniela De Ridder',  # Full setup,  but no tweets
    'Carsten Linnemann',
    'Karin Evers-Meyer',
    'Reinhold Sendker',
    'Sabine Sütterlin-Waack',
    'Albert Weiler',
    'Andreas G. Lämmel',
    'Philipp Graf Lerchenfeld',  # Aww
    'Hans-Joachim Schabedoth',
    'Thomas Dörflinger',
    'Alexander Funk',
    'Ulrike Gottschalck',
    'Gabriele Lösekrug-Möller',
    'Hendrik Hoppenstedt',  # Früher war mehr Lametta!
    'Gustav Herzog',
    'Karl-Heinz Helmut Wange',
}

with open('converge-each.json', 'r') as fp:
    wikified = json.load(fp)

for e in wikified:
    if 'twittering' in e:
        continue
    name = e['name']
    if name in KNOWN_TWITTER:
        e['twittering'] = {'twitterUserName': KNOWN_TWITTER[name]}
        del KNOWN_TWITTER[name]
    elif name in KNOWN_NEGATIVE:
        KNOWN_NEGATIVE.remove(name)
    else:
        print(name)

assert len(KNOWN_TWITTER) == 0 and len(KNOWN_NEGATIVE) == 0,\
    (KNOWN_TWITTER, KNOWN_NEGATIVE)

with open('twitter-each.json', 'w') as fp:
    json.dump(wikified, fp, sort_keys=True, indent=2)
