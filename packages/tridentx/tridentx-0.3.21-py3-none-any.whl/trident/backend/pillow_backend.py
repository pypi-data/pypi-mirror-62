from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import PIL

try:
    from PIL import ImageEnhance
    from PIL import ImageOps
    from PIL import ImageFilter
    from PIL import Image as pil_image
except ImportError:
    pil_image = None
    ImageEnhance = None
    ImageFilter=None
import numpy as np
from .common import get_session
#from .load_backend import to_numpy
#__all__ = ['read_image','read_mask','save_image','save_mask','image2array','array2image','mask2array','array2mask','adjust_brightness','adjust_blur','adjust_saturation']


_session=get_session()
_backend=_session.backend
_image_backend=_session.image_backend

version=PIL.__version__
sys.stderr.write('Pillow version:{0}.\n'.format(version))



def read_image(im_path:str):
    try:
        if os.path.exists(im_path) and im_path.split('.')[-1] in ('jpg','jepg','png','bmp','tiff'):
            img=pil_image.open(im_path)
            return img
        else:
            if not os.path.exists(im_path):
                sys.stderr.write('{0} not exsit'.format(im_path))
            else:
                sys.stderr.write('extension {0} not support (jpg, jepg, png, bmp, tiff)'.format(im_path.split('.')[-1]))
            return   None
    except Exception as e:
        sys.stderr.write(e)
        return None

def read_mask(im_path:str):
    try:
        if os.path.exists(im_path) and im_path.split('.')[-1] in ('jpg','jepg','png','bmp','tiff'):
            img=pil_image.open(im_path).convert('L')
            return img
        else:
            if not os.path.exists(im_path):
                sys.stderr.write('{0} not exsit'.format(im_path))
            else:
                sys.stderr.write('extension {0} not support (jpg, jepg, png, bmp, tiff)'.format(im_path.split('.')[-1]))
            return   None
    except Exception as e:
        sys.stderr.write(e)
        return None

def save_image(arr,file_path):
    img=array2image(arr)
    img.save(file_path)

def save_mask(arr,file_path):
    img=array2mask(arr)
    img.save(file_path)

def image2array(img):
    '''

    Parameters
    ----------
    img  (string, pillow image or numpy.ndarray): Image to be converted to ndarray.

    Returns ndarray  (HWC / RGB)
    -------

    '''
    if isinstance(img,str):
        if os.path.exists(img) and img.split('.')[-1] in ('jpg','jpeg','png','bmp','tiff'):
            img=pil_image.open(img)
        else:
            return None
    arr=None
    if isinstance(img,pil_image.Image):
        arr = np.array(img).astype(_session.floatx)
    elif isinstance(img, np.ndarray):
        arr=img
        if arr.ndim not in [2, 3]:
            raise ValueError('image should be 2 or 3 dimensional. Got {} dimensions.'.format(arr.ndim))
        if arr.ndim == 3:
            if arr.shape[2] in [3, 4] and arr.shape[0] not in [3, 4]:
                pass
            elif arr.shape[0] in [3, 4]:
                arr = arr.transpose([1, 2, 0])
            else:
                raise ValueError('3d image should be 3 or 4 channel. Got {} channel.'.format(arr.shape[0]))
        arr=img.astype(_session.floatx)
    if arr.flags['C_CONTIGUOUS'] == False:
        arr = np.ascontiguousarray(arr)
    return arr


def array2image(arr:np.ndarray):
    '''

    Parameters
    ----------
    arr  ndarry  : array need to convert back to image

    Returns   pillow image
    -------

    '''
    # confirm back to numpy
    if arr.ndim not in [2, 3]:
        raise ValueError('image should be 2 or 3 dimensional. Got {} dimensions.'.format(arr.ndim))
    mode = None
    if arr.ndim == 2:
        mode = 'L'
    elif arr.ndim == 3:
        if (_backend=='tensorflow' and  arr.shape[2] in [3, 4]) or (arr.shape[2] in [3, 4] and arr.shape[0] not in [3, 4]):
            pass
        elif (_backend!='tensorflow' and  arr.shape[0] in [3, 4] and arr.shape[2] not in [3, 4]):
            arr = arr.transpose([1, 2, 0])
        elif _backend in ['pytorch', 'cntk'] and arr.ndim == 3 and arr.shape[0] in [3, 4] and arr.shape[2] not in [3, 4]:
            arr = arr.transpose([1, 2, 0])
        else:
            raise ValueError('3d image should be 3 or 4 channel. Got {} channel.'.format(arr.shape[0]))
        if arr.shape[2] == 3:
            mode = 'RGB'
        elif arr.shape[2] == 4:
            mode = 'RGBA'

    arr = np.clip(arr, 0, 255).astype(np.uint8)
    img = pil_image.fromarray(arr, mode)
    return img


def mask2array(img):
    '''

    Parameters
    ----------
    img  (string, pillow image or numpy.ndarray): Image to be converted to ndarray.

    Returns ndarray  (HW / single channel)
    -------

    '''
    if isinstance(img,str):
        if os.path.exists(img) and img.split('.')[-1] in ('jpg','jepg','png','bmp','tiff'):
            img=pil_image.open(img).convert('L')
        else:
            return None
    arr=None
    if isinstance(img,pil_image.Image):
        arr = np.array(img).astype(_session.floatx)
    elif isinstance(img, np.ndarray):
        if arr.ndim not in [2, 3]:
            raise ValueError('image should be 2 or 3 dimensional. Got {} dimensions.'.format(arr.ndim))
        if arr.ndim == 3:
            if arr.shape[3] in [3, 4] and arr.shape[0] not in [3, 4]:
                pass
            elif arr.shape[0] in [3, 4]:
                arr = arr.transpose([1, 2, 0])
            else:
                raise ValueError('3d image should be 3 or 4 channel. Got {} channel.'.format(arr.shape[0]))
        arr=img.astype(_session.floatx)
    if arr.flags['C_CONTIGUOUS'] == False:
        arr = np.ascontiguousarray(arr)
    return arr

def array2mask(arr:np.ndarray):
    '''

    Parameters
    ----------
    arr  ndarry  : array need to convert back to image

    Returns   pillow image
    -------

    '''
    # confirm back to numpy
    if arr.ndim not in [2, 3]:
        raise ValueError('image should be 2 or 3 dimensional. Got {} dimensions.'.format(arr.ndim))
    mode = None
    if arr.ndim == 2:
        arr = np.expand_dims(arr, 2)
        mode = 'L'
    elif arr.ndim == 3:
        if arr.shape[3] in [3, 4] and arr.shape[0] not in [3, 4]:
            pass
        elif arr.shape[0] in [3, 4]:
            arr = arr.transpose([1, 2, 0])
        else:
            raise ValueError('3d image should be 3 or 4 channel. Got {} channel.'.format(arr.shape[0]))
        if arr.shape[3] == 3:
            mode = 'RGB'
        elif arr.shape[3] == 4:
            mode = 'RGBA'

    arr = np.clip(arr, 0, 255).astype(np.uint8)
    img = pil_image.fromarray(arr, mode)
    return img





#調整明暗
def adjust_brightness(image,gamma):
    if gamma is None:
        gamma = np.random.choice(np.arange(0.5, 1.5, 0.1))
    ImageEnhance.Brightness(image).enhance(gamma)
    return image

#模糊
def adjust_blur(image):
    image=image.filter(ImageFilter.BLUR)
    return image

def adjust_saturation(img,saturation):
    if saturation is None:
        saturation = np.random.choice(np.arange(0.5, 2, 0.2))
    img = ImageEnhance.Color(img).enhance(saturation)
    return img
