import os
from tf.convert.tei import TEI


AUTHOR = "Jacob van Lennep"
TITLE = "Ferdinand Huyck"
INSTITUTE = "KNAW/Huygens Amsterdam"
SOURCE = "DBNL"
SOURCE_URL = "https://www.dbnl.org/tekst/lenn006lotg01_01/"

SECTION_MODEL = dict(
    model="II",
    element="head",
    attributes=dict(rend="h3")
)
GENERIC = dict(
    author=AUTHOR,
    title=TITLE,
    institute=INSTITUTE,
    language="nl",
    source=SOURCE,
    sourceUrl=SOURCE_URL,
    converters="Dirk Roorda (Text-Fabric)",
    sourceFormat="TEI",
    descriptionTf="Diplomatic edition",
)

APP_CONFIG = dict(
    provenanceSpec=dict(
        doi="10.5281/zenodo.nnnnnn",
    )
)

ABOUT_TEXT = """
# Source

J. van Lennep, De lotgevallen van Ferdinand Huyck. (2 delen). P. Meijer
Warnars, Amsterdam 1840

# Encoding

DBNL-TEI 1

# Identifier

*dbnl-nr*: `lenn006lotg01_01`

# Encoding log

*   2003-08-14 CB colofon added
*   2006-08-09 IH conversion to teixlite

# Source item

Universiteitsbibliotheek Leiden, item signature: `1224 C 8` en `1224 C 9`

# Remarks

This file contains a diplomatic rendering of the first imprint of
*De lotgevallen van Ferdinand Huyck*, in two volumes, by Jacob van Lennep, 1840.

# Editor interventions

*   vol. 1, p. I: heading "Eerste deel" added between square brackets
*   vol. 1, p. VI: page number IV corrected to VI
*   vol. 1, p. XVII: heading "Woord van de uitgever" added between square brackets
*   vol. 2, p. 1: heading "Tweede deel" added between square brackets
*   vol. 2, p. 459: heading "Nawoord" added between square brackets

During the conversion of the published source to the DBNL some title pages and blank
pages have been omitted.
"""

TRANSCRIPTION_TEXT = """

The conversion to TEI is done with sectioning model II.
"""

DOC_MATERIAL = dict(
    about=ABOUT_TEXT,
    transcription=TRANSCRIPTION_TEXT,
)


def transform(text):
    return text


T = TEI(
    schema=None,
    sourceVersion="2006-08-09",
    testSet=None,
    sectionModel=SECTION_MODEL,
    generic=GENERIC,
    transform=transform,
    tfVersion="0.1",
    appConfig=APP_CONFIG,
    docMaterial=DOC_MATERIAL,
    force=False,
)

T.run(os.path.basename(__file__))
