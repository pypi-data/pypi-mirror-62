Simple filesystem based file tagging and the associated `fstags` command line script.


*Latest release 20200229*:
New TaggedPath.modified property aliasing the TagSet.modified attribute.
ls: new -d option to treat directories like files (do not recurse), aiding reporting of tags for a directory.
find,ls subcommands: work off the realpath of the supplied top level path.
Tag: now subclasses namedtuple.
Rewrite rpaths() to use scandir and to also yield (is_dir,path) tuples.
TagSet, Tag, TagChoice moved into new cs.tagset module for reuse.
json_import: make --prefix mandatory, is "." as separator if not empty.
Move filename regexp rules to [filename_rules] config section.
New CascadeRule for representing a "target_tag_name = tag_name1 tag_name2..." config rules.
autotag: include the cascade rules in the autotagging after the filename rules.

Simple filesystem based file tagging
and the associated `fstags` command line script.

Why `fstags`?
By storing the tags in a separate file we:
* can store tags without modifying a file
* do no need to know the file's format,
  whether that supports metadata or not
* can process tags on any kind of file
* because tags are inherited from parent directories,
  tags can be automatically acquired merely by arranging your file tree

Tags are stored in the file `.fstags` in each directory;
there is a line for each entry in the directory with tags
consisting of the directory entry name and the associated tags.

Tags may be "bare", or have a value.
If there is a value it is expressed with an equals (`'='`)
followed by the JSON encoding of the value.

The tags for a file are the union of its direct tags
and all relevant ancestor tags,
with priority given to tags closer to the file.

For example, a media file for a television episode with the pathname
`/path/to/series-name/season-02/episode-name--s02e03--something.mp4`
might obtain the tags:

    series.title="Series Full Name"
    season=2
    sf
    episode=3
    episode.title="Full Episode Title"

from the following `.fstags` entries:
* tag file `/path/to/.fstags`:
  `series-name sf series.title="Series Full Name"`
* tag file `/path/to/series-name/.fstags`:
  `season-02 season=2`
* tag file `/path/to/series-name/season-02/.fstags`:
  `episode-name--s02e03--something.mp4 episode=3 episode.title="Full Episode Title"`

## Class `CascadeRule`

A cascade rule of possible source tag names to provide a target tag.

## Class `FSTags(cs.resources.MultiOpenMixin)`

A class to examine filesystem tags.

## Class `FSTagsCommand(cs.cmdutils.BaseCommand)`

`fstags` main command line class.


Command line usage:

    Usage:
        FSTagsCommand autotag paths...
            Tag paths based on rules from the rc file.
        FSTagsCommand cp [-fnv] srcpath dstpath
        FSTagsCommand cp [-fnv] srcpaths... dstdirpath
            Copy files and their tags into targetdir.
            -f  Force: remove destination if it exists.
            -n  No remove: fail if the destination exists.
            -v  Verbose: show copied files.
        FSTagsCommand scrub paths...
            Remove all tags for missing paths.
            If a path is a directory, scrub the immediate paths in the directory.
        FSTagsCommand find [--for-rsync] path {tag[=value]|-tag}...
            List files from path matching all the constraints.
            -d          treat directories like files (do no recurse).
            --direct    Use direct tags instead of all tags.
            --for-rsync Instead of listing matching paths, emit a
                        sequence of rsync(1) patterns suitable for use with
                        --include-from in order to do a selective rsync of the
                        matched paths.
            -o output_format
                        Use output_format as a Python format string to lay out
                        the listing.
                        Default: {filepath}
        FSTagsCommand json_import --prefix=tag_prefix {-|path} {-|tags.json}
            Apply JSON data to path.
            A path named "-" indicates that paths should be read from
            the standard input.
            The JSON tag data come from the file "tags.json"; the name
            "-" indicates that the JSON data should be read from the
            standard input.
        FSTagsCommand ln [-fnv] srcpath dstpath
        FSTagsCommand ln [-fnv] srcpaths... dstdirpath
            Link files and their tags into targetdir.
            -f  Force: remove destination if it exists.
            -n  No remove: fail if the destination exists.
            -v  Verbose: show linked files.
        FSTagsCommand ls [--direct] [-o output_format] [paths...]
            List files from paths and their tags.
            --direct    List direct tags instead of all tags.
            -o output_format
                        Use output_format as a Python format string to lay out
                        the listing.
                        Default: {filepath_encoded} {tags}
        FSTagsCommand mv [-fnv] srcpath dstpath
        FSTagsCommand mv [-fnv] srcpaths... dstdirpath
            Move files and their tags into targetdir.
            -f  Force: remove destination if it exists.
            -n  No remove: fail if the destination exists.
            -v  Verbose: show moved files.
        FSTagsCommand tag {-|path} {tag[=value]|-tag}...
            Associate tags with a path.
            With the form "-tag", remove the tag from the immediate tags.
            A path named "-" indicates that paths should be read from the
            standard input.
        FSTagsCommand tagpaths {tag[=value]|-tag} {-|paths...}
            Associate a tag with multiple paths.
            With the form "-tag", remove the tag from the immediate tags.
            A single path named "-" indicates that paths should be read
            from the standard input.
        FSTagsCommand test [--direct] path {tag[=value]|-tag}...
            Test whether the path matches all the constraints.
            --direct    Use direct tags instead of all tags.
        FSTagsCommand xattr_import {-|paths...}
            Import tag information from extended attributes.
        FSTagsCommand xattr_export {-|paths...}
            Update extended attributes from tags.

## Class `FSTagsConfig`

A configuration for fstags.

### Method `FSTagsConfig.__init__(self, rcfilepath=None)`

Initialise the config.

Parameters:
* `rcfilepath`: the path to the confguration file
  If `None`, default to `'~/.fstagsrc'` (from `RCFILE`).

## Function `get_xattr_value(filepath, xattr_name)`

Read the extended attribute `xattr_name` of `filepath`.
Return the extended attribute value as a string,
or `None` if the attribute does not exist.

Parameters:
* `filepath`: the filesystem path to update
* `xattr_name`: the extended attribute to obtain
  if this is a `str`, the attribute is the UTF-8 encoding of that name.

## Class `HasFSTagsMixin`

Mixin providing a `.fstags` property.

## Function `main(argv=None)`

Command line mode.

## Class `RegexpTagRule`

A regular expression based `Tag` rule.

## Function `rfilepaths(path, name_selector=None, U=None)`

Generator yielding pathnames of files found under `path`.

## Function `rpaths(path, *, yield_dirs=False, name_selector=None, U=None)`

Recurse over `path`, yielding `(is_dir,subpath)`
for all selected subpaths.

## Function `rsync_patterns(paths, top_path)`

Return a list of rsync include lines
suitable for use with the `--include-from` option.

## Class `TagFile(HasFSTagsMixin)`

A reference to a specific file containing tags.

This manages a mapping of `name` => `TagSet`,
itself a mapping of tag name => tag value.

## Class `TagFileEntry(builtins.tuple)`

TagFileEntry(tagfile, name)

## Class `TaggedPath(HasFSTagsMixin)`

Class to manipulate the tags for a specific path.

## Function `update_xattr_value(filepath, xattr_name, new_xattr_value)`

Update the extended attributes of `filepath`
with `new_xattr_value` for `xattr_name`.
Return the previous value, or `None` if the attribute was missing.

We avoid calling `os.setxattr` if the value will not change.

Parameters:
* `filepath`: the filesystem path to update
* `xattr_name`: the extended attribute to update;
  if this is a `str`, the attribute is the UTF-8 encoding of that name.
* `new_xattr_value`: the new extended attribute value, a `str`
  which should be the transcription of `TagSet`
  i.e. `str(tagset)`

## Function `verbose(msg, *a)`

Emit message if in verbose mode.



# Release Log

*Release 20200229*:
New TaggedPath.modified property aliasing the TagSet.modified attribute.
ls: new -d option to treat directories like files (do not recurse), aiding reporting of tags for a directory.
find,ls subcommands: work off the realpath of the supplied top level path.
Tag: now subclasses namedtuple.
Rewrite rpaths() to use scandir and to also yield (is_dir,path) tuples.
TagSet, Tag, TagChoice moved into new cs.tagset module for reuse.
json_import: make --prefix mandatory, is "." as separator if not empty.
Move filename regexp rules to [filename_rules] config section.
New CascadeRule for representing a "target_tag_name = tag_name1 tag_name2..." config rules.
autotag: include the cascade rules in the autotagging after the filename rules.

*Release 20200210*:
New "json_import" subcommand to import a JSON dict as tags, initial use case to load the metadata from youtube-dl.
New "scrub" command line operation, to purge tags of paths which do not exist.
New "cp", "ln" and "mv" subcommands to copy/link/move paths and take their tags with them.
New "test" subcommand to test paths against tag criteria, useful for find and scripts.
Small bugfixes.

*Release 20200130*:
New FSTagsConfig class which parses the .fstagsrc as a .ini file; related adjustments.
New HasFSTagsMixin presenting a settable .fstags property with a shared default.
New xattr_import and xattr_export subcommands, remove implicit xattr access/update from other operations.
New TagSet.__len__ returning the number of tags.
Add "-" support for stdin to "tag" and "tagpaths" subcommands.

*Release 20200113.2*:
FSTagsCommand docstring tweak.

*Release 20200113.1*:
Small docstring updates.

*Release 20200113*:
Mirror tags to user.cs.fstags xattr to honour Linux namespace requirements. Add "filesize" to available tag string format (-o option). Small bugfixes.

*Release 20191230*:
Command line: new "find" command to search a file tree based on tags.
Command line: new "mv" command to move a file and its tags.
Command line: Python string formats for "find" and "ls" output.
TaggedPath.autotag: new optional `no_save` parameter, default False, to suppress update of the associated .fstags file.
Inital and untested "mirror tags to xattrs" support.

*Release 20191201*:
New "edit" subcommand to rename files and edit tags.

*Release 20191130.1*:
Initial release: fstags, filesystem based tagging utility.
