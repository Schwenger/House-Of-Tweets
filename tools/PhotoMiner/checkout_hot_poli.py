#!/usr/bin/env python3

# NOTE: Before running this script, you may want to either get my cache,
# or run 'fetch.py' from the branch 'crawler-fetch'.

import json
import nice
import os
import subprocess

# If True:
#   - only export images where CHOICES_PRIORITY is still relevant
#     (i.e., more than one image and no entry in CHOICES_OVERRIDE)
#   - no pols.json written
#   - non-standard filenames
#   - no thumbnails
# If False:
#   - export "all" images, defaulting to the order in CHOICES_PRIORITY.
#   - pols.json written
#   - standard filenames, identical in scheme to the old ones.
CHOICE_MODE = False

# To make the following dict shorter:
w, l, c, s, g = 'wiki', 'die linke', 'cxu', 'spd', 'gruene'

CHOICES_OVERRIDE = {
    # 'pid': 'slug',
    # Recommended: open a new editor and just write down entries like '52g',
    # and let regexes do the rest.
    '0': l,
    '4': c,
    '5': w,
    '6': w,
    '7': s,
    '9': s,
    '12': g,
    '14': w,
    '16': c,
    '22': s,
    '23': s,
    '24': l,
    '25': w,
    '28': g,
    '29': g,
    '32': c,
    '33': l,
    '34': w,
    '40': c,
    '41': c,
    '42': l,
    '43': s,
    '45': l,
    '56': g,
    '59': w,
    '60': w,
    '61': c,
    '62': w,
    '64': w,
    '67': s,
    '68': s,
    '70': s,
    '74': l,
    '76': l,
    '77': g,
    '78': s,
    '85': w,
    '88': g,
    '89': w,
    '91': g,
    '95': s,
    '97': l,
    '98': s,
    '99': s,
    '104': w,
    '105': w,
    '111': c,
    '114': s,
    '117': s,
    '118': s,
    '124': c,
    '125': w,
    '127': s,
    '130': w,
    '132': w,
    '133': l,
    '134': w,
    '142': l,
    '145': w,
    '147': s,
    '150': w,
    '153': w,
    '156': l,
    '159': w,
    '162': c,
    '165': c,
    '166': l,
    '172': w,
    '173': s,
    '175': l,
    '176': w,
    '177': w,
    '178': s,
    '179': s,
    '181': g,
    '182': w,
    '183': c,
    '184': c,
    '186': w,
    '188': s,
    '189': c,
    '190': w,
    '196': s,
    '204': s,
    '209': w,
    '211': s,
    '214': w,
    '215': g,
    '217': w,
    '218': g,
    '224': c,
    '226': l,
    '229': s,
    '231': g,
    '233': w,
    '234': l,
    '238': c,
    '239': w,
    '240': s,
    '243': w,
    '244': s,
    '245': s,
    '252': l,
    '254': w,
    '257': w,
    '259': w,
    '260': w,
    '261': s,
    '264': c,
    '265': w,
    '267': w,
    '268': s,
    '270': c,
    '271': w,
    '272': c,
    '273': s,
    '275': g,
    '276': c,
    '278': w,
    '282': l,
    '283': w,
    '284': g,
    '287': l,
    '288': w,
    '290': w,
    '291': g,
    '293': c,
    '294': w,
    '295': g,
    '298': c,
    '299': w,
    '301': g,
    '309': s,
    '313': s,
    '314': l,
    '315': w,
    '317': l,
    '319': g,
    '320': s,
    '321': c,
    '325': l,
    '326': w,
    '328': l,
    '329': c,
    '332': g,
    '335': s,
    '339': l,
    '341': w,
    '344': l,
    '346': w,
    '348': g,
    '350': s,
    '351': w,
    '356': w,
    '357': s,
    '360': w,
    '361': w,
    '369': g,
    '373': l,
    '375': w,
    '379': w,
    '385': w,
    '386': w,
    '389': g,
    '392': w,
    '393': c,
    '395': s,
    '397': l,
    '398': g,
    '399': g,
}

CHOICES_PRIORITY = [
    'twitter',  # Just in case we ever do that
    'spd',
    'die linke',
    'gruene',
    'wiki',  # Not the best source of images
    'cxu',  # Often enough worse than Wikipedia's images
]

DIR_PREFIX = 'preview'
os.mkdir(DIR_PREFIX)  # If this fails: you should always start from scratch here!


def convert(*args):
    try:
        subprocess.run(['convert', *args],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       check=True)
    except subprocess.CalledProcessError as e:
        print('stdout:\n{}\nstderr:\n{}\n'.format(e.stdout, e.stderr))
        raise


def checkout(pid, fields):
    img_prefix = os.path.join(DIR_PREFIX, pid)
    dl_path = nice.get(fields['url'])
    freshest_path = dl_path

    # Provide '_raw' for intermediate processing
    raw_dst_path = img_prefix + '_raw.jpg'
    if fields.get('is_compressed'):
        with open(raw_dst_path, 'wb') as raw_fp:
            subprocess.run(['unzip', '-p', dl_path],
                           stdout=raw_fp, stderr=subprocess.PIPE, check=True)
        freshest_path = raw_dst_path
    else:
        # Need '../' to get out of 'preview/'
        os.symlink('../' + dl_path, raw_dst_path)

    # Something about digitally rotated images (Michael Grosse-Brömer, 154)
    # doesn't work as it should.
    inject = []
    if '154' in pid:
        inject = ['-rotate', '-90']

    # Provide ready-to-use image
    convert(freshest_path,
            '-resize', '330x330^',
            '-gravity', 'north',
            '-extent', '330x330',
            *inject,
            '-strip',
            img_prefix + '.jpg')

    if not CHOICE_MODE:
        # Provide thumbnail
        convert(freshest_path,
               '-thumbnail', '75x75^',
               '-gravity', 'north',
               '-extent', '75x75',
               *inject,
               img_prefix + '_t.jpg')
        # TODO: Use '-strip'.
        # Don't do it right now in order to
        # avoid blowing up 'heavy' even more.

    # Retract '_raw'
    os.remove(raw_dst_path)

    entry = {
        'pathToImage': pid + '.jpg',
        'pathToThumb': pid + '_t.jpg',
        'license': fields['license'],
    }
    if 'copyright' in fields:
        entry['copyright'] = fields['copyright']
    return entry


def choose_img(pid, imgs):
    if pid in CHOICES_OVERRIDE:
        choice = CHOICES_OVERRIDE[pid]
    elif len(imgs) == 1:
        choice = list(imgs.keys())[0]
    else:
        print('[WARN] No human selection for ' + pid)
        appliccable = [ch for ch in CHOICES_PRIORITY if ch in imgs]
        assert len(appliccable) > 0, (imgs.keys(), CHOICES_PRIORITY)
        choice = appliccable[0]
    return imgs[choice]


SPOOF_USERS = {
    'hot': {
        "twittering": {
          "twitterId": "4718199753",
          "twitterUserName": "HouseOfTweetsSB"
        },
        "self_bird": "amsel",
        "party": "Gr\u00fcn",
        "name": "House Of Tweets",
        "pid": "hot",
        "cv": {
          "en": "A good bird person.  Very reliable.  But also killed.  In bird culture, that was considered a 'dick move'.",
          "de": "Uhh, keine Ahnung, ich kenn das Zitat nur auf Englisch."
        },
        "images": {
          "pathToThumb": "tgroup_greengr\u00fcn.jpg",
          "pathToImage": "group_greengr\u00fcn.jpg"
        },
        "citizen_bird": "amsel"
    },
    '523': {
        "twittering": {
            "twitterId": "237115617",
            "twitterUserName": "sc_ontour"
        },
        "self_bird": "girlitz",
        "party": "SPD",
        "name": "Stephan Schweitzer",
        "pid": "523",
        "cv": {
            "en": "Schweitzer, born in Saarland, used to work in the Willy-Brandt-Haus in Berlin for four years. He started out as head of Astrid Klug's office, then became the head of the department for communication. Lastly, he was technical director for the election campaign. Before transferring to Berlin, the certified public administration specialist directed the affairs of the Saar-SPD. His career began as publicist for the Saarlouis county in 1993.",
            "de": "Schweitzer, ein gebürtiger Saarländer, arbeitete zuvor vier Jahre im Willy-Brandt-Haus in Berlin, zunächst als Büroleiter der damaligen SPD-Bundesgeschäftsführerin Astrid Klug, dann als Abteilungsleiter für Kommunikation und zuletzt als technischer Wahlkampfleiter im Bundestagswahlkampf. Vor seinem Wechsel nach Berlin hatte der Diplom-Verwaltungswirt, der seine Laufbahn 1993 als Pressesprecher des Landkreises Saarlouis begann, die Geschäfte der Saar-SPD geführt."
        },
        "images": {
            "pathToThumb": "523_t.jpg",
            "pathToImage": "523.jpg"
        },
        "citizen_bird": "zaunkoenig"
    },
    # FIXME: Icomplete, pols.json has copyright
    '701': {
        "twittering": {
            "twitterId": "18250754",
            "twitterUserName": "ulrichcommercon"
        },
        "self_bird": "fitis",
        "party": "SPD",
        "name": "Ulrich Commerçon",
        "pid": "701",
        "cv": {
            "de": "Ulrich Commerçon (* 28. April 1968 in Homburg) ist ein deutscher Politiker der SPD und seit 2017 saarländischer Minister für Bildung und Kultur im Kabinett Kramp-Karrenbauer III. Zuvor war er von 2012 bis 2017 Minister für Bildung und Kultur.",
            "en": "Ulrich Commerçon is a German politician. He is a member of the CSU."
        },
        "images": {
            "pathToThumb": "701_t.jpg",
            "pathToImage": "701.jpg"
        },
        "citizen_bird": "hausrotschwanz"
    },
    '702': {
        "twittering": {
            "twitterId": "47620601",
            "twitterUserName": "_A_K_K_"
        },
        "self_bird": "klappergrasmuecke",
        "party": "CSU",
        "name": "Annegret Kramp-Karrenbauer",
        "pid": "702",
        "cv": {
            "en": "Annegret Kramp-Karrenbauer is a German politician. She is a member of the CSU.",
            "de": "Annegret Kramp-Karrenbauer (geb. Kramp; * 9. August 1962 in Völklingen) ist eine deutsche Politikerin. Sie ist seit August 2011 Ministerpräsidentin des Saarlandes, seit Juni 2011 Vorsitzende der CDU Saar und seit November 2010 Mitglied im CDU-Bundespräsidium. Sie war von 2000 bis 2011 Ministerin in der Regierung des Saarlandes in verschiedenen Ressorts (Inneres, Bildung, Soziales). 1998 war sie für ein halbes Jahr Mitglied des Deutschen Bundestages und ist seit 1999 Abgeordnete im Landtag des Saarlandes."
        },
        "images": {
            "pathToThumb": "702_t.jpg",
            "pathToImage": "702.jpg"
        },
        "citizen_bird": "rauchschwalbe"
    },
    '703': {
        "twittering": {
            "twitterId": "474792689",
            "twitterUserName": "AnkeRehlinger"
        },
        "self_bird": "schneeeule",
        "party": "SPD",
        "name": "Anke Rehlinger",
        "pid": "703",
        "cv": {
            "en": "Anke Rehlinger is a German politician. She is a member of the SPD.",
            "de": "Anke Rehlinger (geb. Moos; * 6. April 1976 in Wadern) ist eine deutsche Politikerin (SPD). Sie ist Ministerin für Wirtschaft, Arbeit, Energie und Verkehr und stellvertretende Ministerpräsidentin im Saarland. Zuvor war sie saarländische Ministerin der Justiz und Ministerin für Umwelt und Verbraucherschutz im Kabinett Kramp-Karrenbauer II.  Sie trat bei der saarländischen Landtagswahl im Frühjahr 2017 als Spitzenkandidatin für das Amt der saarländischen Ministerpräsidentin an, und erreichte mit der SPD Saar 29,6 Prozent der Stimmen."
        },
        "images": {
            "pathToThumb": "703_t.jpg",
            "pathToImage": "703.jpg"
        },
        "citizen_bird": "stieglitz"
    },
}


def prune_convert(pols):
    pols = {poli['pid']: poli for poli in pols if 'twittering' in poli}
    for poli in pols.values():
        del poli['imgs']
    for (pid, poli) in SPOOF_USERS.items():
        assert pid == poli['pid']
        pols[pid] = poli
    return pols


def run():
    with open('converge_each.json', 'r') as fp:
        pols = json.load(fp)

    for e in pols:
        if 'twittering' not in e:
            print('[INFO] Skipping (not twittering) ' + e['full_name'])
            continue
        if len(e['imgs']) == 0:
            print('[WARN] No images at all for ' + e['full_name'])
            continue

        print('[INFO] Checking out files for ' + e['full_name'])
        if not CHOICE_MODE:
            fields = choose_img(e['pid'], e['imgs'])
            e['images'] = checkout(e['pid'], fields)
        elif len(e['imgs']) >= 2 and e['pid'] not in CHOICES_OVERRIDE:
            for slug, fields in e['imgs'].items():
                checkout(e['pid'] + slug, fields)

    if not CHOICE_MODE:
        print('[INFO] CHOICE_MODE = False, so I\'ll write out pols.json')
        pols = prune_convert(pols)
        with open('pols.json', 'w') as fp:
            json.dump(pols, fp, sort_keys=True, indent=2)
    else:
        print('[INFO] CHOICE_MODE = True, so not writing anything')


if __name__ == '__main__':
    if not CHOICE_MODE:
        print('[INFO] If there\'s many complaints about missing human choices, re-run with CHOICE_MODE = True')
    run()

    print('Done.')
