import os

import pendulum
from babel.support import Translations

from last.services.constants import BASE_DIR
from last.services.template import templates

TRANSLATIONS = {
    "zh_CN": Translations.load(os.path.join(BASE_DIR, "locales"), locales=["zh_CN"]),
    "en_US": Translations.load(os.path.join(BASE_DIR, "locales"), locales=["en_US"]),
}

translations = TRANSLATIONS.get("en_US")


def set_locale(locale: str):
    global translations
    if locale == "zh_CN":
        plocale = "zh"
    else:
        plocale = "en"
    pendulum.set_locale(plocale)

    translations = TRANSLATIONS.get(locale) or TRANSLATIONS.get("en_US")
    templates.env.install_gettext_translations(translations)
    translations.install(locale)


def _(msg: str):
    return translations.ugettext(msg)
