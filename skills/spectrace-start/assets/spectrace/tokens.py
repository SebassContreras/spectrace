"""Words for lexical search: split camelCase, snake_case and digits, fold case and accents, strip plurals."""
import re
import unicodedata

WORD_RE = re.compile(r"[A-Za-zÀ-ɏ]+|\d+")
CAMEL_RE = re.compile(r"[A-Z]+(?=[A-Z][a-z])|[A-Z]?[a-zß-ɏ]+|[A-Z]+|\d+")
STOP = set("""a an and are as at be by for from in is it of on or that the this to with
de del el en es la las los lo un una y o que se con por para al su sus no""".split())


def fold(word):
    """Lowercase without accents: `Sesión` → `sesion`."""
    return "".join(c for c in unicodedata.normalize("NFKD", word.lower()) if not unicodedata.combining(c))


def stem(word):
    """A simple plural strip for English and Spanish: tasks → task, ciudades → ciudad, entries → entry."""
    if len(word) <= 3 or word.endswith("ss"):
        return word
    if word.endswith("ies") and len(word) > 4:
        return word[:-3] + "y"
    if word.endswith("es") and (word[-3] in "sxzd" or word.endswith(("ches", "shes", "ones", "ores", "ales"))):
        return word[:-2]
    if word.endswith("s"):
        return word[:-1]
    return word


def tokens(text):
    """Search tokens of a text: identifiers split into words, folded and stemmed, stop words out."""
    out = []
    for raw in WORD_RE.findall(text):
        for part in CAMEL_RE.findall(raw) or [raw]:
            word = stem(fold(part))
            if len(word) > 1 and word not in STOP:
                out.append(word)
    return out
