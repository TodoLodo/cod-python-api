extensions = ['sphinx_tabs.tabs', 'sphinxcontrib.fulltoc']
sphinx_tabs_valid_builders = ['linkcheck']
sphinx_tabs_disable_tab_closing = True
def setup(app):
   app.add_lexer('alias', MyCustomLexer())
sphinx_tabs_disable_css_loading = True