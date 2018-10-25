from typing import List

__CLASS_TARGET__ = {
    92: 0,
    88: 1,
    42: 2,
    90: 3,
    65: 4,
    16: 5,
    67: 6,
    95: 7,
    62: 8,
    15: 9,
    52: 10,
    6: 11,
    64: 12,
    53: 13
}


class Metadata(object):
    def __init__(self, uuid: int, ra: float, decl: float, gal_l: float, gal_b: float, ddf: bool, specz: float,
                 photoz: float, photoz_err: float, distmod: float, mwebv: float, target: int) -> None:
        self.uuid = uuid
        self.ra = ra
        self.decl = decl
        self.gal_l = gal_l
        self.gal_n = gal_b
        self.ddf = ddf
        self.specz = specz
        self.photoz = photoz
        self.photoz_err = photoz_err
        self.distmod = distmod
        self.mwebv = mwebv
        self.target = target

    def __repr__(self):
        return "(uuid={}, ra={}, decl={}, gal_l={}, gal_n={}, ddf={}, specz={}, photoz={}, photoz_err={}, distmod={}, mwebv={}, target={})".format(
            self.uuid,
            self.ra,
            self.decl,
            self.gal_l,
            self.gal_n,
            self.ddf,
            self.specz,
            self.photoz,
            self.photoz_err,
            self.distmod,
            self.mwebv,
            self.target
        )


def new(uuid: int, ra: float, decl: float, gal_l: float, gal_b: float, ddf: bool, specz: float,
        photoz: float, photoz_err: float, distmod: float, mwebv: float, target: int) -> Metadata:
    return Metadata(
        uuid=uuid,
        ra=ra,
        decl=decl,
        gal_l=gal_l,
        gal_b=gal_b,
        ddf=ddf,
        specz=specz,
        photoz=photoz,
        photoz_err=photoz_err,
        distmod=distmod,
        mwebv=mwebv,
        target=target
    )


def from_line(line: List[str]) -> Metadata:
    return Metadata(
        uuid=int(line[0]),
        ra=float(line[1]),
        decl=float(line[2]),
        gal_l=float(line[3]),
        gal_b=float(line[4]),
        ddf=line[5] == '1',
        specz=float(line[6]),
        photoz=float(line[7]),
        photoz_err=float(line[8]),
        distmod=float(line[9]),
        mwebv=float(line[10]),
        target=__CLASS_TARGET__[int(line[11])]
    )
