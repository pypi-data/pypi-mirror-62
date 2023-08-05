# -*- coding: utf-8 -*-
from math import factorial
import operator

import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy.optimize import curve_fit
from scipy.signal import argrelextrema

try:
    from lmfit import Model
    _has_lmfit = True
except ImportError:
    _has_lmfit = False


from pysprint.utils import (
    findNearest, _handle_input, lmfit_disp, fourier_interpolate
    )


__all__ = [
    'min_max_method', 'cos_fit1', 'cos_fit2', 'cos_fit3',
    'cos_fit4', 'cos_fit5', 'spp_method', 'cff_method', 'fft_method',
    'cut_gaussian', 'ifft_method', 'args_comp'
    ]


def min_max_method(
        initSpectrumX, initSpectrumY, referenceArmY, sampleArmY, ref_point,
        maxx=None, minx=None, fitOrder=5, showGraph=False
        ):
    """Calculates the dispersion with minimum-maximum method

    Parameters
    ----------

    initSpectrumX: array-like
    x-axis data

    initSpectrumY: array-like
    y-axis data

    referenceArmY, sampleArmY: array-like
    reference and sample arm spectra evaluated at initSpectrumX

    ref_point: float
    the reference point to calculate order

    maxx and minx: array-like, optional
    the accepted minimal and maximal x values (if you want to manually pass)

    fitOrder: int, optional
    degree of polynomial to fit data [1, 5]

    showGraph: bool, optional
    if True returns a matplotlib plot and pauses execution until closing the window

    Returns
    -------

    dispersion: array-like
    [GD, GDD, TOD, FOD, QOD]

    dispersion_std: array-like
    [GD_std, GDD_std, TOD_std, FOD_std, QOD_std]

    fit_report: lmfit report object
    """
    Xdata, Ydata = _handle_input(
        initSpectrumX, initSpectrumY, referenceArmY, sampleArmY
        )
    if maxx is None:
        maxInd = argrelextrema(Ydata, np.greater)
        maxx = Xdata[maxInd]
    if minx is None:
        minInd = argrelextrema(Ydata, np.less)
        minx = Xdata[minInd]

    _, ref_index = findNearest(Xdata, ref_point)

    relNegMaxFreqs = np.array([a for a in (Xdata[ref_index] - maxx) if a < 0])
    relNegMinFreqs = np.array([b for b in (Xdata[ref_index] - minx) if b < 0])
    relNegFreqs = sorted(np.append(relNegMaxFreqs, relNegMinFreqs))
    relNegFreqs = relNegFreqs[::-1]
    relPosMaxFreqs = np.array([c for c in (Xdata[ref_index] - maxx) if c > 0])
    relPosMinFreqs = np.array([d for d in (Xdata[ref_index] - minx) if d > 0])
    relPosFreqs = sorted(np.append(relPosMinFreqs, relPosMaxFreqs))

    if len(relNegFreqs) == 0 and len(relPosFreqs) == 0:
        raise ValueError('No extremal points found.')
    negValues = np.zeros_like(relNegFreqs)
    posValues = np.zeros_like(relPosFreqs)
    for freq in range(len(relPosFreqs)):
        posValues[freq] = np.pi * (freq + 1)
    for freq in range(len(relNegFreqs)):
        negValues[freq] = np.pi * (freq + 1)
    x_s = np.append(relPosFreqs, relNegFreqs)
    y_s = np.append(posValues, negValues)

    # FIXME: Do we even need this?
    idx = np.argsort(x_s)
    fullXValues, fullYValues = x_s[idx], y_s[idx]
    
    if _has_lmfit:
        if fitOrder == 5:
            fitModel = Model(polynomialFit5)
            params = fitModel.make_params(b0=0, b1=1, b2=1, b3=1, b4=1, b5=1)
            result = fitModel.fit(fullYValues, x=fullXValues, params=params, method='leastsq')
        elif fitOrder == 4:
            fitModel = Model(polynomialFit4)
            params = fitModel.make_params(b0=0, b1=1, b2=1, b3=1, b4=1)
            result = fitModel.fit(fullYValues, x=fullXValues, params=params, method='leastsq')
        elif fitOrder == 3:
            fitModel = Model(polynomialFit3)
            params = fitModel.make_params(b0=0, b1=1, b2=1, b3=1)
            result = fitModel.fit(fullYValues, x=fullXValues, params=params, method='leastsq')
        elif fitOrder == 2:
            fitModel = Model(polynomialFit2)
            params = fitModel.make_params(b0=0, b1=1, b2=1)
            result = fitModel.fit(fullYValues, x=fullXValues, params=params, method='leastsq')
        elif fitOrder == 1:
            fitModel = Model(polynomialFit1)
            params = fitModel.make_params(b0=0, b1=1)
            result = fitModel.fit(fullYValues, x=fullXValues, params=params, method='leastsq')
        else:
            raise ValueError('Order is out of range, please select from [1,5]')
    else:
        if fitOrder == 5:
            popt, pcov = curve_fit(polynomialFit5, fullXValues, fullYValues, maxfev=8000)
            _function = polynomialFit5
        elif fitOrder == 4:
            popt, pcov = curve_fit(polynomialFit4, fullXValues, fullYValues, maxfev=8000)
            _function = polynomialFit4
        elif fitOrder == 3:
            popt, pcov = curve_fit(polynomialFit3, fullXValues, fullYValues, maxfev=8000)
            _function = polynomialFit3
        elif fitOrder == 2:
            popt, pcov = curve_fit(polynomialFit2, fullXValues, fullYValues, maxfev=8000)
            _function = polynomialFit2
        elif fitOrder == 1:
            popt, pcov = curve_fit(polynomialFit1, fullXValues, fullYValues, maxfev=8000)
            _function = polynomialFit1
        else:
            raise ValueError('Order is out of range, please select from [1,5]')
    try:
        if _has_lmfit:
            dispersion, dispersion_std = lmfit_disp(result.params.items())
            dispersion = dispersion[1:]
            dispersion_std = dispersion_std[1:]
            for idx in range(len(dispersion)):
                dispersion[idx] = dispersion[idx] * factorial(idx+1)
                dispersion_std[idx] = dispersion_std[idx] * factorial(idx+1)
            while len(dispersion) < 5:
                dispersion.append(0)
                dispersion_std.append(0)
            fit_report = result.fit_report()
        else:
            fullXValues = np.asarray(fullXValues)
            dispersion = []
            dispersion_std = []
            for idx in range(len(popt) - 1):
                dispersion.append(popt[idx + 1] * factorial(idx + 1))
            while len(dispersion) < 5:
                dispersion.append(0)
            while len(dispersion_std) < len(dispersion):
                dispersion_std.append(0)
            fit_report = '\nTo display detailed results, you must have lmfit installed.'
        if showGraph:
            fig = plt.figure(figsize=(7, 7))
            fig.canvas.set_window_title('Min-max method fitted')
            plt.plot(fullXValues, fullYValues, 'o', label='dataset')
            try:
                plt.plot(fullXValues, result.best_fit, 'r*', label='fitted')
            except Exception:
                plt.plot(fullXValues, _function(fullXValues, *popt), 'r*', label='fitted')
            plt.legend()
            plt.grid()
            plt.show()
        return dispersion, dispersion_std, fit_report
    except Exception as e:
        return [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], e


def polynomialFit5(x, b0, b1, b2, b3, b4, b5):
    """
    Taylor polynomial for fit
    b1 = GD
    b2 = GDD / 2
    b3 = TOD / 6
    b4 = FOD / 24
    b5 = QOD / 120
    """
    return b0+b1*x+b2*x**2+b3*x**3+b4*x**4+b5*x**5


def polynomialFit4(x, b0, b1, b2, b3, b4):
    """
    Taylor polynomial for fit
    b1 = GD
    b2 = GDD / 2
    b3 = TOD / 6
    b4 = FOD / 24
    """
    return b0+b1*x+b2*x**2+b3*x**3+b4*x**4


def polynomialFit3(x, b0, b1, b2, b3):
    """
    Taylor polynomial for fit
    b1 = GD
    b2 = GDD / 2
    b3 = TOD / 6

    """
    return b0+b1*x+b2*x**2+b3*x**3


def polynomialFit2(x, b0, b1, b2):
    """
    Taylor polynomial for fit
    b1 = GD
    b2 = GDD / 2
    """
    return b0+b1*x+b2*x**2


def polynomialFit1(x, b0, b1):
    """
    Taylor polynomial for fit
    b1 = GD
    """
    return b0+b1*x


def cos_fit1(x, c0, c1, b0, b1):
    return c0 + c1 * np.cos(polynomialFit1(x, b0, b1))


def cos_fit2(x, c0, c1, b0, b1, b2):
    return c0 + c1 * np.cos(polynomialFit2(x, b0, b1, b2))


def cos_fit3(x, c0, c1, b0, b1, b2, b3):
    return c0 + c1 * np.cos(polynomialFit3(x, b0, b1, b2, b3))


def cos_fit4(x, c0, c1, b0, b1, b2, b3, b4):
    return c0 + c1 * np.cos(polynomialFit4(x, b0, b1, b2, b3, b4))


def cos_fit5(x, c0, c1, b0, b1, b2, b3, b4, b5):
    return c0 + c1 * np.cos(polynomialFit5(x, b0, b1, b2, b3, b4, b5))


def spp_method(delays, omegas, reference_point=0, fitOrder=4, from_raw=False):
    """
    Calculates the dispersion from SPP's positions and delays.

    Parameters
    ----------

    delays: array-like
    the time delays in fs
    if from_raw is enabled you must pass matching pairs with omegas

    omegas: array-like
    in form of [[SPP1, SPP2, SPP3, SPP4],[SPP1, SPP2, SPP3, SPP4], ..]
    for lesser SPP cases replace elements with None:
    [[SPP1, None, None, None],[SPP1, None, None, None], ..]
    if from_raw is enabled, you must pass matching pairs with delays

    fitOrder: int
    order of polynomial to fit the given data

    from_raw: bool
    if True you can pass matching pairs to delays and omegas, and it will perform
    a normal curve fitting. It's useful at the API.

    Returns
    -------
    omegas_unpacked: array-like
    x axis data

    delays_unpacked : array-like
    y axis data

    dispersion: array-like
    [GD, GDD, TOD, FOD, QOD]

    dispersion_std: array-like
    [GD_std, GDD_std, TOD_std, FOD_std, QOD_std]

    bf: array-like
    best fitting curve for plotting
    """
    if from_raw:
        delays_unpacked = delays
        omegas_unpacked = omegas
    else:
        delays = delays[delays != np.array(None)]
        omegas_unpacked = []
        delays_unpacked = []
        for delay, element in zip(delays, omegas):
            item = [x for x in element if x is not None]
            omegas_unpacked.extend(item)
            delays_unpacked.extend(len(item) * [delay])
    # FIXME: should be numpy arrays..
    L = sorted(zip(omegas_unpacked, delays_unpacked), key=operator.itemgetter(0))
    omegas_unpacked, delays_unpacked = zip(*L)
    omegas_unpacked = [val-reference_point for val in omegas_unpacked]
    try:
        if _has_lmfit:
            if fitOrder == 2:
                fitModel = Model(polynomialFit2)
                params = fitModel.make_params(b0=1, b1=1, b2=1)
                result = fitModel.fit(delays_unpacked, x=omegas_unpacked, params=params, method='leastsq')
            elif fitOrder == 3:
                fitModel = Model(polynomialFit3)
                params = fitModel.make_params(b0=1, b1=1, b2=1, b3=1)
                result = fitModel.fit(delays_unpacked, x=omegas_unpacked, params=params, method='leastsq')
            elif fitOrder == 4:
                fitModel = Model(polynomialFit4)
                params = fitModel.make_params(b0=1, b1=1, b2=1, b3=1, b4=1)
                result = fitModel.fit(delays_unpacked, x=omegas_unpacked, params=params, method='leastsq')
            elif fitOrder == 1:
                fitModel = Model(polynomialFit1)
                params = fitModel.make_params(b0=1, b1=1)
                result = fitModel.fit(delays_unpacked, x=omegas_unpacked, params=params, method='leastsq')
            else:
                raise ValueError('Order is out of range, please select from [1,4]')
            dispersion, dispersion_std = lmfit_disp(result.params.items())
            for idx in range(len(dispersion)):
                dispersion[idx] = dispersion[idx]*factorial(idx)
            for idx in range(len(dispersion_std)):
                if dispersion_std[idx] is not None:
                    dispersion_std[idx] = dispersion_std[idx] * factorial(idx)
                else:
                    dispersion_std[idx] = 0
            while len(dispersion) < 5:
                dispersion.append(0)
                dispersion_std.append(0)
            while len(dispersion_std) < 5:
                dispersion_std.append(0)
            bf = result.best_fit
        else:
            if fitOrder == 4:
                popt, pcov = curve_fit(polynomialFit4, omegas_unpacked, delays_unpacked, maxfev=8000)
                _function = polynomialFit4
            elif fitOrder == 3:
                popt, pcov = curve_fit(polynomialFit3, omegas_unpacked, delays_unpacked, maxfev=8000)
                _function = polynomialFit3
            elif fitOrder == 2:
                popt, pcov = curve_fit(polynomialFit2, omegas_unpacked, delays_unpacked, maxfev=8000)
                _function = polynomialFit2
            elif fitOrder == 1:
                popt, pcov = curve_fit(polynomialFit1, omegas_unpacked, delays_unpacked, maxfev=8000)
                _function = polynomialFit1
            else:
                raise ValueError('Order is out of range, please select from [1,4]')
            omegas_unpacked = np.asarray(omegas_unpacked)
            dispersion = []
            dispersion_std = []
            for idx in range(len(popt)):
                dispersion.append(popt[idx] * factorial(idx))
            while len(dispersion) < 5:
                dispersion.append(0)
            while len(dispersion_std) < len(dispersion):
                dispersion_std.append(0)
            bf = _function(omegas_unpacked, *popt)
        return omegas_unpacked, delays_unpacked, dispersion, dispersion_std, bf
    except Exception as e:
        return [], [], [e], [], []


def cff_method(
        initSpectrumX, initSpectrumY, referenceArmY, sampleArmY, ref_point=0,
        p0=[1, 1, 1, 1, 1, 1, 1, 1], maxtries=8000
        ):
    """
    Phase modulated cosine function fit method.


    Parameters
    ----------

    initSpectrumX: array-like
    x-axis data

    initSpectrumY: array-like
    y-axis data

    referenceArmY, sampleArmY: array-like
    the reference and sample arm spectra evaluated at initSpectrumX

    p0: array-like
    the initial parameters for fitting

    Returns
    -------

    dispersion: array-like
    [GD, GDD, TOD, FOD, QOD]

    bf: array-like
    best fitting curve

    """
    # TODO: BOUNDS WILL BE SET  ..
    # bounds=((-1000, -10000, -10000, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf),
    # (1000, 10000, 10000, np.inf, np.inf, np.inf, np.inf, np.inf))
    Xdata, Ydata = _handle_input(
        initSpectrumX, initSpectrumY, referenceArmY, sampleArmY
        )
# TODO: replace with lmfit
    try:
        if len(np.trim_zeros(p0, 'b')) + 4 == len(p0):
            _funct = cos_fit1
            p0 = p0[:-4]
        elif p0[-1] == 0 and p0[-2] == 0 and p0[-3] == 0:
            _funct = cos_fit2
            p0 = p0[:-3]
        elif p0[-1] == 0 and p0[-2] == 0:
            _funct = cos_fit3
            p0 = p0[:-2]
        elif p0[-1] == 0:
            _funct = cos_fit4
            p0 = p0[:-1]
        else:
            _funct = cos_fit5
        popt, pcov = curve_fit(_funct, Xdata-ref_point, Ydata, p0, maxfev=maxtries)
        dispersion = np.zeros_like(popt)[:-3]
        for num in range(len(popt)-3):
            dispersion[num] = popt[num+3]*factorial(num+1)
        return dispersion, _funct(Xdata-ref_point, *popt)
    except RuntimeError:
        raise ValueError(f'Max tries ({maxtries}) reached.. \nParameters could not be estimated.')


def fft_method(initSpectrumX, initSpectrumY):
    """Perfoms FFT on data

    Parameters
    ----------

    initSpectrumX: array-like
    the x-axis data

    initSpectrumY: array-like
    the y-axis data

    Returns
    -------
    xf: array-like
    the transformed x data

    yf: array-like
    transformed y data
    """
    if len(initSpectrumY) > 0 and len(initSpectrumX) > 0:
        Ydata = initSpectrumY
        Xdata = initSpectrumX
    else:
        raise FileNotFoundError
    yf = scipy.fftpack.fft(Ydata)
    xf = np.linspace(Xdata[0], Xdata[-1], len(Xdata))
    return xf, yf


def gaussian_window(t, tau, standardDev, order):
    """
    Returns a simple gaussian window of given parameters evaulated at t.

    Parameters
    ----------
    t: array-like
    input array to perform window on

    tau: float
    center of gaussian window

    standardDev: float
    FWHM of given gaussian

    order: float
    order of gaussian window. If not even it's incremented by 1.

    Returns
    -------
    array : array-like
    nth order gaussian window with params above

    """
    if order % 2 == 1:
        order += 1
    std = standardDev/(2 * (np.log(2)**(1 / order)))
    return np.exp(-((t - tau)**order)/(std**order))


def cut_gaussian(initSpectrumX, initSpectrumY, spike, sigma, win_order):
    """
    Applies gaussian window with the given params.

    Parameters
    ----------
    initSpectrumX: array-like
    x-axis data

    initSpectrumY: array-like
    y-axis data

    spike: float
    center of gaussian window

    sigma: float
    Full width at half max

    Returns
    -------

    Ydata: array-like
    the windowed y values
    """
    Ydata = initSpectrumY * gaussian_window(initSpectrumX, tau=spike, standardDev=sigma, order=win_order)
    return Ydata


def ifft_method(initSpectrumX, initSpectrumY, interpolate=True):
    """
    Perfoms IFFT on data

    Parameters
    ----------

    initSpectrumX: array-like
    the x-axis data

    initSpectrumY: array-like
    the y-axis data

    interpolate: bool
    if True perform a linear interpolation on dataset before transforming

    Returns
    -------
    xf: array-like
    the transformed x data

    yf: array-like
    transformed y data

    """
    if len(initSpectrumY) > 0 and len(initSpectrumX) > 0:
        Ydata = initSpectrumY
        Xdata = initSpectrumX
    else:
        raise ValueError
    N = len(Xdata)
    if interpolate:
        Xdata, Ydata = fourier_interpolate(Xdata, Ydata)
    xf = np.fft.fftfreq(N, d=(Xdata[1]-Xdata[0])/(2*np.pi))
    yf = np.fft.ifft(Ydata)
    return xf, yf


def args_comp(
        initSpectrumX, initSpectrumY, reference_point=0, fitOrder=5, showGraph=False
        ):
    """
    Calculates the phase of complex dataset then unwrap by changing deltas between
    values to 2*pi complement. At the end, fit a polynomial curve to determine
    dispersion coeffs.

    Parameters
    ----------

    initSpectrumX: array-like
    the x-axis data

    initSpectrumY: array-like
    the y-axis data

    reference_point: float
    the reference point to calculate order

    fitOrder: int
    degree of polynomial to fit data [1, 5]

    showGraph: bool
    if True returns a matplotlib plot and pauses execution until closing the window

    Returns
    -------

    dispersion: array-like
    [GD, GDD, TOD, FOD, QOD]

    dispersion_std: array-like
    [GD_std, GDD_std, TOD_std, FOD_std, QOD_std]

    fit_report: lmfit report
    """
    Xdata = initSpectrumX-reference_point
    angles = np.angle(initSpectrumY)
    # shifting to [0, 2pi] if necessary
    # angles = (angles + 2 * np.pi) % (2 * np.pi)
    Ydata = np.unwrap(angles, axis=0)
    if fitOrder == 5:
        fitModel = Model(polynomialFit5)
        params = fitModel.make_params(b0=0, b1=1, b2=1, b3=1, b4=1, b5=1)
        result = fitModel.fit(Ydata, x=Xdata, params=params, method='leastsq')
    elif fitOrder == 4:
        fitModel = Model(polynomialFit4)
        params = fitModel.make_params(b0=0, b1=1, b2=1, b3=1, b4=1)
        result = fitModel.fit(Ydata, x=Xdata, params=params, method='leastsq')
    elif fitOrder == 3:
        fitModel = Model(polynomialFit3)
        params = fitModel.make_params(b0=0, b1=1, b2=1, b3=1)
        result = fitModel.fit(Ydata, x=Xdata, params=params, method='leastsq')
    elif fitOrder == 2:
        fitModel = Model(polynomialFit2)
        params = fitModel.make_params(b0=0, b1=1, b2=1)
        result = fitModel.fit(Ydata, x=Xdata, params=params, method='leastsq')
    elif fitOrder == 1:
        fitModel = Model(polynomialFit1)
        params = fitModel.make_params(b0=0, b1=1)
        result = fitModel.fit(Ydata, x=Xdata, params=params, method='leastsq')
    else:
        raise ValueError('Order is out of range, please select from [1,5]')
    try:
        dispersion, dispersion_std = lmfit_disp(result.params.items())
        dispersion = dispersion[1:]
        dispersion_std = dispersion_std[1:]
        for idx in range(len(dispersion)):
            dispersion[idx] = dispersion[idx] * factorial(idx+1)
            dispersion_std[idx] = dispersion_std[idx] * factorial(idx+1)
        while len(dispersion) < 5:
            dispersion.append(0)
            dispersion_std.append(0)
        fit_report = result.fit_report()
        if showGraph:
            fig = plt.figure(figsize=(7, 7))
            fig.canvas.set_window_title('Phase')
            plt.plot(Xdata, Ydata, 'o', label='dataset')
            plt.plot(Xdata, result.best_fit, 'r--', label='fitted')
            plt.legend()
            plt.grid()
            plt.show()
        return dispersion, dispersion_std, fit_report
    except Exception as e:
        return [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], e
