# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/stable/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
import recommonmark
from recommonmark.parser import CommonMarkParser
from recommonmark.transform import AutoStructify

# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_parsers = {
    '.md': CommonMarkParser,
}

source_suffix = ['.rst', '.md']

# The master toctree document.
master_doc = 'index'

# -- Project information -----------------------------------------------------

project = u'Bumblebee'
copyright = u'2012, Patrick Herrmann, John Hammerlund, and Todd Meinershagen'
author = u'Patrick Herrmann, John Hammerlund, and Todd Meinershagen'

# The short X.Y version
version = '1.2'
# The full version, including alpha/beta/rc tags
release = '1.2.0'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    'logo_only': False,
    'display_version': True
}

# html_logo = 'images/bumblebee-logo-150px.png'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'Bumblebeedoc'


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'Bumblebee.tex', u'Bumblebee Documentation',
     u'Patrick Herrmann, John Hammerlund, and Todd Meinershagen', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'bumblebee', u'Bumblebee Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'Bumblebee', u'Bumblebee Documentation',
     author, 'Bumblebee', 'Bumblebee is a .NET layer on top of the Selenium browser automation framework that allows for the standardized creation of page objects, even for dynamic web pages.',
     'Miscellaneous'),
]

## -- Custom Extensions ----------------------------------------------------

def setup(app):
    # Lets Hercule (https://www.npmjs.com/package/hercule) and Node.js scripts
    # from the 'docs/_extensions' directory to process each document before
    # it gets processed by Sphinx
    init_js_extensions(app)

    # Fixing how references (local links) work with Markdown
    app.connect('doctree-read', collect_ref_data)
    app.connect('doctree-resolved', process_refs)

    # Better support for Markdown (see https://recommonmark.readthedocs.io/en/latest/auto_structify.html)
    app.add_config_value('recommonmark_config', {
        'enable_eval_rst': True,
        'enable_auto_toc_tree': True,
        'auto_toc_tree_section': 'Contents',
    }, True)
    app.add_transform(AutoStructify)


# -- Markdown References --------------------------------------------------

def collect_ref_data(app, doctree):
    """
    Finds all anchors and references (local links) within documents,
    and saves them as meta data
    """
    filename = doctree.attributes['source'].replace(docs_dir, '').lstrip('/')
    docname = filename.replace('.md', '')

    anchors = []
    references = []

    for node in doctree.traverse(nodes.raw):
        if 'name=' in node.rawsource:
            match = re.search(r'name="([^\"]+)', node.rawsource)
            if match:
                anchors.append(match.group(1))
        elif 'id=' in node.rawsource:
            match = re.search(r'id="([^\"]+)', node.rawsource)
            if match:
                anchors.append(match.group(1))

    for node in doctree.traverse(nodes.section):
        for target in frozenset(node.attributes.get('ids', [])):
            anchors.append(target)

    for node in doctree.traverse(nodes.reference):
        uri = node.get('refuri')
        if uri and not uri.startswith(('http://', 'https://')):
            references.append(to_reference(uri, basedoc=docname))

    app.env.metadata[docname]['anchors'] = anchors
    app.env.metadata[docname]['references'] = references

def process_refs(app, doctree, docname):
    """
    Fixes all references (local links) within documents, breaks the build
    if it finds any links to non-existent documents or anchors.
    """
    for reference in app.env.metadata[docname]['references']:
        referenced_docname, anchor = parse_reference(reference)

        if referenced_docname not in app.env.metadata:
            message = "Document '{}' is referenced from '{}', but it could not be found"
            raise SphinxError(message.format(referenced_docname, docname))

        if anchor and anchor not in app.env.metadata[referenced_docname]['anchors']:
            message = "Section '{}#{}' is referenced from '{}', but it could not be found"
            raise SphinxError(message.format(referenced_docname, anchor, docname))

        for node in doctree.traverse(nodes.reference):
            uri = node.get('refuri')
            if to_reference(uri, basedoc=docname) == reference:
                node['refuri'] = to_uri(app, referenced_docname, anchor)

def to_uri(app, docname, anchor=None):
    uri = ''

    if IS_READTHEDOCS:
        language = app.config.language or 'en'
        version_name = os.environ.get('READTHEDOCS_VERSION')
        uri = '/{}/{}'.format(language, version_name)

    uri += '/{}.html'.format(docname)
    if anchor:
        uri += '#{}'.format(anchor)

    return uri

def to_reference(uri, basedoc=None):
    """
    Helper function, compiles a 'reference' from given URI and base
    document name
    """
    if '#' in uri:
        filename, anchor = uri.split('#', 1)
        filename = filename or basedoc
    else:
        filename = uri or basedoc
        anchor = None

    if not filename:
        message = "For self references like '{}' you need to provide the 'basedoc' argument".format(uri)
        raise ValueError(message)

    reference = os.path.splitext(filename.lstrip('/'))[0]
    if anchor:
        reference += '#' + anchor
    return reference

def parse_reference(reference):
    """
    Helper function, parses a 'reference' to document name and anchor
    """
    if '#' in reference:
        docname, anchor = reference.split('#', 1)
    else:
        docname = reference
        anchor = None
    return docname, anchor
