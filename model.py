"""
API models.
"""


class Housing():
    """
    A studentbostäder housing.
    """
    def __init__(self, address, url, rent):
        self.address = address
        self.url = url
        self.rent = rent
