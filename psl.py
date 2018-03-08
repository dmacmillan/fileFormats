# Information retrieved from https://uswest.ensembl.org/info/website/upload/psl.html

class Psl:

    # PSL format columns
    cols = (
        'matches',
        'misMatches',
        'repMatches',
        'nCount',
        'qNumInsert',
        'qBaseInsert',
        'tNumInsert',
        'tBaseInsert',
        'strand',
        'qName',
        'qSize',
        'qStart',
        'qEnd',
        'tName',
        'tSize',
        'tStart',
        'tEnd',
        'blockCount',
        'blockSizes',
        'qStarts',
        'tStarts'
    )

    def __init__(
        self,
        matches = 0,
        misMatches = 0,
        repMatches = 0,
        nCount = 0,
        qNumInsert = 0,
        qBaseInsert = 0,
        tNumInsert = 0,
        tBaseInsert = 0,
        strand = 'NA',
        qName = 'NA',
        qSize = 0,
        qStart = 0,
        qEnd = 0,
        tName = 'NA',
        tSize = 0,
        tStart = 0,
        tEnd = 0,
        blockCount = 0,
        blockSizes = 0,
        qStarts = 0,
        tStarts = 0
    ):
        self.matches = int(matches)
        self.misMatches = int(misMatches)
        self.repMatches = int(repMatches)
        self.nCount = int(nCount)
        self.qNumInsert = int(qNumInsert)
        self.qBaseInsert = int(qBaseInsert)
        self.tNumInsert = int(tNumInsert)
        self.tBaseInsert = int(tBaseInsert)
        self.strand = strand
        self.qName = qName
        self.qSize = int(qSize)
        self.qStart = int(qStart)
        self.qEnd = int(qEnd)
        self.tName = tName
        self.tSize = int(tSize)
        self.tStart = int(tStart)
        self.tEnd = int(tEnd)
        self.blockCount = int(blockCount)
        try:
            self.blockSizes = [int(x) for x in blockSizes.rstrip(',').split(',')]
        except AttributeError:
            self.blockSizes = [blockSizes]
        try:
            self.qStarts = [int(x) for x in qStarts.rstrip(',').split(',')]
        except AttributeError:
            self.qStarts = [qStarts]
        try:
            self.tStarts = [int(x) for x in tStarts.rstrip(',').split(',')]
        except AttributeError:
            self.tStarts = [tStarts]

    def __str__(self):
        to_write = {x:getattr(self, x) for x in self.cols}
        to_write['blockSizes'] = (',').join((str(x) for x in to_write['blockSizes'])) + ','
        to_write['qStarts'] = (',').join((str(x) for x in to_write['qStarts'])) + ','
        to_write['tStarts'] = (',').join((str(x) for x in to_write['tStarts'])) + ','
        return ('\t').join((
            str(to_write[key]) for key in self.cols
        ))

    @staticmethod
    def read(psl_file):
        with open(psl_file, 'r') as f:
            # Check to see if the PSL file has a header
            # If so skip through it
            first_line = f.readline()
            if first_line[0] not in (str(x) for x in range(10)):
                for i in range(4):
                    f.readline()
            else:
                yield Psl(*first_line.strip().split('\t'))
            for line in f:
                # print(*['"{}"'.format(x) for x in line.strip().split('\t')])
                yield Psl(*line.strip().split('\t'))