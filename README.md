# libpytunes

Fork of the [libpytunes](https://github.com/liamks/libpytunes) repo by Liam Kaufman. 

## Changes
### More fields
Adds more fields to the `Song` class, including:
- Start time
- Stop time
- BPM
- Disliked
- File Folder Count
- Library Folder Count

### Field reordering
Fields in relevant places (the song dictionary, sources, etc.) are shown in the order they appear in the iTunes XML.
Where applicable, fields with unknown order are placed at the bottom of the field list.

### Writing modified `Song` objects back to an XML file 
`Library` adds the `writeToXML()` function, which allows changes to the `Song` dictionary to be written back to an 
XML file. The XML file is formatted as close to the auto-generated XML file as possible:
- `sort_keys` is `False` to keep keys in identical order.
- `writeToXML()` has an optional `reformat` keyword argument that strips certain newlines normally made by the 
  `plistlib` library.
  
Note that the built-in `plistlib` formats certain parts of the output XML differently, such as the width of any 
`data` fields. These are not reformatted to maintain consistency with the auto-generated file.

This function does not consider any changes to `Playlist` objects.

### Python 3.9 support
Adds support for Python 3.9 by using `plistlib.load()` instead of `plistlib.readPlist()`.

