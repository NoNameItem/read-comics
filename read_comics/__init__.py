__version__ = "1.25.2"  # x-release-please-version
__version_info__ = tuple([int(num) if num.isdigit() else num for num in __version__.replace("-", ".", 1).split(".")])
