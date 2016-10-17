#!/usr/bin/env python3

import html
import json

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
    'nav_toggle': 'Navigation ein-/ausblenden',
    'nav_index': 'index.html',
    'nav_about': 'about.html',
    'nav_index_de': '#',
    'nav_about_de': '#',
    'nav_index_en': 'index_en.html',
    'nav_about_en': 'about_en.html',
    'de_active': ' class="active"',  # Must start with a space
    'en_active': '',
    # Appears on index.html only:
    'index_lead': 'Alle Vogelstimmen, die im Rahmen des Projekts House of Tweets zur Verf&uuml;gung stehen.',
    'index_function_title': 'Funktionsweise',
    'index_function_1_2':
        'Jedem Bundestagsabgeordneten wurde eine Vogelstimme zugeordnet.'
        ' Diese k&ouml;nnen sie ganz leicht &auml;ndern! Ein Klick auf einen der nachfolgenden Vögel,'
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
    # 'about_copyright_html': AUTOGENERATED
    # Copyright strings:
    'copyright_pre': 'Wir danken den folgenden Fotografen f&uuml;r die herrlichen Vogelbilder:',
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
    'nav_toggle': 'Toggle navigation',
    'nav_index': 'index_en.html',
    'nav_about': 'about_en.html',
    'nav_index_de': 'index.html',
    'nav_about_de': 'about.html',
    'nav_index_en': '#',
    'nav_about_en': '#',
    'de_active': '',
    'en_active': ' class="active"',  # Must start with a space
    # Appears on index.html only:
    'index_lead': 'All bird voices that can be selected, in the context of the project House of Tweets.',
    'index_function_title': 'How it works',
    'index_function_1_2':
        'Each member of the parliament has been assigned a bird\'s voice.'
        ' You can easily change that! A single click on one of the birds below,'
        ' a Tweet sent, and our systems recognise your preferences!',
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
    # 'about_copyright_html': AUTOGENERATED
    # Copyright strings:
    'copyright_pre': 'We thank the following photographers for their great images:',
    # Appears only in HTML-comment
    'about_thanks': 'Thanks',
    'about_thanks_text':
        'We thank Bootstrap, Github Pages, CoffeeScript, Wikipedia and NodeJS'
        ' for their awesome projects!',
}

assert STRINGS_DE.keys() == STRINGS_EN.keys()

# Technically, I have to properly URI-component-escape the bid string.
# Factually, I know that it's just plain ascii, so there's nothing to do.
# FIXME: Properly share resources between this python code and the generating JS code.
BIRD_HTML_TEMPLATE = """<div class="col-xs-12 col-sm-6 col-md-4 col-lg-3 text-center">
          <div class="bird-entry">
            <div class="bird-image">
              <img src="imgs/{bid}.jpg" alt="{display}"/>
            </div>
            <div class="caption">
              <span class="caption-text">{display}</span>
              <a class="tw-widget" href="https://twitter.com/intent/tweet?text={tweet}&button_hashtag=HouseOfTweets">
                <span class="tw-img"></span>
                <span class="tw-label"> Tweet </span>
              </a>
            </div>
          </div>
        </div>
        """


def generate(slug):
    with open(slug + '.html.in', 'r') as fp:
        fmt = fp.read()
    page = fmt.format(**STRINGS_DE)
    with open('autogen/' + slug + '.html', 'w') as fp:
        fp.write(page)
    page = fmt.format(**STRINGS_EN)
    with open('autogen/' + slug + '_en.html', 'w') as fp:
        fp.write(page)


# Returns a list of lists of bird-entries, aggregated by their copyright holder
# Sorted by copyright-holder's name, birds "unsorted".
def birds_by_name(birds):
    by_name = dict()
    for bird in birds:
        holder = bird['copyright']
        if holder in by_name:
            entry = by_name[holder]
        else:
            entry = {'holder': holder, 'birds': []}
            by_name[holder] = entry
        entry['birds'].append(bird)
    sorted_by_name = list(sorted(by_name.values(), key=lambda e: e['holder']))
    return sorted_by_name


def html_escape(s):
    return html.escape(s).encode('ascii', 'xmlcharrefreplace').decode()


def spoof_copyright_single(entry, lang: str):
    holder = entry['holder']
    name_key = lang + '_name'
    sorted_birds = list(sorted(entry['birds'], key=lambda x: x[name_key]))
    birds = ', '.join(['{} ({})'.format(bird[name_key], bird['license'])
                       for bird in sorted_birds])
    content = '{}: {}'.format(holder, birds)
    return '<li>{}</li>'.format(html_escape(content))


def spoof_copyright(by_name, lang):
    return '\n      '.join([spoof_copyright_single(entry, lang) for entry in by_name])


def spoof_bird(bid, display_name, tweet_name):
    return BIRD_HTML_TEMPLATE.format(bid=bid, display=html_escape(display_name), tweet=html_escape(tweet_name))


def run():
    with open('../tools/PhotoMiner/checkout_pubweb_birds.json', 'r') as fp:
        birds = json.load(fp)
    by_name = birds_by_name(birds)
    for strings, lang in [(STRINGS_DE, 'de'), (STRINGS_EN, 'en')]:
        strings['about_copyright_html'] = spoof_copyright(by_name, lang)
        with open('birds_' + lang + '_init.json', 'r') as fp:
            init_birds = json.load(fp)
        strings['index_init_content'] = ''.join([spoof_bird(bid, display_name, tweet_name)
                                                 for bid, display_name, tweet_name in init_birds])

    # FIXME: Spoof "init" images properly
    generate('index')
    generate('about')


if __name__ == '__main__':
    run()
