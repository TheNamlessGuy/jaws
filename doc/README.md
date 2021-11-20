# Getting started
TODO

# Syntax
The entire wiki system is built using a series of starting and ending brackets, not unlike XML/HTML/whatever. Check below and you'll probably get it.  
All bracket type names and parameter names are case insensitive.

## Display text
Just write the text. For example:
```
Hello :)
```

## Header
Use the header brackets:
```
[[header]]Hello :)[[/header]]
```
In order to make a sub-header, use the level parameter:
```
[[header]]Hello :)[[/header]]
[[header level="2"]]Hello again :)[[/header]]
```

If a level is not specified, it will default to 1 - the highest available.

## Italic text
Just write the text within i-brackets:
```
[[i]]Hello :)[[/i]]
```

## Bold text
Just write the text within b-brackets:
```
[[b]]Hello :)[[/b]]
```

## Links
You can do links two ways:
```
[[link url="foo"]]bar[[/link]]
```
which will result in:
```
<a href="/read/foo">bar</a>
```
or you can write:
```
[[link url="foo"/]]
```
which will, assuming the "foo" page has a title of "Foo", result in:
```
<a href="/read/foo">Foo</a>
```
Links that lead to pages that don't exist get marked in red.  
Links to external pages get a little box at the end of the link to indicate such.  
If a display value can't be determined (the link is external, or the local page doesn't have a title) it will display the URL as the display value.

## Bullet list
Once again, you can do this two ways:
```
[[bullet/]] Blah blah blah
```
or:
```
[[*/]] Blah blah blah
```

The "value" of each bullet entry goes to the end of the line the bullet bracket started.

### Multi-level bullet lists
Just stack bullet brackets:
```
[[*/]] Blah blah blah
[[*/]][[*/]] Blah but in a subpoint to the Blah above
```

## Table
Tables are built up using the table, table-header, and table-cell brackets:
```
[[table]]
[[table-header]]
[[table-cell]]First name[[/table-cell]]
[[table-cell]]Last name[[/table-cell]]
[[/table-header]]
[[table-cell]]John[[/table-cell]]
[[table-cell]]Doe[[/table-cell]]
[[table-cell]]Jane[[/table-cell]]
[[table-cell]]Doe[[/table-cell]]
[[/table]]
```

The table-cell brackets can be replaced with the tc brackets:
```
[[table]]
[[table-header]]
[[tc]]First name[[/tc]]
[[/table-header]]
[[tc]]John[[/tc]]
[[tc]]Jane[[/tc]]
[[/table]]
```

## Table of Contents
Just put the toc bracket where you want it on the page.
**Note:** You can only have one TOC per page.
Example:
```
[[TOC/]]
```
