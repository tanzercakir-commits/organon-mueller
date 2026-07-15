# Design Note — `addition` + `scalars` in the Term Language (Stage 7 spec input)

Source requirement: `docs/term-language-extensions.md` priority 1/1b —
bring the physics of coherent superposition (I15–I18) into the language.

## Language extension

```
t ::= Atom(name) | Mul(t, t) | Conj(t)
    | Sum(t, t)                    # NEW: term sum
    | Scale(c, t)                  # NEW: scale by an opaque scalar coefficient c
c ::= ScalarAtom(name) | ScalarConj(c)   # opaque; NO arithmetic (M10)
```

- **Hybrid boundary preserved (M10)**: the e-graph keeps the scalar OPAQUE —
  no arithmetic rule on `c` at all (addition/multiplication evaluation lives in SymPy).
  The e-graph only knows the STRUCTURAL laws.
- Interpretation: `ScalarAtom(name)` → SymPy complex symbol; at the numeric
  layer a random complex scalar (separate seed, K14 extends).

## Structural axioms (with soundness-boundary analysis — stage-02/03 lessons)

| Rule | Note |
|---|---|
| Sum commutative + associative | matrix addition ✓ sound |
| Mul distributes over Sum on both sides | ✓ sound |
| Conj(Sum(x,y)) = Sum(Conj(x),Conj(y)) | elementwise ✓ |
| Conj(Scale(c,x)) = Scale(ScalarConj(c), Conj(x)) | ✓ |
| Scale(c, x)·y = Scale(c, x·y) = x·Scale(c, y) | scalar is central ✓ |
| Scale nested: Scale(c, Scale(d, x)) = Scale(d, Scale(c, x)) | scalars commute ✓ (reordering WITHOUT FORMING their product — opacity preserved) |
| **NONE**: scalar reduction/combination (c+d, c·d) | M10: on the SymPy side |

The atom-commutation rule (I10) is unchanged; there is NO free-variable
commutation involving Sum/Scale (stage-03 soundness lesson — a general rule
would be unsound, so the derivation is left to saturation).

## Explosion management

- Initially **Sum at most once, 2 summands** (superposition pair
  aZ_a + bZ_b) — enumeration size is controlled; it opens up gradually.
- conj-normal pruning extends to Sum/Scale: Conj only at the
  atom/scalar-atom level.
- **The fingerprint switches to a scale-relative key** (the stage-03 warning
  comes due): once opaque scalars take random values, absolute 3-decimal
  rounding is insufficient; the key is produced from entries divided by the
  matrix's Frobenius norm (+ zero-matrix special case). The false-separation
  analysis is redone.

## Acceptance targets (Stage 7)

1. I15 expansion: the four-term structural form of the expansion
   (aZ_a + bZ_b)·conj(aZ_a + bZ_b) is derived by the engine; the reality of
   the cross term (conj-symmetry in the structural form) is gained.
2. I16 interference: the Scale(e, x) special case — its structural skeleton
   (SymPy verifies the scalar arithmetic).
3. The recovery campaign reruns; M22 monotonicity: the recovered set
   {I1, I10} ⊂ new set (target: + the structural half of I15; part of I16-I18).
4. All old tests green unchanged (K11 API inviolability).

## Risks

- The egglog pathology may recur on different surfaces with the new node types →
  isolated-graph mode (M18) already protects against this; the probe is extended.
- Symbolic certification cost grows with Sum (polynomial term count) —
  certify times are remeasured; if needed the "underivable-only" default is kept.
