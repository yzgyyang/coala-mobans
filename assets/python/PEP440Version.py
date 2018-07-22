from distutils.version import LooseVersion  # noqa (late-import)


class PEP440Version(LooseVersion):
    """
    Basic PEP440 version with a few features.

    Uses the same version semantics as LooseVersion,
    with the addition that a ``v`` prefix is allowed
    in the version as required by PEP 440.

    vstring may be a list, tuple or string.

    v_prefix indicates whether output of the version
    should include a v prefix.

    v_prefix is auto-detected by default.
    Set to False to remove if present, or True to add if missing.
    """

    def __init__(self, vstring=None, v_prefix=None):
        self._v_prefix = v_prefix

        if isinstance(vstring, (list, tuple)):
            type_ = type(vstring)
            vstring = '.'.join(str(i) for i in vstring)
        else:
            type_ = list

        vstring = vstring.strip()

        if vstring.startswith('v'):
            vstring = vstring[1:]
            if vstring.startswith('!'):
                raise ValueError('Invalid use of epoch')
            if v_prefix is not False:
                self._v_prefix = True

        # Can not use super(..) on Python 2.7
        LooseVersion.__init__(self, vstring)
        if self._v_prefix:
            self.vstring = 'v' + self.vstring
        if len(self.version) > 1 and self.version[1] == '!':
            self._epoch = self.version[0]
            if not isinstance(self._epoch, int) or len(self.version) < 3:
                raise ValueError('Invalid use of epoch')

        # Normalise to lower case
        self.version = [
            x if isinstance(x, int) else x.lower() for x in self.version
            if x not in ('-', '_')]

        if self.version[-1] != '*' and not isinstance(self.version[-1], int):
            self.version += (0, )

        if type_ is tuple:
            self.version = tuple(self.version)

        self._final = None
        self._previous = None

    def __repr__(self):
        return "%s('%s')" % (self.__class__.__name__, str(self))

    @property
    def is_dev(self):
        return any(part == 'dev' for part in self.version)

    @property
    def has_epoch(self):
        return any(part == '!' for part in self.version)

    @property
    def final(self):
        """
        Provide only the final component of the version.

        A new instance is return if this instance is not final.
        """
        if self.has_epoch:
            raise NotImplementedError

        if self._final is not None:
            return self._final

        for i, part in enumerate(self.version):
            if not isinstance(part, int):
                final = self.version[:i]
                break
        else:
            self._final = self
            return self

        self._final = PEP440Version(final, self._v_prefix)

        return self._final

    @property
    def is_final(self):
        return self.final == self

    @property
    def is_zero(self):
        return all(part == 0 for part in self.version)

    _zero_message = 'version prior to 0.0 can not exist'

    def _estimate_previous(self):
        """
        Return a new version calculated to be the previous version.

        Currently only handles when the current instance is a final version.

        To really get the previous for 1.0.0, we need to consult PyPi,
        git tags, or some other source of all released versions,
        to find the highest patch release in the prior minor release, or
        highest minor releases if there were no patch releases in the
        last minor release, etc.

        As a result, currently this assumes that release x.(x-1).0 exists
        in that instance.
        """
        if self._previous:
            return self._previous

        assert self.is_final, '%r is not final' % self

        if self.is_zero:
            raise ValueError(self._zero_message)

        previous = self._decrement(self.version)
        self._previous = PEP440Version(previous, self._v_prefix)
        return self._previous

    @staticmethod
    def _decrement(version):
        pos = len(version) - 1

        # Look for non-zero int part
        while pos != 0 and not (isinstance(version[pos], int) and version[pos]):
            pos -= 1

        previous = []
        if pos:
            previous = version[:pos]

        previous += (version[pos] - 1, )

        if len(previous) == len(version):
            return previous

        remaining = version[pos + 1:-1]

        previous += tuple(
            0 if isinstance(i, int) else i for i in remaining)

        previous += ('*', )

        return previous
