"""Restricted srepr parser — the STAGE-2 GATE hardening (stage 17).

External input must NEVER reach raw `sympy.sympify`: sympify goes through
Python `eval` in every mode, and constrained `global_dict`s have
historically been escapable via attribute-access chains reachable from
string payloads. The security boundary here is therefore "never enter
eval at all": the srepr text is parsed with `ast.parse` and rebuilt into
SymPy objects by an explicit WHITELIST walk — unknown node types, call
names, keyword arguments, oversized inputs and over-deep trees are all
rejected with `UnsafeExpressionError` (K26: no silent rejection either).

Accepted grammar (sufficient for this library's serialized objects):
    Symbol('name'[, real=True, ...])   name ~ ^[A-Za-z][A-Za-z0-9_]{0,63}$
    Integer(n) | Float('...'[, precision=int]) | Rational(p, q)
    Add(...) | Mul(...) | Pow(a, b) | conjugate(x) | I | -x
"""
from __future__ import annotations

import ast
import math
import re

import sympy as sp

_math_isfinite = math.isfinite

__all__ = ["UnsafeExpressionError", "safe_parse_srepr"]

_MAX_TEXT = 65536
_MAX_NODES = 2000
_MAX_DEPTH = 64
_MAX_DIGITS = 4096

_NAME_RE = re.compile(r"[A-Za-z][A-Za-z0-9_]{0,63}")  # used with fullmatch

_MAX_EXP = 6              # reject Pow exponents / sci-notation beyond this
_MAX_MANTISSA = 4096      # Float mantissa string length

_ALLOWED_ASSUMPTIONS = frozenset(
    {"real", "positive", "negative", "complex", "imaginary", "integer"})

_CALLS = {
    "Symbol": sp.Symbol,
    "Integer": sp.Integer,
    "Float": sp.Float,
    "Rational": sp.Rational,
    "Add": sp.Add,
    "Mul": sp.Mul,
    "Pow": sp.Pow,
    "conjugate": sp.conjugate,
}

_BARE_NAMES = {"I": sp.I}


class UnsafeExpressionError(ValueError):
    """Input rejected by the restricted parser (reason in the message)."""


def _reject(reason: str):
    raise UnsafeExpressionError(f"rejected: {reason}")


_MAX_BITS = _MAX_DIGITS * 4        # ~ _MAX_DIGITS decimal digits of bits


def _check_numeric_string(s: str, kind: str) -> None:
    """Bound the encoded MAGNITUDE, not the text length (review round 2).

    Scientific notation is ALLOWED (srepr emits it for small Floats,
    e.g. Float('1.0e-10')) but the EXPONENT magnitude is capped, so a
    '1e9999999' bomb is refused while '1e-10' passes; the mantissa /
    plain-digit length is capped too."""
    body = s.strip().lower().lstrip("+-")
    if "e" in body:
        mant, _, exp = body.partition("e")
        if len(mant.replace(".", "").replace("/", "")) > _MAX_DIGITS:
            _reject(f"{kind} mantissa exceeds {_MAX_DIGITS} digits")
        try:
            exp_val = int(exp)
        except ValueError:
            _reject(f"{kind} has a malformed exponent")
        # cap the exponent at the DIGIT budget (review S1): sp.Float
        # materializes an internal integer ~ proportional to the decimal
        # exponent, so 1e300000 would burn seconds BEFORE any post-build
        # guard. Legit small Floats (1e-300) have |exp| well under this.
        if abs(exp_val) > _MAX_DIGITS:
            _reject(f"{kind} exponent magnitude exceeds {_MAX_DIGITS}")
    elif len(body.replace(".", "").replace("/", "")) > _MAX_DIGITS:
        _reject(f"{kind} literal exceeds {_MAX_DIGITS} digits")


def _check_number_size(value) -> None:
    if isinstance(value, int) and value.bit_length() > _MAX_BITS:
        _reject(f"integer magnitude exceeds {_MAX_BITS} bits")


def _int_bits(v) -> int:
    if isinstance(v, sp.Integer):
        return int(v).bit_length()
    if isinstance(v, sp.Rational):
        return max(int(v.p).bit_length(), int(v.q).bit_length())
    return 0


def _numeric_bits_in(expr) -> int:
    """Largest bit-length among the numeric atoms of `expr` (Integer /
    Rational); >= 1 if any Float atom is present. Used to project the
    cost of raising `expr` to a power BEFORE materializing (review round
    4: a numeric coefficient nested inside a Mul base, e.g. 3*x, still
    materializes 3^exp)."""
    bits = 0
    if isinstance(expr, sp.Basic):
        for a in expr.atoms(sp.Integer, sp.Rational):
            bits = max(bits, _int_bits(a))
        if expr.atoms(sp.Float):
            bits = max(bits, 1)
    return bits


def _reject_if_huge(value, kind: str) -> None:
    """Final magnitude guard on a built result — inspects EVERY numeric
    atom (not just a top-level Integer/Rational), catching products/sums
    that embed an oversized coefficient."""
    if isinstance(value, sp.Basic):
        for a in value.atoms(sp.Integer, sp.Rational):
            if _int_bits(a) > _MAX_BITS:
                _reject(f"{kind} result holds a numeric atom exceeding "
                        f"{_MAX_BITS} bits")


def _build(node: ast.AST, depth: int):
    if depth > _MAX_DEPTH:
        _reject(f"expression deeper than {_MAX_DEPTH}")

    if isinstance(node, ast.Expression):
        return _build(node.body, depth + 1)

    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool) or node.value is None:
            _reject(f"bare constant {node.value!r} outside keyword position")
        if isinstance(node.value, (int, float, str)):
            if isinstance(node.value, float) and not _math_isfinite(node.value):
                _reject("non-finite float constant")   # review D4: 1e999
            _check_number_size(node.value)
            return node.value
        _reject(f"constant type {type(node.value).__name__}")

    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        inner = _build(node.operand, depth + 1)
        if isinstance(inner, (int, float)):
            return -inner
        if isinstance(inner, sp.Basic):
            return -inner
        _reject("unary minus on non-numeric")

    if isinstance(node, ast.Name):
        if node.id in _BARE_NAMES:
            return _BARE_NAMES[node.id]
        _reject(f"name {node.id!r} not in the whitelist")

    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            _reject("only plain-name calls are allowed (no attributes)")
        fname = node.func.id
        if fname not in _CALLS:
            _reject(f"call {fname!r} not in the whitelist")
        args = [_build(a, depth + 1) for a in node.args]
        kwargs = {}
        for kw in node.keywords:
            if kw.arg is None:
                _reject("**kwargs expansion not allowed")
            if fname == "Symbol":
                if kw.arg not in _ALLOWED_ASSUMPTIONS:
                    _reject(f"Symbol assumption {kw.arg!r} not allowed")
                if not (isinstance(kw.value, ast.Constant)
                        and isinstance(kw.value.value, bool)):
                    _reject(f"assumption {kw.arg!r} must be a bool literal")
                kwargs[kw.arg] = kw.value.value
            elif fname == "Float" and kw.arg == "precision":
                if not (isinstance(kw.value, ast.Constant)
                        and isinstance(kw.value.value, int)
                        and 1 <= kw.value.value <= 4096):
                    _reject("Float precision must be an int in [1, 4096]")
                kwargs[kw.arg] = kw.value.value
            else:
                _reject(f"keyword {kw.arg!r} not allowed for {fname}")
        if fname == "Symbol":
            if not (len(args) == 1 and isinstance(args[0], str)
                    and _NAME_RE.fullmatch(args[0])):  # fullmatch: no \n (D5)
                _reject("Symbol needs one name fully matching "
                        "[A-Za-z][A-Za-z0-9_]{0,63}")
        if fname in ("Integer", "Rational", "Float"):
            for a in args:                             # magnitude guard (D1)
                if isinstance(a, str):
                    _check_numeric_string(a, fname)
                elif isinstance(a, int):
                    _check_number_size(a)
        if fname == "Pow" and len(args) == 2:
            # PROJECT the result size BEFORE materializing (review rounds
            # 2-4). Handle EVERY exponent type, not just Integer:
            base, exp = args
            if isinstance(exp, sp.Float):
                # base**Float = exp(Float*log base) -> mpmath materializes
                # 10^(10^k); the library never emits Float exponents.
                _reject("Pow with a Float exponent is not permitted")
            mag = None
            if isinstance(exp, sp.Integer):
                mag = abs(int(exp))
            elif isinstance(exp, sp.Rational):
                mag = abs(int(exp.p)) // max(int(exp.q), 1) + 1
            if mag is not None:
                if mag > 10 ** _MAX_EXP:
                    _reject(f"Pow exponent magnitude exceeds 10^{_MAX_EXP}")
                # numeric bits ANYWHERE in the base (incl. a coefficient
                # nested in a Mul base like 3*x)
                nb = _numeric_bits_in(base)
                if nb and nb * mag > _MAX_BITS:
                    _reject("Pow would materialize a value exceeding "
                            f"{_MAX_BITS} bits")
        if fname in ("Mul", "Add"):
            # PROJECT before folding (review S2): a Mul folds all args into
            # one integer BEFORE any post-build guard; sum the per-arg bit
            # budgets (upper bound for both product and sum) and refuse
            # early so the huge number is never materialized.
            total = sum(_int_bits(a) for a in args)
            if total > _MAX_BITS:
                _reject(f"{fname} of rational terms would exceed "
                        f"{_MAX_BITS} bits")
        try:
            value = _CALLS[fname](*args, **kwargs)
        except UnsafeExpressionError:
            raise
        except Exception as exc:   # constructor rejected the values
            _reject(f"{fname} constructor error: {exc}")
        # non-finite passthrough guard (review D4): NaN/oo/zoo never valid
        if isinstance(value, sp.Basic):
            if value in (sp.oo, -sp.oo, sp.zoo, sp.nan) or value.is_finite is False:
                _reject(f"{fname} produced a non-finite value")
        _reject_if_huge(value, fname)
        return value

    _reject(f"AST node {type(node).__name__} not allowed")


def safe_parse_srepr(text: str) -> sp.Basic:
    """Parse an srepr string into a SymPy expression WITHOUT eval/sympify.

    Raises UnsafeExpressionError with the reason for any input outside
    the restricted grammar."""
    if not isinstance(text, str):
        _reject(f"input must be str, got {type(text).__name__}")
    if len(text) > _MAX_TEXT:
        _reject(f"input longer than {_MAX_TEXT} characters")
    try:
        tree = ast.parse(text.strip(), mode="eval")
    except (SyntaxError, ValueError, RecursionError, MemoryError) as exc:
        # MemoryError: deep-nesting can blow ast.parse before the
        # post-parse guards fire (review D2) -> still a reasoned reject
        _reject(f"not a parseable expression: {type(exc).__name__}")
    n_nodes = sum(1 for _ in ast.walk(tree))
    if n_nodes > _MAX_NODES:
        _reject(f"more than {_MAX_NODES} AST nodes")
    result = _build(tree, 0)
    if isinstance(result, (int, float)):
        if isinstance(result, float) and not _math_isfinite(result):
            _reject("non-finite top-level number")   # review D4 (belt+braces)
        return sp.sympify(result)   # plain PYTHON number, not a string
    if not isinstance(result, sp.Basic):
        _reject(f"top-level value {type(result).__name__} is not an "
                "expression")
    if result in (sp.oo, -sp.oo, sp.zoo, sp.nan) or result.is_finite is False:
        _reject("non-finite top-level expression")
    return result
