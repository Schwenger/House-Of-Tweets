#!/usr/bin/env python3

import html
import json

# Core concept: HTML doesn't usually contain curly braces.
# Thus, we can read the file "birds.html.in" as a very large format string and
# call '.format' on it with the following dictionaries as argument, and we're done.
# PRO: Unmatched strings in the HTML code (i.e., typos in either this or the HTML file)
#      would cause an immediate error.
# CON: Superfluous strings are not detected.
#      Counter-measure: if there's multiple strings for the same ID, hand out counters
#      like '_1_2' (first of two) or '_3_9' (third of nine), so when the overall
#      amount changes, mistakes becomes obvious (either by compilation error or by
#      "wait, why is there a '_8_3'?")
# PRO: Superfluous strings are not detected.
#      (So we can use the same dictionary for both about.html and birds.html)

STRINGS_DE = {
    # Appears on both pages
    'birds_title': 'Vogelauswahl',
    'about_title': '&Uuml;ber',
    'nav_toggle': 'Navigation ein-/ausblenden',
    'nav_index': 'index.html',
    'nav_birds': 'birds.html',
    'nav_about': 'about.html',
    'nav_index_de': '#',
    'nav_birds_de': '#',
    'nav_about_de': '#',
    'nav_index_en': 'index_en.html',
    'nav_birds_en': 'birds_en.html',
    'nav_about_en': 'about_en.html',
    'de_active': ' class="active"',  # Must start with a space
    'en_active': '',
    # Appears on index.html only:
    'index_lead': 'Worum es bei dem Projekt geht',
    'index_concept': 'Konzept',
    'index_concept_text': """
        Bei House of Tweets handelt es sich um eine interdisziplin&auml;re
        und interaktive Klangskulptur f&uuml;r den Deutschen Bundestag.
        <br>
        Jeder Politiker kann sich eine stellvertretende Vogelstimme ausw&auml;hlen,
        die genutzt wird um Tweets auditiv darzustellen. Diese Stimme reflektiert
        dann den Gef&uuml;hlszustand des Politikers beim Tweeten; ein aggresiver Tweet
        wird in einen aggressiven Ton &uuml;bersetzt.
        <br>
        So werden hitzige Bundestagsdebatten zu einem Konzert der V&ouml;gel,
        ein berauschender Mix verschiedener Stimmen, der sich stets &auml;ndert
        und niemals still steht.
        <br>
        Zudem k&ouml;nnen Besucher der Ausstellung den Politikern selbst einen
        passenden Vogel zuweisen und die folgenden Tweets mit den neuen Stimmen erleben.
        <br>
        Sie k&ouml;nnen auch f&uuml;r Ihren eigenen Twitteraccount einen Vogel
        aussuchen und selbst Teil der Ausstellung werden. Ihre Tweets werden nicht
        nur zusammen mit den der Politiker angezeigt, sondern sind auch zu h&ouml;ren
        und tragen zum Klangerlebnis bei.
        """,
    'index_spacetime': 'Ort und Zeit',
    'index_spacetime_text': """
        Die Ausstellung beginnt am Donnerstag, den 18. Mai 2017,
        und findet in der saarl&auml;ndischen Landesvertretung statt.
        <br />
        Die Anschrift lautet:
        <blockquote>
        Die Vertretung des Saarlandes beim Bund <br />
        In den Ministerg&auml;rten 4 <br />
        10117 Berlin <br />
        <a class="quotelink" href="https://www.google.de/maps/place/Berlin+Landesvertretung+Saarland">In Google Maps &ouml;ffnen</a>
        </blockquote>
        """,
    'index_demo': 'Vorschau',
    # Appears on birds.html only:
    'birds_lead': 'Alle Vogelstimmen, die im Rahmen des Projekts House of Tweets zur Verf&uuml;gung stehen.',
    'birds_function_title': 'Funktionsweise',
    'birds_function_1_2':
        'Jedem Bundestagsabgeordneten wurde eine Vogelstimme zugeordnet.'
        ' Um Ihre Vogelstimme zu &auml;ndern m&uuml;ssen Sie lediglich den Namen'
        ' des Vogels zusammen mit dem Hashtag'
        ' <strong>#HouseOfTweets</strong> tweeten, oder kurz <strong>#Hot</strong>.',
    'birds_function_2_2':
        'Um das so einfach wie m&ouml;glich zu gestalten ist hier eine Auswahl aller Vogelnamen,'
        ' die unser System erkennt. Jeder Politiker kann ganz einfach einen Vogel anklicken,'
        ' einen Tweet absenden, und seine Wunsch-Vogelstimme wird von'
        ' unseren Systemen &uuml;bernommen.',
    'birds_list_title': 'Vogelliste',
    # Appears on about.html only:
    'about_lead': 'Wer wir und unsere Sponsoren sind.',
    'about_sponsors': 'Sponsoren',
    'about_sponsors_html': """<ul>
        <li>
        Deutsches Forschungszentrum f&uuml;r K&uuml;nstliche Intelligenz
        </li><li>
        Spielbanken Saar
        </li><li>
        Saartoto
        </li><li>
        Ministerium f&uuml;r Bildung und Kultur Saarland
        </li>
      </ul>""",
    'about_team': 'Das Team hinter House of Tweets',
    'about_team_html': """<ul>
        <li>
        Volker Sieben: Idee und Konzept
        </li><li>
        Maximilian Schwenger: Design und technische Umsetzung
        </li><li>
        Ben Wiederhake: Design und technische Umsetzung
        </li>
      </ul>""",
    'about_copyright': 'Copyright-Hinweise',
    # 'about_copyright_html': AUTOGENERATED
    # Copyright strings:
    'copyright_pre': 'Wir danken den folgenden Fotografen f&uuml;r die herrlichen Vogelbilder:',
    'about_thanks': 'Danksagung',
    'about_thanks_text':
        'Wir danken Bootstrap, Github Pages, CoffeeScript, Wikipedia und NodeJS'
        ' f&uuml;r diese wundervollen Projekte, und der Universit&auml;t des Saarlandes'
        ' sowie der Hochschule der Bildenen K&uuml;nste Saar f&uuml;r ihre Unterst&uuml;tzung.',
}

STRINGS_EN = {
    # Appears on both pages
    'birds_title': 'Bird selection',
    'about_title': 'About',
    'nav_toggle': 'Toggle navigation',
    'nav_index': 'index_en.html',
    'nav_birds': 'birds_en.html',
    'nav_about': 'about_en.html',
    'nav_index_de': 'index.html',
    'nav_birds_de': 'birds.html',
    'nav_about_de': 'about.html',
    'nav_index_en': '#',
    'nav_birds_en': '#',
    'nav_about_en': '#',
    'de_active': '',
    'en_active': ' class="active"',  # Must start with a space
    # Appears on index.html only:
    'index_lead': 'What this project is about',
    'index_concept': 'Concept',
    'index_concept_text': """
        House of Tweets is a interdisciplinary and interactive sound sculpture for the German Bundestag.
        <br>
        Each politician can choose a representative bird. The bird's voice will then be used to depict tweets aurally. It reflects the politician's mood while tweeting: an aggressive tweet will be translated into an aggressive bird call.
        <br>
        During a fiery debate in the Bundestag a concert of birds arises, a befuddling mix of different voices, constantly changing, never subsiding.
        <br>
        In addition, visitors of the exhibit can assign their own ideas of birds to the politicians and experience upcoming tweets with the new voice.
        <br>
        They can also add their own twitter account, choose a bird, and become themselves part of the exhibit. Their tweets will not only be displayed among the politicians', but become audible and contribute to the sound experience.
        """,
    'index_spacetime': 'Place and time',
    'index_spacetime_text': """
        The exhibition opens on Thursday, the 18th of May 2017,
        in the saarl&auml;ndische Landesvertretung.
        <br />
        The address is:
        <blockquote>
        Die Vertretung des Saarlandes beim Bund <br />
        In den Ministerg&auml;rten 4 <br />
        10117 Berlin <br />
        <a class="quotelink" href="https://www.google.de/maps/place/Berlin+Landesvertretung+Saarland">Open in Google Maps</a>
        </blockquote>
        """,
    'index_demo': 'Preview',
    # Appears on birds.html only:
    'birds_lead': 'All bird voices that can be selected, in the context of the project House of Tweets.',
    'birds_function_title': 'How it works',
    'birds_function_1_2':
        'Each member of the parliament has been assigned a bird\'s voice.'
        ' To change their bird, they just have to tweet their preferred bird'
        ' alongside the hashtag <strong>#HouseOfTweets</strong>'
        ' (or <strong>#HoT</strong>, for short).',
    'birds_function_2_2':
        'To make this as easy as possible, here\'s a selection of all bird names'
        ' our systems recognize. Any member of the parliament can simply click on one of the birds,'
        ' send a Tweet, and their preferred bird voice will be applied by our systems',
    'birds_list_title': 'List of recognised birds.',
    # Appears on about.html only:
    'about_lead': 'Who we and our sponsors are.',
    'about_sponsors': 'Sponsors',
    'about_sponsors_html': """<ul>
        <li>
        German Research Center for Artificial Intelligence
        </li><li>
        Spielbanken Saar
        </li><li>
        Saartoto
        </li><li>
        Ministerium f&uuml;r Bildung und Kultur Saarland
        </li>
      </ul>""",
    'about_team': 'The Team behind House of Tweets',
    'about_team_html': """<ul>
        <li>
        Volker Sieben: Idea and Concept
        </li><li>
        Maximilian Schwenger: Design and technical Implementation
        </li><li>
        Ben Wiederhake: Design and technical Implementation
        </li>
      </ul>""",
    'about_copyright': 'Copyright notices',
    # 'about_copyright_html': AUTOGENERATED
    # Copyright strings:
    'copyright_pre': 'We thank the following photographers for their great images:',
    'about_thanks': 'Thanks',
    'about_thanks_text':
        'We thank Bootstrap, Github Pages, CoffeeScript, Wikipedia and NodeJS'
        ' for their awesome projects, and the University of Saarlandes'
        ' and the Hochschule der Bildenen K&uuml;nste Saar for their support.',
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
        strings['birds_init_content'] = ''.join([spoof_bird(bid, display_name, tweet_name)
                                                 for bid, display_name, tweet_name in init_birds])

    generate('index')
    generate('birds')
    generate('about')


if __name__ == '__main__':
    run()
