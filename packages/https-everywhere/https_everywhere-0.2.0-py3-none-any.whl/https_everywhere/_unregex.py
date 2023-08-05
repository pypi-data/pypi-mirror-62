import sre_parse
import logging

import urllib3
from urllib3.util.url import parse_url as urlparse

import sre_yield

from logzero import setup_logger

from ._fixme import (
    _FIXME_SUBDOMAIN_PREFIXES,
    _FIXME_SUBDOMAIN_SUFFIXES,
    _FIXME_EXTRA_REPLACEMENTS,
)

logger = setup_logger(name="httpseverwhere.unregex", level=logging.INFO)
valid_host_char = set(
    "ABCDEFGHIJKMLNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz09123456789.-*"
)


class ExpansionError(ValueError):
    pass


class TooManyExpansions(ExpansionError):
    pass


class NonsenseExpansions(ExpansionError):
    pass


def remove_subdomain_prefix(pattern):
    unregex = pattern
    for prefix in _FIXME_SUBDOMAIN_PREFIXES:
        unregex = unregex.replace(prefix, "*.")

    for suffix in _FIXME_SUBDOMAIN_SUFFIXES:
        unregex = unregex.replace(suffix, ".*")

    return unregex


def expand_pattern(pattern, max_count=100):
    if not pattern.startswith("^http://"):
        pattern = "^http://" + pattern
    pattern = pattern[8:]
    pattern_without_subdomain_prefix = remove_subdomain_prefix(pattern)
    if pattern_without_subdomain_prefix != pattern:
        if not (set(pattern_without_subdomain_prefix) & set(r"?|+{}()")):
            s = pattern_without_subdomain_prefix.replace(r"\.", ".")
            try:
                p = urlparse(s)
                if (
                    not p.host
                    or set(p.host) | valid_host_char != valid_host_char
                    or ".." in p.host
                    or "**" in p.host
                ):  # pragma: no cover
                    raise RuntimeError(
                        "urlparse includes junk in host in {}: {!r}".format(
                            s, sorted(set(p.host) - valid_host_char)
                        )
                    )
                else:
                    return [p.host]
            except urllib3.exceptions.LocationParseError:  # pragma: no cover
                # TODO: build test case for this
                pass

        pattern = pattern_without_subdomain_prefix.replace("*.", "~~").replace(
            ".*", ",,"
        )

    for match, replacement in _FIXME_EXTRA_REPLACEMENTS:
        pattern = pattern.replace(match, replacement)

    pattern = pattern.replace("*", "").rstrip("./").replace(r"\d+", r"\d\d")

    # https://github.com/google/sre_yield/issues/6
    pos = pattern.find("(?!")
    if pos == 0:
        pos = pattern.find(")")
        if pos == -1:  # pragma: no cover
            raise RuntimeError("couldnt find end of assertion in {}".format(pattern))
        pattern = pattern[pos + 1 :]

    c = sre_parse.parse(pattern)

    c = split_regex(c, "/")[0]

    rv = sre_yield.AllStrings(c, max_count=10, relaxed=True)[: max_count + 1]

    # https://github.com/google/sre_yield/issues/16
    assert rv.__len__() <= max_count + 1, (rv.__len__(), max_count, pattern, c)
    rv = list(rv)
    assert rv.__len__() <= max_count + 1, (pattern, max_count)

    if not rv:  # pragma: no cover
        raise RuntimeError("{} has no results".format(pattern))

    for count, i in enumerate(rv):
        assert count <= max_count + 1, (pattern, max_count)
        if not i:  # pragma: no cover
            raise RuntimeError("{} has no useful results".format(pattern))
        if "." not in i:
            logger.info("{} has invalid domain expansions: {}".format(pattern, rv))
            raise NonsenseExpansions(
                "{} produced nonsense at pos {}: {}".format(pattern, count, i)
            )

    # https://github.com/google/sre_yield/issues/16
    if rv.__len__() > max_count:
        logger.info("{} has too many results: {}".format(pattern, rv))
        raise TooManyExpansions(
            "{} has too many (> {}) results: {} ".format(pattern, max_count, rv)
        )
    return [i.replace("~~", "*.").replace("~", "*").replace(",,", ".*") for i in rv]


def split_regex(pattern, at):
    if not isinstance(pattern, sre_parse.SubPattern):
        pattern = sre_parse.parse(pattern)
    found = False
    new = sre_parse.SubPattern(pattern.pattern)
    for i, (tok, val) in enumerate(pattern.data.copy()):
        if not found and tok == sre_parse.LITERAL and val == ord(at):
            found = True
            del pattern[i]
            continue
        elif not found and tok == sre_parse.IN and (sre_parse.LITERAL, ord(at)) in val:
            found = True
            del pattern[i]
            continue
        elif not found and tok == sre_parse.MAX_REPEAT:
            val = val[2]
            if (sre_parse.LITERAL, ord(at)) in val:
                found = True
                del pattern[i]
                continue
        if found:
            new.append((tok, val))
            del pattern[-1]
    if not found:
        return pattern, None
    return pattern, new
