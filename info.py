"""
All package info is here. By defaults, opens URL with the repo
"""

info = {
    "name": "zakhar_pycore",
    "version": "1.0",
    "description": ("Python package used by the Zakhar project (zakhar.agramakov.me). "
                    "The package contains addresses of devices, command codes, "
                    "hardware interfaces and logging"),
    "url": "https://github.com/an-dr/zakhar_pycore",
    "author": "Andrei Gramakov",
    "author_email": "mail@agramakov.me",
    "install_requires": [line.rstrip('\n') for line in open("requirements.txt")],  # reading requirements.txt content
    "license": "MIT",
}

if __name__ == '__main__':
    import webbrowser

    webbrowser.open(info["url"])
