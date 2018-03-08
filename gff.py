class Gff:

    # GFF format columns
    cols = (
        'seqname',
        'source',
        'feature',
        'start',
        'end',
        'score',
        'strand',
        'frame',
        'attribute'
    )

    def __init__(
        self,
        seqname = 'NA',
        source = 'NA',
        feature = 'NA',
        start = 'NA',
        end = 'NA',
        score = 'NA',
        strand = 'NA',
        frame = 'NA',
        attribute = 'NA'
    ):
        import re
        pattern = re.compile(r'\s*;\s*')
        self.seqname = seqname
        self.source = source
        self.feature = feature
        self.start = start
        self.end = end
        self.score = score
        self.strand = strand
        self.frame = frame
        self.start = self.toInt(start)
        self.end = self.toInt(end)
        self.score = self.toInt(score)
        self.frame = self.toInt(frame)
        try:
            self.attribute = dict([x.split('=') for x in re.split(pattern, attribute)])
        except ValueError:
            pass

    def __str__(self):
        try:
            attribute = ('; ').join((
                '{}={}'.format(key, value) for key, value in self.attribute.items()
            ))
        except AttributeError:
            attribute = 'NA'
        return ('\t').join((
            self.seqname,
            self.source,
            self.feature,
            str(self.start),
            str(self.end),
            str(self.score),
            self.strand,
            str(self.frame),
            attribute
            )
        )

    @staticmethod
    def toInt(string):
        try:
            return int(string)
        except ValueError:
            return string

    @staticmethod
    def read(gff_file):
        # Required libraries
        import re
        pattern = re.compile(r'\s*;\s*')
        with open(gff_file, 'r') as f:
            for line in f:
                # Skip commented lines
                if line[0] == '#':
                    continue
                cols = line.strip().split('\t')
                try:
                    seqname, source, feature, start, end, score, strand, frame, attribute = cols
                except ValueError:
                    raise
                # Try to load the attributes into a dictionary
                try:
                    attributes = dict([x.split('=') for x in re.split(pattern, cols[8])])
                except Exception as e:
                    raise
                # Convert integer columns
                try:
                    start, end, score, frame = map(int, (start, end, score, frame))
                except ValueError:
                    pass
                yield Gff(seqname, source, feature, start, end, score, strand, frame, attribute)