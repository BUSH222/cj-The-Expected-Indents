from io import BytesIO

import numpy as np
import requests
from numpy.linalg import svd as SVD
from PIL import Image


def scale(A):
    """Scale the matrix A to the range [0, 255]

    Args:
        A (np.array): Matrix to scale

    Returns:
        np.array: Scaled matrix
    """
    up = A.max()
    lo = A.min()
    if up == lo or (up == 255 and lo == 0):
        return A
    return ((A - lo) / (up - lo) * 255).astype(np.uint8)


class SVDImage:
    """Class for image compression using SVD"""

    def __init__(self, word, size=512, verbose=True):
        self.size = size
        self.word = word
        self._fetch_image(word)  # self.A is defined by this function
        if len(self.A.shape) != 3:
            raise ValueError("Image does not have 3 channels")
        # separating the R, G and B channels to 2D matrices
        self.R = self.A[:, :, 0]
        self.G = self.A[:, :, 1]
        self.B = self.A[:, :, 2]

        if verbose:
            print("SVD for Red Channel")
        U, S, V = SVD(self.R)
        S = np.diag(S)
        self.RU, self.RS, self.RV = U, S, V

        if verbose:
            print("SVD for Green Channel")
        U, S, V = SVD(self.G)
        S = np.diag(S)
        self.GU, self.GS, self.GV = U, S, V

        if verbose:
            print("SVD for Blue Channel")
        U, S, V = SVD(self.B)
        S = np.diag(S)
        self.BU, self.BS, self.BV = U, S, V

    def _fetch_image(self, word):
        """Fetch image from loremflickr API using word

        Args:
            word (str): Image search term
        """
        res = requests.get(f"https://loremflickr.com/512/512/{word}", timeout=10)
        image = Image.open(BytesIO(res.content))
        image = image.resize((self.size, self.size))
        self.A = np.array(image)

    def reduce(self, terms, type=np.uint8):
        """Reduce the image to the specified number of terms

        Args:
            terms (int): Number of terms to keep
            type (numpy type, optional): Type of the returned array. Defaults to np.uint8.

        Returns:
            _type_: _description_
        """
        R_ = scale(
            self.RU[:, :terms] @ self.RS[:terms, :terms] @ self.RV[:terms, :]
        ).astype(np.uint8)

        G_ = scale(
            self.GU[:, :terms] @ self.GS[:terms, :terms] @ self.GV[:terms, :]
        ).astype(np.uint8)

        B_ = scale(
            self.BU[:, :terms] @ self.BS[:terms, :terms] @ self.BV[:terms, :]
        ).astype(np.uint8)

        return np.dstack((R_, G_, B_)).astype(type)
