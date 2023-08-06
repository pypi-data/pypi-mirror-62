import logging
import random
import numpy as np
import pandas as pd
from astropy.coordinates import SkyCoord
import astropy.units as u

from pyobs import PyObsModule
from pyobs.interfaces import IAcquisition
from pyobs.utils.time import Time

log = logging.getLogger(__name__)

# 20150607S-0189;-10 41 26.122;00 41 36.833;28 52 45.427;00 03 54.322;00 00 00.000;13 51 21.016;00 00 00.000;00 00 00.000;
# Name;AZ;PMcorrAz;ZD;PMcorrZD;DEROT;DEROTOFF;DOME;DOMEOFF


class PointingMastermind(PyObsModule):
    """Mastermind that acts as a state machine."""

    def __init__(self, min_alt: int = 15, max_alt: int = 85, num_alt: int = 8, num_az: int = 24, finish: int = 90,
                 catalog: str = '/pyobs/pointing_cat.csv', max_distance: float = 5, acquisition: str = 'acquisition',
                 *args, **kwargs):
        """Initialize a new auto focus system.

        Args:
            min_alt: Mininum altitude to use.
            max_alt: Maximum altidude to use.
            num_alt: Number of altitude points to create on grid.
            num_az: Number of azimuth points to create on grid.
            finish: When this number in percent of points have been finished, terminate mastermind.
            catalog: Name of catalog file.
            max_distance: Maximum distance in degrees of catalog star to grid point.
            acquisition: IAcquisition unit to use.
        """
        PyObsModule.__init__(self, *args, **kwargs)

        # add thread func
        self._add_thread_func(self._run_thread, False)

        # store
        self._finish = 1. - finish / 100.
        self._max_distance = max_distance
        self._acquisition = acquisition

        # read catalog
        with self.open_file(catalog, 'r') as f:
            self._catalog = pd.read_csv(f, index_col=False)

        # create grid
        grid = {'alt': [], 'az': [], 'done': []}
        for az in np.linspace(0, 360 - 360 / num_az, num_az):
            for alt in np.linspace(min_alt, max_alt, num_alt):
                grid['alt'] += [alt]
                grid['az'] += [az]
                grid['done'] += [False]

        # to dataframe
        self._grid = pd.DataFrame(grid).set_index(['alt', 'az'])

    def open(self):
        """Open module."""
        PyObsModule.open(self)

    def _run_thread(self):
        # get acquisition unit
        acquisition: IAcquisition = self.proxy(self._acquisition, IAcquisition)

        # loop until finished
        while not self.closing.is_set():
            # get all entries without offset measurements
            todo = list(self._grid[~self._grid['done']].index)
            if len(todo) / len(self._grid) < self._finish:
                log.info('Finished.')
                break
            log.info('Grid points left to do: %d', len(todo))

            # try to find a good point
            while True:
                # pick a random index and remove from list
                alt, az = random.sample(todo, 1)[0]
                todo.remove((alt, az))

                # convert to ra/dec
                radec = SkyCoord(alt=alt*u.deg, az=az*u.deg, frame='altaz',
                                 obstime=Time.now(), location=self.observer.location).icrs
                ra, dec = radec.ra.radian, radec.dec.radian

                # calculate x/y/z
                x, y, z = np.cos(ra) * np.cos(ra), np.cos(dec) * np.sin(ra), np.sin(dec)

                # and distance to every star in catalog
                self._catalog['dist'] = np.sqrt((x - self._catalog['x']) ** 2 +
                                                (y - self._catalog['y']) ** 2 +
                                                (z - self._catalog['z']) ** 2)

                # sort by dist
                target = self._catalog.sort_values('dist', ascending=True).iloc[0]

                # check distance
                dist = np.degrees(target['dist'])
                if dist < self._max_distance:
                    break

                # to do list empty?
                if len(todo) == 0:
                    # could not find a grid point
                    log.info('Could not find a suitable grid point, resetting todo list for next entry...')
                    todo = list(self._grid.index)
                    continue

            # create SkyCoord from target
            radec = SkyCoord(target['ra'] * u.deg, target['dec'] * u.deg, frame='icrs')

            # log finding
            log.info('Picked star at %s, which is %.1f degrees of the grid point at Alt=%.2f, Az=%.2f.',
                     radec.to_string('hmsdms'), dist, alt, az)

            # acquire target
            try:
                acquisition.acquire_target(float(radec.ra.degree), float(radec.dec.degree))
            except ValueError:
                log.info('Could not acquire target.')
                continue

            # finished
            self._grid.loc[alt, az] = True


__all__ = ['PointingMastermind']
