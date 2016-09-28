#!/usr/bin/env python3

# Core concept: HTML doesn't usually contain curly braces.
# Thus, we can read the file "index.html.in" as a very large format string and
# call '.format' on it with the following dictionaries as argument, and we're done.
# PRO: Unmatched strings in the HTML code (i.e., typos in either this or the HTML file)
#      would cause an immediate error.
# CON: Superfluous strings are not detected.
#      Counter-measure: if there's multiple strings for the same ID, hand out counters
#      like '_1_2' (first of two) or '_3_9' (third of nine), so when the overall
#      amount changes, mistakes becomes obvious (either by compilation error or by
#      "wait, why is there a '_8_3'?")
# PRO: Superfluous strings are not detected.
#      (So we can use the same dictionary for both about.html and index.html)

LOREM_IPSUM = '''
    FIXME Ut wisi enim ad minim veniam, quis nostrud exerci tation
    ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo
    consequat. Duis autem vel eum iriure dolor in hendrerit in
    vulputate velit esse molestie consequat, vel illum dolore eu
    feugiat nulla facilisis at vero eros et accumsan et iusto odio
    dignissim qui blandit praesent luptatum zzril delenit augue duis
    dolore te feugait nulla facilisi.
'''

STRINGS_DE = {
    # Appears on both pages
    'index_title': 'Vogelauswahl',
    'about_title': '&Uuml;ber',
    'toggle_nav': 'Navigation ein-/ausblenden',
    'de_active': ' class="active"',  # Must start with a space
    'en_active': '',
    # Appears on index.html only:
    'index_lead': 'Alle Vogelstimmen, die im Rahmen des Projects House of Tweets zur Verf&uuml;gung stehen.',
    'index_function_title': 'Funktionsweise',
    'index_function_1_2':
        'Jedem Bundestagsabgeordneten wurde eine Vogelstimme zugeordnet.'
        ' Diese k&ouml;nnen sie ganz leicht &auml;ndern! Ein Klick auf einen untenstehenden Vogel,'
        ' ein abgesetzter Tweet, und schon erkennen unsere Systeme ihren &Auml;nderungswunsch!',
    'index_function_2_2':
        'Der Tweet muss nur den Vogel und das Hashtag <strong>#HouseOfTweets</strong> enthalten.'
        ' Oder <strong>#Hot</strong>, wem das zu lang ist.',
    'index_list_title': 'Vogelliste',
    # Appears on about.html only:
    'about_lead': 'Wer wir sind, wor&uuml;ber dieses Projekt geht, und unsere Sponsoren.',
    'about_concept': 'Konzept',
    'about_concept_text_1_2': LOREM_IPSUM,
    'about_concept_text_2_2': LOREM_IPSUM,
    'about_sponsors': 'Sponsoren',
    'about_sponsors_text': LOREM_IPSUM,
    'about_team': 'Das Team hinter House of Tweets',
    'about_team_text': LOREM_IPSUM,
    'about_copyright': 'Copyright-Hinweise',
    'about_copyright_html': '<p>FIXME &quot;Attributions&quot; &uuml;ber Vogelbilder (auto-gen?)</p>',
    # Appears only in HTML-comment
    'about_thanks': 'Danksagung',
    'about_thanks_text':
        'Wir danken Bootstrap, Github Pages, CoffeeScript, Wikipedia und NodeJS'
        ' f&uuml;r diese wundervollen Projekte!',
}

STRINGS_EN = {
    # Appears on both pages
    'index_title': 'Bird selection',
    'about_title': 'About',
    'toggle_nav': 'Toggle navigation',
    'de_active': '',
    'en_active': ' class="active"',  # Must start with a space
    # Appears on index.html only:
    'index_lead': 'All bird voices that can be selected, in the context of the project House of Tweets.',
    'index_function_title': 'How it works',
    'index_function_1_2':
        'Each member of the parliament has been assigned a bird\'s voice.'
        ' You can easily change that! A single click on one of the birds below,'
        ' a Tweet sent, and our systems recognize your preferences!',
    'index_function_2_2':
        'Your Tweet only needs to contain the name of the bird and the hashtag <strong>#HouseOfTweets</strong>.'
        ' Or <strong>#Hot</strong>, if that\'s too long for you.',
    'index_list_title': 'List of recognised birds',
    # Appears on about.html only:
    'about_lead': 'Who we are, what this project is about, and our sponsors.',
    'about_concept': 'Concept',
    'about_concept_text_1_2': LOREM_IPSUM,
    'about_concept_text_2_2': LOREM_IPSUM,
    'about_sponsors': 'Sponsors',
    'about_sponsors_text': LOREM_IPSUM,
    'about_team': 'The Team behind House of Tweets',
    'about_team_text': LOREM_IPSUM,
    'about_copyright': 'Copyright notices',
    'about_copyright_html': '<p>FIXME &quot;Attributions&quot; &uuml;ber Vogelbilder (auto-gen?)</p>',
    # Appears only in HTML-comment
    'about_thanks': 'Thanks',
    'about_thanks_text':
        'We thank Bootstrap, Github Pages, CoffeeScript, Wikipedia and NodeJS'
        ' for their awesome projects!',
}

assert STRINGS_DE.keys() == STRINGS_EN.keys()


def generate(slug):
    with open(slug + '.html.in', 'r') as fp:
        fmt = fp.read()
    page = fmt.format(**STRINGS_DE)
    with open('autogen/' + slug + '.html', 'w') as fp:
        fp.write(page)
    page = fmt.format(**STRINGS_EN)
    with open('autogen/' + slug + '_en.html', 'w') as fp:
        fp.write(page)


if __name__ == '__main__':
    generate('index')
    generate('about')
