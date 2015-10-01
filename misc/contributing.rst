############################
Contributing to this project
############################

Are you interested in contributing to this project, or just interested
in learning what goes into it?  Then this is the page for you!

There are two main areas of work:  maintaining and improving the
existing content (walkthrough chapters and tutorials), and adding
new tutorials.

At the moment I'm focussing on updating Tiny Pirate's
`old tutorials <http://afteractionreporter.com/dwarf-fortress-tutorials/>`_ -
the chapters are written for DF v0.28.181.40d, which was
released in 2008!

If you want to help out by improving existing chapters and tutorials,
that would be much appreciated.  I'm also very happy to take bug reports!
(for the updated chapters, anyway - I know the old ones are old!)

You can `find the project on Github
<https://github.com/PeridexisErrant/DF-Walkthrough>`_.

If this sounds like a lot of work - and it is - you can
`support me on Patreon <https://www.patreon.com/PeridexisErrant>`_ instead.


How to turn text into the website
=================================
Anyone who wants to contribute content, fix a bug, or just have an offline
copy need to turn the text files into the website.  Luckily, this is
pretty easy!  You only need two things installed:

* `Python <https://www.python.org>`_.
  If you're on OSX or Linux, Python is probably already installed.
  If it isn't, or you're on Windows, install it from the site above.

* `Sphinx <http://sphinx-doc.org>`_.  With Python installed, just run
  ``pip install -U Sphinx`` in a terminal / command prompt.  If you're
  using an old Python version and that doesn't work, the site has
  alternative install instructions.

Get the code from the GitHub repo, either by forking the repo if you want
to contribute), or usig the 'download ZIP' option and unzipping the folder.

Congratulations, you now have the text!  There's only one more step:
open a command prompt in the DF-Walkthrough folder, and run ``make html``

That's it!


Authors and Contributors
========================
.. note to authors

    Anyone who's contributed more than a bug report should be here -
    add yourself if you're not!*

PeridexisErrant and TinyPirate.


Contribution standards
======================
This section describes the target standard for the project.
Not all pages will meet it, and that's OK.  Don't let them stop you
adding something - but feel free to apply them to existing content!


Content
-------
The walkthrough chapters cover core knowledge, with a clear progression
of skills. If a topic can be put in a self-contained tutorial, it should
be.  Prefer linking to a tutorial over adding a section to the walkthrough.

The tutorials each cover a single, self-contained topic.  Tutorials
are aimed at players who have just finished the walkthrough.  They
introduce core topics not covered in the walkthrough.


Style
-----
Use clear, direct, and simple language.  Avoid jargon or the passive voice.
I find the `hemmingway editor <http://www.hemingwayapp.com>`_ useful;
I often ignore but always consider it's suggestions.

Keep all lines to 80 characters or less.  Sphinx will automatically join
everything between blank lines into one paragraph, and short lines
make the raw text easier to read for editors.  More importantly, short
lines make version-control software much more useful.  When writing
new text, keep to about 70 characters to avoid many lines changing for
small edits later.  Do not use tabs or leave trailing whitespace.

You can check with ``python misc/lint.py && make clean && make html`` -
this sequence of commands should always run without errors, or
at least give warnings about specific files and line numbers!


Markup
------
Markup should be fairly minimal and let readers focus on the text.
Basic markup helps with this, and should be used where appropriate.
If in doubt, just match the surrounding sections.

Headings:

* File headings over- and underlined with ``#####``
* Section headings underlined with ``====``
* Subsections generally avoided, but underlined with ``----`` otherwise

Lists:

* Bulleted lists use ``*`` and one space.  Use these instead of a paragraph
  for sections such as a list of examples or sequence of commands.
* Use numbered lists only when the ordering is both important and unclear
  from context.  Use ``#.`` and one space, so renumbering will be automatic
  if the list is changed later.

Special text:

* Use bold, italics, etc. very sparingly - add meaning, not just emphasis.
* For keybindings, use the ``:kbd:`Key``` directive, which is rendered
  with the special style.  Keys are case sensitive, so ``:kbd:`Shift```
  should never be used (unlike :kbd:`Esc`, :kbd:`Space`, etc.).
* For in-game text, use the ``:guilabel:`In game text``` directive, which
  is rendered with the appropriate font and background.  Ensure that phrasing
  and capitalisation matches DF exactly (except ``'``, which renders as
  :guilabel:`'` - leave it out).  Don't use this style for ASCII art, only
  ingame menus which should be read as text.


TODO list
=========
*There's a lot to do; this list is roughly in order of priority but
items may be done in other orders for whatever reason.*

#. Update all content for DF2014.  Preferably *before* the next DF release
#. Use ``:kbd:`` and ``:guilabel:`` roles everywhere; see chapter one and two
#. Update all images and make sure descriptions match
#. Run everything through Hemmingway
#. Make usage / reading a nicer experience for new players
#. Make contributing easier and more rewarding
#. Add more tutorials; eg modding, quantum stockpiles, graphics, etc
#. Add an adventure mode walkthrough

