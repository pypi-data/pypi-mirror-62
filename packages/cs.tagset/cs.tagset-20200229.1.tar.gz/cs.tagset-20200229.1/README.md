Tags and sets of tags.


*Latest release 20200229.1*:
Initial release: pull TagSet, Tag, TagChoice from cs.fstags for independent use.

Tags and sets of tags.

## Class `Tag(Tag,builtins.tuple)`

A Tag has a `.name` (`str`) and a `.value`.

The `name` must be a dotted identifier.

A "bare" `Tag` has a `value` of `None`.

## Class `TagChoice(TagChoice,builtins.tuple)`

A "tag choice", an apply/reject flag and a `Tag`,
used to apply changes to a `TagSet`
or as a criterion for a tag search.

Attributes:
* `spec`: the source text from which this choice was parsed,
  possibly `None`
* `choice`: the apply/reject flag
* `tag`: the `Tag` representing the criterion

## Class `TagSet`

A setlike class associating a set of tag names with values.

### Method `TagSet.__init__(self, *, defaults=None)`

Initialise the `TagSet`.

Parameters:
* `defaults`: a mapping of name->`TagSet` to provide default values.



# Release Log

*Release 20200229.1*:
Initial release: pull TagSet, Tag, TagChoice from cs.fstags for independent use.
