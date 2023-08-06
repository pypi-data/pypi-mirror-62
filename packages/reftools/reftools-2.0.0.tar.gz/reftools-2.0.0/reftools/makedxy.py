"""Generate DXY reference files from a grid of points."""
import numpy as np
from astropy.io import fits

__all__ = ['run', 'help']


def run(in_list, output, xstep=64, ystep=64, shape=(2048, 4096),
        template=None, order=1, expand=True, verbose=True, overwrite=True):
    """Create a full-frame DXY reference file derived from a sub-sampled grid
    of values read in from the ASCII files specified in the list of filenames
    given in ``in_list``.


    The input file specified by the first filename are assumed to contain the
    corrections for ``SCI,1`` data, while the second file will be used to
    create the extension associated with ``SCI,2``, and so on for as many chips
    as the needed for the instrument/detector. Each of the input files
    should have the columns::

        x   y   dx   dy

    The parameter ``shape`` needs to specify the full-readout shape of each
    chip as ``[ny, nx]`` and all chips are assumed to have the same shape.

    If ``expand`` is `False`, only the sub-sampled arrays will be written out
    to the file without interpolating to the full-chip readout size.

    The FITS file specified by ``output`` will be created as a multi-extension
    reference file with the same structure as the ACS full-frame DXY files.
    If a template filename is provided, the headers from that file will be
    copied as the headers for the output file.

    .. warning::

        No information in the template headers will be edited during
        this process!

    Examples
    --------
    >>> from reftools import makedxy
    >>> makedxy.run([fname1, ..., fnameN], output)  # doctest: +SKIP

    """
    # start by creating FITS object
    fimg = fits.HDUList()
    phdu = fits.PrimaryHDU(header=get_template_hdr(template, None))
    fimg.append(phdu)

    # Now, start creating each of the extensions
    for fname, extver in zip(in_list, list(range(1, len(in_list) + 1))):
        if verbose:
            print(f'Converting data from {fname} into DXY extensions.')
        # read in the raw data for each chip from the ASCII file
        x, y, dx, dy = np.loadtxt(fname, usecols=(0, 1, 2, 3), unpack=True)
        # for each axis
        for extname, vals in zip(['DX', 'DY'], [dx, dy]):
            if verbose:
                print(f'Processing extension {extname}, {extver}')
            varr = convert_ascii_to_array(x, y, vals)
            if expand:
                vout = expand_array(varr, shape, spline_order=order)
            else:
                vout = varr
            # Create HDU
            hdu = fits.ImageHDU(
                data=vout,
                header=get_template_hdr(template, extname, extver))
            # specifically set the extname and extver to what we know to be
            # correct just in case the template file is not ordered the same
            hdu.header['EXTNAME'] = extname
            hdu.header['EXTVER'] = extver

            hdu.header['CDELT1'] = xstep
            hdu.header['CDELT2'] = ystep

            # Append new HDU to FITS file
            fimg.append(hdu)

    # Write out newly created FITS object to a FITS file
    if verbose:
        print(f'Writing out new reference file to: {output}')
    fimg.writeto(output, overwrite=overwrite)
    fimg.info()


def get_template_hdr(template, extname, extver=1):
    """Return the header from the FITS file ``template`` for the extension
    ``extname,extver``. If ``template`` is `None`, blank, or N/A, it will
    return `None`.

    """
    if template in (None, '', 'N/A', 'n/a'):
        return

    if extname in (None, 'PRIMARY'):
        extn = 0
    else:
        # count number of extensions with 'extname' in template
        # if we are trying to create an extension with 'extver' larger than
        # what the template file contains, simply use 'extver' == 1 from
        # template
        tmax = 1
        with fits.open(template) as timg:
            for e in timg:
                if 'extver' in e.header and e.header['extver'] > tmax:
                    tmax = e.header['extver']
        if extver > tmax:
            extver = 1

        extn = (extname, extver)

    return fits.getheader(template, extn)


def convert_ascii_to_array(x, y, vals):
    """Convert a list of values ``vals`` corresponding to pixel positions
    ``x,y`` into an array.
    """
    return vals.reshape([y.max(), x.max()])


def expand_array(input, output_shape, spline_order=1):
    """Expand the input array ``input`` to create a new array with the shape
    specified by ``output_shape`` with spline interpolation order given by
    ``spline_order``. The default interpolation of 1 corresponds to bilinear
    interpolation.

    This implementation is based on the recipe posted in the SciPy cookbook at
    http://www.scipy.org/Cookbook/Interpolation .

    """
    from scipy import ndimage

    # define range of x and y values spanned by input array
    stepx = output_shape[1] // (input.shape[1] - 1)
    stepy = output_shape[0] // (input.shape[0] - 1)
    x = np.transpose(np.array(
        [list(range(0, output_shape[1] + 1, stepx))], np.float32))
    y = np.array(
        [list(range(0, output_shape[0] + 1, stepy))], dtype=np.float32)
    # define range of x and y values to be filled in output array
    nx = np.arange(0, output_shape[1], 1, dtype=np.int32)
    ny = np.arange(0, output_shape[0], 1, dtype=np.int32)
    newx, newy = np.meshgrid(nx, ny)

    # initialize transformation from input to output coordinates
    # Algorithm used here copied from:
    # http://www.scipy.org/Cookbook/Interpolation
    x0 = x[0, 0]
    y0 = y[0, 0]
    dx = x[1, 0] - x0
    dy = y[0, 1] - y0
    ivals = (newx - x0) / dx
    jvals = (newy - y0) / dy
    coords = np.array([jvals, ivals])
    return ndimage.map_coordinates(input, coords, order=spline_order)


def help():
    """Print help."""
    print(__doc__)
    print(run.__doc__)
