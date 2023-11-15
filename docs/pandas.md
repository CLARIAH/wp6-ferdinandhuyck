# Text data in Pandas

We have exported the TEI text via Text-Fabric data to Pandas.

## Summary

TEI | Text-Fabric | Pandas
--- | --- | ---
words | slot nodes | rows
elements | nodes | rows
chunks | nodes | rows
chapters | nodes | rows
attributes | features | columns

## Rows

The rows in the data frame correspond to the Text-Fabric nodes, which derive
from the TEI elements plus a few additional objects such as `chunk`, `chapter`.
The order of the rows is a top-down, left-right walk through the TEI tree.

# Colums

When we describe the columns we refer to the *node* as the Text-Fabric node
that corresponds with the individual row. This node corresponds in turn
with a TEI element.

column | type | description
--- | --- | ---
`nd` | *int* | the number of the node in Tex-Fabric
`element` | *str* | the type of the node
`str` | *str* | the text of the node, only if the type is `word`
`after` | *str* | the text after the word node, and before the next word
`in.chapter` | *int* | the node number of the chapter in which this node is contained
`in.chunk` | *int* | the node number of the chunk in which this node is contained
`chapter` | *str* | the heading of the chapter of this node, only for `chunk` and `chapter` nodes
`chunk` | *str* | the number of the chunk of this node, only for `chunk` nodes

The following columns correspond to the Text-Fabric features as 
described in [transcription](transcription.md), and originate from TEI attributes.

# Usage

You can get the complete text from columns `str` + `after` for those rows that have
the value `word` in the `element` column.

See
[pandas.ipynb](https://nbviewer.org/github/CLARIAH/wp6-ferdinandhuyck/blob/main/programs/pandas.ipynb)
for examples.
