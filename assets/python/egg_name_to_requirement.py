def egg_name_to_requirement(name):
    name = name.strip()
    parts = name.split('-')

    # The first part may be v or v0, which would be considered a version
    # if processed in the following loop.
    name_parts = [parts[0]]
    # Pre-releases may contain a '-' and be alpha only, so we must
    # parse from the second part to find the first version-like part.
    for part in parts[1:]:
        version = PEP440Version(part)
        if isinstance(version.version[0], int):
            break
        name_parts.append(part)

    version_parts = parts[len(name_parts):]

    if not version_parts:
        return name

    name = '-'.join(name_parts)

    version = PEP440Version('-'.join(version_parts))

    # Assume that alpha, beta, pre, post & final releases
    # are in PyPi so setuptools can find it.
    if not version.is_dev:
        return name + '==' + str(version)

    # setuptools fails if a version is given with any specifier such as
    # `==`, `=~`, `>`, if the version is not in PyPi.

    # For development releases, which will not usually be PyPi,
    # setuptools will typically fail.

    # So we estimate a previous release that should exist in PyPi,
    # by decrementing the lowest final version part, and use version
    # specifier `>` so that the installed package from VCS will have a
    # version acceptable to the requirement.

    # With major and minor releases, the previous version must be guessed.
    # If the version was `2.1.0`, the previous_version will be literally
    # `2.0.*` as it assumes that a prior minor release occurred and used
    # the same versioning convention.
    previous_version = version.final._estimate_previous()

    if previous_version.is_zero:
        raise ValueError(
            'Version %s could not be decremented' % version)

    return name + '>' + str(previous_version)
