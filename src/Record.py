from typing import List


class Record(object):
    def __init__(self, id: int, mjd: int, passband: int, flux: float, flux_err: float, detected: bool) -> None:
        self.id = id
        self.mjd = mjd
        self.passband = passband
        self.flux = flux
        self.flux_err = flux_err
        self.detected = detected

    def __repr__(self):
        return "(id={}, mjd={}, passband={}, flux={}, flux_err={}, detected={})".format(self.id, self.mjd,
                                                                                        self.passband, self.flux,
                                                                                        self.flux_err, self.detected)


def new(id: int, mjd: int, passband: int, flux: float, flux_err: float, detected: bool) -> Record:
    return Record(
        id=id,
        mjd=mjd,
        passband=passband,
        flux=flux,
        flux_err=flux_err,
        detected=detected
    )


def from_line(line: List[str]) -> Record:
    return Record(
        id=int(line[0]),
        mjd=int(float(line[1])),
        passband=int(line[2]),
        flux=float(line[3]),
        flux_err=float(line[4]),
        detected=line[5] == '1'
    )
