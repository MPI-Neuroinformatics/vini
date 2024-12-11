"""
Resampling methods to resample the image data.
"""
import numpy as np
from scipy import ndimage, __version__ as scipy_version
from distutils.version import LooseVersion
import warnings
import time

def resample_image(data, affine, shape, interpolation):
    # Extract linear and translation components
    A = affine[0:3, 0:3]
    b = affine[0:3, 3]
    shape = tuple(np.asarray(shape).astype(int))
    
    # --- Early exit checks --- #
    if shape == data.shape and np.allclose(A, np.eye(3)) and np.allclose(b, 0):
        # No transformation needed
        return data

    # 2. If we have a pure translation by an integer number of voxels and no scaling/rotation:
    #    We can handle this by slicing.
    if np.allclose(A, np.eye(3), atol=1e-10):
        # Check if b is all integers (or very close):
        if np.allclose(b, np.round(b), atol=1e-10):
            b_int = np.round(b).astype(int)
            # Apply translation by slicing if it fits inside the bounds
            src_slices = []
            dest_slices = []
            for dim_idx, (orig_size, new_size, offset) in enumerate(zip(data.shape, shape, b_int)):
                # If offset is positive, we need to start reading from offset in source
                # If offset is negative, we shift differently.
                if offset >= 0:
                    src_start = offset
                    src_end = min(orig_size, offset + new_size)
                    dest_start = 0
                    dest_end = src_end - offset
                else:
                    src_start = 0
                    src_end = min(orig_size, new_size + offset)
                    dest_start = -offset
                    dest_end = dest_start + (src_end - src_start)

                # If the transformed area is completely outside the source bounds, 
                # it would result in an empty image. Handle that by just returning an empty array.
                if src_end <= src_start or dest_end <= dest_start:
                    # No overlap
                    return np.zeros(shape, dtype=data.dtype)

                src_slices.append(slice(src_start, src_end))
                dest_slices.append(slice(dest_start, dest_end))
            
            # Construct the result array and copy
            result = np.zeros(shape, dtype=data.dtype)
            result[dest_slices[0], dest_slices[1], dest_slices[2]] = data[src_slices[0], src_slices[1], src_slices[2]]
            return result
    
    # If none of the early exits apply, proceed with the standard affine transform.
    if np.all(np.diag(np.diag(A)) == A):
        # If SciPy < 0.18.0, apply workaround
        if LooseVersion(scipy_version) < LooseVersion("0.18.0"):
            b = np.dot(np.linalg.inv(A), b)
        # Reduce A to just the diagonal elements
        A = np.diag(A)

    # Allocate result
    result = np.empty(shape, dtype=float)

    # Perform affine transform with warnings suppressed
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        ndimage.affine_transform(
            data, A, offset=b, output_shape=shape, output=result, order=interpolation
        )


    return result

if __name__ == "__main__":

    # small test of scipy's ndimage.affine_transform
    A = np.zeros((4,4))
    B = np.zeros((2,2))

    A[1,1] = 1
    A[2,2] = np.nan

    ndimage.affine_transform(A, [1,1], [2,2], (2,2), B, 0)

    print(B)
