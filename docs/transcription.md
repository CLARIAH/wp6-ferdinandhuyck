
# Corpus CLARIAH - wp6-ferdinandhuyck


## Essentials

*   Text-Fabric non-slot nodes correspond to TEI elements in the source.
*   Text-Fabric node-features correspond to TEI attributes.
*   Text-Fabric slot nodes correspond to characters in TEI element content.

In order to understand the encoding, you need to know

*   the [TEI elements](https://tei-c.org/release/doc/tei-p5-doc/en/html/REF-ELEMENTS.html).
*   the [TEI attributes](https://tei-c.org/release/doc/tei-p5-doc/en/html/REF-ATTS.html).
*   the [Text-Fabric datamodel](https://annotation.github.io/text-fabric/tf/about/datamodel.html)

The TEI to TF conversion is an almost literal and very faithful transformation from
the TEI source files to a Text-Fabric data set.

But there are some peculiarities.

## Sectioning

The material is divided into three levels of sections, mainly for the purposes
of text display.

But how these levels relate to the source material is a different matter.

The conversion supports a few sectioning models that specify this.
This aspect is *work-in-progress*, because TEI sources differ wildly in how they
are sectioned.
The sectioning models that are currently supported correspond to cases we have
encountered, we have not done exhaustive research into TEI sectioning in practice.

### Model I: folders and files

This model assumes that the source is a directory consisting of folders
consisting of xml files, the TEI files.

There are three section levels: folder - file - subdivision in file.

1.  Subdirectories and files are sorted in the lexicographic ordering
1.  The folder `__ignore__` is ignored.
1.  For each folder, a section level 1 node will be created, with
    feature `name` containing its name.
1.  For each file in a folder, a section level 2 node will be created, with
    feature `name` containing its name.
1.  A third section level, named `chunk` will be made.
    For each immediate child element of `<teiHeader>` and for each immediate child
    element of `<body>`, a chunk node will be created, wit a feature `chunk`
    containing the number of the chunk within the file, starting with 1.
    Also the following elements will trigger a chunk node:
    `<facsimile>`, `<fsdDecl>`, `<sourceDoc>`, and `<standOff>`.

### Model II: single file and divs.

This model assumes that the source is a single TEI file.

There are two section levels: "chapter"like - "p"like.

1.  The name of the source file is not recorded.
1.  The first section level, named `chapter` will be made as follows:
    For the `<teiHeader>` and for each immediate child
    element of `<body>`, a chapter node will be created, wit a feature `chapter`
    containing the content of the first element with certain properties that
    follows the section-1-level element.
1.  The properties of the heading bearing element is given by its element
    name and a dictionary of attribute values.
    For example:

    ```
    element = "head"
    attributes = dict(rend="h3")
    ```

    Heading bearing elements also occur in the text, and are treated in the same
    way as all other element. The only special thing is that their plain text
    content is used as the value of a feature.
1.  The second section level, named `chunk` consists of the top-level elements within
    the chapters, except certain empty elements, such as breaks.
1.  Section-2-level nodes get a feature `chunk` with a chunk number.
1.  `cn` is positive for `<p>` elements, and it is the sequence number
    of the `p` within the chapter.
1.  `cn` is negative for all other elements of section-level-2. For those elements
    it is the sequence number of the non-p immediate children of the chapter.

### Specifying a sectioning model

## Elements and attributes

1.  All elements, except `<TEI>` and `<teiHeader>` result in nodes whose type is
    exactly equal to the tag name.
1.  These nodes are linked to the slots that are produced when converting the
    content of the corresponding source elements.
1.  Attributes translate into features of the same name; the feature assigns
    the attribute value (as string) to the node that corresponds to the element
    of the attribute.

## Word detection

Words will be detected. They are maximally long sequences of alphanumeric characters
and hyphens.

1.  What is alphanumeric is determined by the unicode class of the character,
    see the Python documentation of the function
    [`isalnum()`](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)
1.  Hyphens are Unicode characters 002D (ascii hyphen) and 2010 (unicode hyphen).
1.  Words get the following features:
    *   `str`: the alphanumeric string that is the word;
    *   `after`: the non-alphanumeric string after the word unti the following word.

## Slots

The basic unit is the unicode character.
For each character in the input we make a slot, but the correspondence is not
quite 1-1.

1.  Spaces are stripped when they are between elements whose parent does not allow
    mixed content; other whitespace is reduced to a single space.
1.  All slots inside the teiHeader will get the feature `is_meta` set to 1;
    for slots inside the body, `is_meta` has no value.
1.  Empty elements will receive one extra slot; this will anchor the element to
    a textual position; the empty slot gets the ZERO-WIDTH-SPACE (Unicode 200B)
    as character value.
1.  Slots get the following features:
    *   `ch`: the character of the slot
    *   `empty`: 1 if the slot has been inserted as an empty slot, no value otherwise.

## Text kinds and text formatting

We record in additional features whether text occurs in metadata elements and
in note elements and what formatting specifiers influence the text.
These features are provided for characters and words, and have only one value: 1.
The absence of values means that the corresponding property does not hold.

The following features are added:

*   `is_meta`: 1 if the word occurs in inside the `<teiHeader>`, no value otherwise.
*   `is_note`: 1 if the word occurs in inside the `<note>`, no value otherwise.
*   `rend_`*r*: for any *r* that is the value of a `rend` attribute.

All these features are defined for `char` and `word` nodes.
For word nodes, the value of these features is set equal to what these features
are for their first character.

Special formatting for the `rend_`*r* features is supported for some values of *r*.
The conversion supports these out-of-the-box:

`italic`
`bold`
`underline`
`center`
`large`
`spaced`
`margin`
`above`
`below`
`sub`
`sup`
`super`

It is possible for the corpus designer to add more formatting on a per-corpus
basis by adding it to the `display.css` in the app directory of the corpus.
Unsupported values get a generic kind of special format: an orange-like color.

Special formatting becomes visible when material is rendered in a `layout` text
format.

## Text-formats

Text-formats regulate how text is displayed, and they can also determine
what text is displayed.

There are two kind of text-formats: those that start with the word `layout` and
those that start with `text`.

The `text` formats do not apply any kind of special formating, the `layout` formats
do.

We have the following formats:

*   `text-orig-full`: all text
*   `layout-orig-full`: all text, formatted in HTML

## Simplifications

XML is complicated, the TEI guidelines use that complexity to the full.
In particular, it is difficult to determine what the set of TEI elements is
and what their properties are, just by looking at the schemas, because they are full
of macros, indirections, and abstractions, which can be overridden in any particular
TEI application.

On the other hand, the resulting TF should consist of clearly demarcated node types
and a simple list of features. In order to make that happen, we simplify matters
a bit.

1.  Processing instructions (`<!proc a="b">`) are ignored.
1.  Comments (`<!-- this is a comment -->`) are ignored.
1.  Declarations (`<?xml ...>` `<?xml-model ...>` `<?xml-stylesheet ...>`) are
    read by the parser, but do not leave traces in the TF output.
1.  The atrributes of the root-element (`<TEI>`) are ignored.
1.  Namespaces (`xmlns="http://www.tei-c.org/ns/1.0"`) are read by the parser,
    but only the unqualified names are distinguishable in the output as feature names.
    So if the input has elements `tei:abb` and `ns:abb`, we'll see just the node
    type `abb` in the output.

## Validation

We have used [lxml](https://lxml.de) for XML parsing. During `convert` it is not used
in validating mode, but we can trigger a validation step during `check`.

However, some information about the elements, in particular whether they allow
mixed content or not, has been gleaned from the schemas, and has been used
during conversion.

Care has been taken that the names of these extra nodes and features do not collide
with element/attribute names of the TEI.

## TF noded and features

(only in as far they are not in 1-1 correspondence with TEI elements and attributes)

### node type `folder`

*The type of subfolders of TEI documents.*

**Section level 1.**

**Features**

feature | description
--- | ---
`folder` | name of the subfolder

### node type `file`

*The type of individual TEI documents.*

**Section level 2.**

**Features**

feature | description
--- | ---
`file` | name of the file, without the `.xml` extension. Other extensions are included.

### node type `chunk`

*Top-level division of material inside a document.*

**Section level 3.**

**Features**

feature | description
--- | ---
`chunk` | sequence number of the chunk within the document, starting with 1.

### node type `word`

*Individual words, without punctuation.*

**Features**

feature | description
--- | ---
`str` | the characters of the word, without soft hyphens.
`after` | the non-word characters after the word, up till the next word.
`is_meta` | whether a word is in the teiHeader element
`is_note` | whether a word is in a note element
`rend_`*r* | whether a word is under the influence of a `rend="`*r*`"` attribute.

### node type `char`

*Unicode characters.*

**Slot type.**

The characters of the text of the elements.
Ignorable whitespace has been discarded, and is not present in the TF dataset.
Meaningful whitespace has been condensed to single spaces.

Some empty slots have been inserted to mark the place of empty elements.

**Features**

feature | description
--- | ---
`ch` | the unicode character in that slot. There are also slots
`empty` | whether a slot has been inserted in an empty element
`is_meta` | whether a character is in the teiHeader element
`is_note` | whether a character is in a note element
`rend_`*r* | whether a character is under the influence of a `rend="`*r*`"` attribute.


## See also

*   [about](about.md)
