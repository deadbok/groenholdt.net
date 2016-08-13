'''
Config file for my personal blog.
'''
CONFIG = {
        'AUTHOR': 'Martin Bo Kristensen Grønholdt',
        'SITEURL': 'https://groenholdt.net',
        'SITENAME': 'Homepage V. 5.1.3',
        'POSTSPERINDEX': 6,
        'METAPARSERS': ['CategoryMetaParser'],
        'GENERATORS': ['BlogIndexGenerator', 'CategoryIndexGenerator', 'TagCloudGenerator'],
        'CONTENTFILTERS': ['LocalURL']
}
