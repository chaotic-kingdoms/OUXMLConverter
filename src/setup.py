try:
    from setuptools import setup

    install_requires = ['lxml', 'pystache', 'cssselect', 'requests', 'Pil']

    kws = {'install_requires': install_requires}
except ImportError:
    from distutils.core import setup
    kws = {}

setup(name='OUXMLConverter',
      version='0.0.1',
      author='Chaotic Kingdoms',
      url='https://github.com/chaotic-kingdoms/OUXMLConverter',
      description='Standalone script to process courses in OUXML (Open University XML) format',
      **kws)
