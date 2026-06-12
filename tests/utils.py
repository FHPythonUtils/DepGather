from packaging.requirements import Requirement


def assert_eq_packages(a: set[Requirement], b: set[str]) -> None:
	lhs = {x.name.upper() for x in a}
	rhs = {x.upper() for x in b}

	missing = rhs - lhs
	extra = lhs - rhs

	assert lhs == rhs, (
		f"Extra in Expected (RHS): {sorted(missing)}\nExtra in Requirements: {sorted(extra)}"
	)


def assert_not_in_packages(a: set[Requirement], b: str) -> None:
	reqs = {d.name.upper() for d in a}
	assert b.upper() not in reqs


def assert_in_packages(a: set[Requirement], b: str) -> None:
	reqs = {d.name.upper() for d in a}
	assert b.upper() in reqs
