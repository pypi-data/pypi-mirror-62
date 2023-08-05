import warnings
from math import isclose
from poisson_approval.constants.constants import *
from poisson_approval.constants.EquilibriumStatus import EquilibriumStatus
from poisson_approval.containers.AnalyzedStrategies import AnalyzedStrategies
from poisson_approval.profiles.ProfileCardinal import ProfileCardinal
from poisson_approval.strategies.StrategyThreshold import StrategyThreshold
from poisson_approval.utils.DictPrintingInOrderIgnoringZeros import DictPrintingInOrderIgnoringZeros
from poisson_approval.utils.Util import product_dict, sort_weak_order, is_weak_order
from poisson_approval.utils.UtilCache import cached_property


class ProfileNoisyDiscrete(ProfileCardinal):
    """Profile with a discrete distribution of voters, with noise.

    Parameters
    ----------
    d : dict
        The first possible format is a dict that maps a tuple (ranking, utility, noise) to the share of voters who have
        this ranking, and this utility for their second candidate (up to the noise). The second possible format is a
        dict of dict that maps a ranking (first key) and a tuple (utility, noise) (second key) to the corresponding
        share of voters; it corresponds more closely to the attribute :attr:`d_ranking_utility_noise_share` mentioned
        below. Cf. examples below.
    d_weak_order_share : dict
        E.g. ``{'a~b>c': 0.2, 'a>b~c': 0.1}``. ``d_weak_order_share['a~b>c']`` is the probability that a voter likes
        candidates ``a`` and ``b`` equally and prefer them to candidate ``c``.
    normalization_warning : bool
        Whether a warning should be issued if the input distribution is not normalized.
    ratio_sincere : Number
        The ratio of sincere voters, in the interval [0, 1]. This is used for :meth:`tau`.
    ratio_fanatic : Number
        The ratio of fanatic voters, in the interval [0, 1]. This is used for :meth:`tau`. The sum of `ratio_sincere`
        and `ratio_fanatic` must not exceed 1.
    voting_rule : str
        The voting rule. Possible values are ``APPROVAL``, ``PLURALITY`` and ``ANTI_PLURALITY``.

    Attributes
    ----------
    d_ranking_utility_noise_share : dict of dict
        It maps a ranking to a dict that maps a tuple (utility, noise) to a share of voters. It means that this share
        of voters have this ranking and with a utility for their second candidate that is uniformly distributed in an
        interval [umin, umax], where umin = max(utility - noise, 0) and umax = min(utility + noise, 1).

    Notes
    -----
    If the input distribution is not normalized, the profile will be normalized anyway and a warning is
    issued (unless `normalization_warning` is False).

    Examples
    --------
    The first possible input syntax is a dict that maps a tuple (ranking, utility, noise) to a share of voters:

        >>> from fractions import Fraction
        >>> profile = ProfileNoisyDiscrete({
        ...     ('abc', 0.3, 0.01): Fraction(26, 100),
        ...     ('abc', 0.8, 0.01): Fraction(53, 100),
        ...     ('bac', 0.1, 0.01): Fraction(21, 100)
        ... })
        >>> print(profile)
        <abc 0.3 ± 0.01: 13/50, abc 0.8 ± 0.01: 53/100, bac 0.1 ± 0.01: 21/100> (Condorcet winner: a)

    The second possible input syntax is a dict that maps a ranking to a nested dict, itself mapping a tuple
    (utility, noise) to a share of voters:

        >>> from fractions import Fraction
        >>> profile = ProfileNoisyDiscrete({
        ...     'abc': {(0.3, 0.01): Fraction(26, 100), (0.8, 0.01): Fraction(53, 100)},
        ...     'bac': {(0.1, 0.01): Fraction(21, 100)}
        ... })
        >>> print(profile)
        <abc 0.3 ± 0.01: 13/50, abc 0.8 ± 0.01: 53/100, bac 0.1 ± 0.01: 21/100> (Condorcet winner: a)

    Some examples of operations on the profile:

        >>> profile
        ProfileNoisyDiscrete({'abc': {(0.3, 0.01): Fraction(13, 50), (0.8, 0.01): Fraction(53, 100)}, \
'bac': {(0.1, 0.01): Fraction(21, 100)}})
        >>> profile.d_ranking_share
        {'abc': Fraction(79, 100), 'bac': Fraction(21, 100)}
        >>> profile.abc
        Fraction(79, 100)
        >>> profile.have_ranking_with_utility_above_u('abc', 0.5)
        Fraction(53, 100)
        >>> profile.have_ranking_with_utility_below_u('abc', 0.5)
        Fraction(13, 50)
        >>> profile.have_ranking_with_utility_u('abc', 0.3)
        0

    The profile can include weak orders:

        >>> profile = ProfileNoisyDiscrete(
        ...     {('abc', 0.3, 0.01): Fraction(26, 100), ('bac', 0.1, 0.01): Fraction(21, 100)},
        ...     d_weak_order_share={'a~b>c': Fraction(53, 100)})
        >>> profile
        ProfileNoisyDiscrete({'abc': {(0.3, 0.01): Fraction(13, 50)}, 'bac': {(0.1, 0.01): Fraction(21, 100)}}, \
d_weak_order_share={'a~b>c': Fraction(53, 100)})
        >>> print(profile)
        <abc 0.3 ± 0.01: 13/50, bac 0.1 ± 0.01: 21/100, a~b>c: 53/100> (Condorcet winner: a)
    """

    def __init__(self, d, d_weak_order_share=None, normalization_warning=True, ratio_sincere=0, ratio_fanatic=0,
                 voting_rule=APPROVAL):
        """
            >>> profile = ProfileNoisyDiscrete({42: 51})
            Traceback (most recent call last):
            TypeError: Key should be tuple or str, got: <class 'int'> instead.
        """
        super().__init__(ratio_sincere=ratio_sincere, ratio_fanatic=ratio_fanatic, voting_rule=voting_rule)
        self.d_ranking_utility_noise_share = DictPrintingInOrderIgnoringZeros({
            ranking: DictPrintingInOrderIgnoringZeros() for ranking in RANKINGS})
        if d_weak_order_share is None:
            d_weak_order_share = dict()
        self._d_weak_order_share = DictPrintingInOrderIgnoringZeros({
            weak_order: 0 for weak_order in WEAK_ORDERS_WITHOUT_INVERSIONS})
        # Input d

        def add_voters(r, u, epsilon, s):
            # Ranking r, utility u, share s, noise epsilon
            if s == 0:
                return
            elif epsilon == 0:  # pragma: no cover
                raise ValueError('Noise should be > 0')
            else:
                self.d_ranking_utility_noise_share[r][(u, epsilon)] = (
                    self.d_ranking_utility_noise_share[r].get((u, epsilon), 0) + s)

        for key, value in d.items():
            if is_weak_order(key):
                self._d_weak_order_share[sort_weak_order(key)] += value
            elif isinstance(key, tuple):
                ranking, utility, noise = key
                share = value
                add_voters(ranking, utility, noise, share)
            elif isinstance(key, str):
                ranking = key
                d_utility_noise_share = value
                for (utility, noise), share in d_utility_noise_share.items():
                    add_voters(ranking, utility, noise, share)
            else:
                raise TypeError('Key should be tuple or str, got: %s instead.' % type(key))
        # Input d_weak_order_share
        for weak_order, share in d_weak_order_share.items():
            self._d_weak_order_share[sort_weak_order(weak_order)] += share
        # Normalize if necessary
        total = (sum([sum(d_utility_noise_share.values())
                      for d_utility_noise_share in self.d_ranking_utility_noise_share.values()])
                 + sum(self._d_weak_order_share.values()))
        if not isclose(total, 1.):
            if normalization_warning:
                warnings.warn("Warning: profile is not normalized, I will normalize it.")
            for d_utility_noise_share in self.d_ranking_utility_noise_share.values():
                for utility_noise, share in d_utility_noise_share.items():
                    d_utility_noise_share[utility_noise] = share / total
            for weak_order in self._d_weak_order_share.keys():
                self._d_weak_order_share[weak_order] /= total

    @cached_property
    def d_ranking_share(self):
        return DictPrintingInOrderIgnoringZeros({
            ranking: sum(d_utility_noise_share.values())
            for ranking, d_utility_noise_share in self.d_ranking_utility_noise_share.items()
        })

    @cached_property
    def d_ranking_umin_umax_share(self):
        """dict: Dictionary that maps a ranking to a dictionary that maps a tuple (u_min, u_max) to a share of voters.
        """
        return {ranking: {(max(utility - noise, 0), min(utility + noise, 1)): share
                          for (utility, noise), share in d_utility_noise_share.items()}
                for ranking, d_utility_noise_share in self.d_ranking_utility_noise_share.items()}

    @cached_property
    def d_weak_order_share(self):
        return self._d_weak_order_share

    def have_ranking_with_utility_above_u(self, ranking, u):
        d_umin_umax_share = self.d_ranking_umin_umax_share[ranking]
        return sum([
            _crop((umax - u) / (umax - umin)) * share
            for (umin, umax), share in d_umin_umax_share.items()
        ])

    def have_ranking_with_utility_u(self, ranking, u):
        return 0

    def have_ranking_with_utility_below_u(self, ranking, u):
        d_umin_umax_share = self.d_ranking_umin_umax_share[ranking]
        return sum([
            _crop((u - umin) / (umax - umin)) * share
            for (umin, umax), share in d_umin_umax_share.items()
        ])

    def __repr__(self):
        """
            >>> from fractions import Fraction
            >>> profile = ProfileNoisyDiscrete({
            ...     ('abc', 0.3, 0.01): Fraction(26, 100),
            ...     ('abc', 0.8, 0.01): Fraction(53, 100),
            ...     ('bac', 0.1, 0.01): Fraction(21, 100)
            ... }, ratio_sincere=Fraction(1, 10), ratio_fanatic=Fraction(2, 10))
            >>> profile
            ProfileNoisyDiscrete({'abc': {(0.3, 0.01): Fraction(13, 50), (0.8, 0.01): Fraction(53, 100)}, \
'bac': {(0.1, 0.01): Fraction(21, 100)}}, ratio_sincere=Fraction(1, 10), ratio_fanatic=Fraction(1, 5))
        """
        arguments = repr(self.d_ranking_utility_noise_share)
        if self.contains_weak_orders:
            arguments += ', d_weak_order_share=%r' % self.d_weak_order_share
        if self.ratio_sincere > 0:
            arguments += ', ratio_sincere=%r' % self.ratio_sincere
        if self.ratio_fanatic > 0:
            arguments += ', ratio_fanatic=%r' % self.ratio_fanatic
        if self.voting_rule != APPROVAL:
            arguments += ', voting_rule=%r' % self.voting_rule
        return 'ProfileNoisyDiscrete(%s)' % arguments

    def __str__(self):
        """
            >>> from fractions import Fraction
            >>> profile = ProfileNoisyDiscrete({
            ...     ('abc', 0.3, 0.01): Fraction(26, 100),
            ...     ('abc', 0.8, 0.01): Fraction(53, 100),
            ...     ('bac', 0.1, 0.01): Fraction(21, 100)
            ... }, ratio_sincere=Fraction(1, 10), ratio_fanatic=Fraction(2, 10))
            >>> print(profile)
            <abc 0.3 ± 0.01: 13/50, abc 0.8 ± 0.01: 53/100, bac 0.1 ± 0.01: 21/100> (Condorcet winner: a) \
(ratio_sincere: 1/10) (ratio_fanatic: 1/5)
        """
        contents = []
        if self.contains_rankings:
            contents.append(', '.join([
                '%s %s ± %s: %s' % (ranking, utility, noise,
                                    self.d_ranking_utility_noise_share[ranking][(utility, noise)])
                for ranking in sorted(self.d_ranking_utility_noise_share.keys())
                if self.d_ranking_utility_noise_share[ranking]
                for utility, noise in sorted(self.d_ranking_utility_noise_share[ranking].keys())
            ]))
        if self.contains_weak_orders:
            contents.append(str(self.d_weak_order_share)[1:-1])
        result = '<' + ', '.join(contents) + '>'
        if self.is_profile_condorcet:
            result += ' (Condorcet winner: %s)' % self.condorcet_winners
        if self.ratio_sincere > 0:
            result += ' (ratio_sincere: %s)' % self.ratio_sincere
        if self.ratio_fanatic > 0:
            result += ' (ratio_fanatic: %s)' % self.ratio_fanatic
        if self.voting_rule != APPROVAL:
            result += ' (%s)' % self.voting_rule
        return result

    def _repr_pretty_(self, p, cycle):  # pragma: no cover
        # https://stackoverflow.com/questions/41453624/tell-ipython-to-use-an-objects-str-instead-of-repr-for-output
        p.text(str(self) if not cycle else '...')

    def __eq__(self, other):
        """Equality test.

        Parameters
        ----------
        other : Object

        Returns
        -------
        bool
            True iff this profile is equal to `other`.

        Examples
        --------
            >>> from fractions import Fraction
            >>> profile = ProfileNoisyDiscrete({
            ...     ('abc', 0.3, 0.01): Fraction(26, 100),
            ...     ('abc', 0.8, 0.01): Fraction(53, 100),
            ...     ('bac', 0.1, 0.01): Fraction(21, 100)
            ... })
            >>> profile == ProfileNoisyDiscrete({
            ...     ('abc', 0.3, 0.01): Fraction(26, 100),
            ...     ('abc', 0.8, 0.01): Fraction(53, 100),
            ...     ('bac', 0.1, 0.01): Fraction(21, 100)
            ... })
            True
        """
        return (isinstance(other, ProfileNoisyDiscrete)
                and all([self.d_ranking_utility_noise_share[ranking] == other.d_ranking_utility_noise_share[ranking]
                         for ranking in RANKINGS])
                and self.d_weak_order_share == other.d_weak_order_share
                and self.ratio_sincere == other.ratio_sincere
                and self.ratio_fanatic == other.ratio_fanatic
                and self.voting_rule == other.voting_rule)

    @cached_property
    def standardized_version(self):
        """ProfileNoisyDiscrete : Standardized version of the profile (makes it unique, up to permutations of the
        candidates).

        Examples
        --------
            >>> from fractions import Fraction
            >>> profile = ProfileNoisyDiscrete({
            ...     ('abc', 0.3, 0.01): Fraction(26, 100),
            ...     ('abc', 0.8, 0.01): Fraction(53, 100),
            ...     ('bac', 0.1, 0.01): Fraction(21, 100)
            ... })
            >>> print(profile.standardized_version)
            <abc 0.3 ± 0.01: 13/50, abc 0.8 ± 0.01: 53/100, bac 0.1 ± 0.01: 21/100> (Condorcet winner: a)
            >>> profile.is_standardized
            True
        """
        def translate(s, permute):
            return s.replace('a', permute[0]).replace('b', permute[1]).replace('c', permute[2])

        best_d = {}
        best_signature = []
        for perm in XYZ_PERMUTATIONS:
            d_test = {translate(ranking, perm): d_utility_noise_share
                      for ranking, d_utility_noise_share in self.d_ranking_utility_noise_share.items()}
            d_test.update({sort_weak_order(translate(weak_order, perm)): share
                           for weak_order, share in self.d_weak_order_share.items()})
            signature_test = [[(utility, d_test[ranking][utility]) for utility in sorted(d_test[ranking].keys())]
                              for ranking in XYZ_RANKINGS]
            signature_test += [d_test[weak_order] for weak_order in XYZ_WEAK_ORDERS_WITHOUT_INVERSIONS]
            if signature_test > best_signature:
                best_signature = signature_test
                best_d = d_test
        return ProfileNoisyDiscrete(
            {ranking: best_d[xyz_ranking] for ranking, xyz_ranking in zip(RANKINGS, XYZ_RANKINGS)},
            {weak_order: best_d[xyz_weak_order] for weak_order, xyz_weak_order in zip(
                WEAK_ORDERS_WITHOUT_INVERSIONS, XYZ_WEAK_ORDERS_WITHOUT_INVERSIONS)},
            ratio_sincere=self.ratio_sincere, ratio_fanatic=self.ratio_fanatic,
            voting_rule=self.voting_rule)

    @cached_property
    def analyzed_strategies(self):
        raise NotImplementedError


def _crop(x, low=0, high=1):
    """Crop a number to an interval.

    Parameters
    ----------
    x : Number
    low : Number
    high : Number

    Returns
    -------
    Number
        `x` in the general case, but `low` if `x` is lower and `high` if `x` is higher.

    Examples
    --------
        >>> _crop(- 0.2)
        0
        >>> _crop(0.5)
        0.5
        >>> _crop(1.5)
        1
    """
    return min(max(x, low), high)
