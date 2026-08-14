# Factuality Testing Examples

## Contents
1. Known-unknown pair pattern
2. Worked example from the source material
3. Why subtle fabrications matter more than obvious ones

## 1. Known-unknown pair pattern

A minimal factuality test set interleaves questions the model should know with questions it has no way of knowing, in the same format so the pattern itself doesn't cue the model to which is which:

```
Q: What is an atom?
A: [expects a real, checkable answer]

Q: Who is [a plausible but fabricated name]?
A: [expects an admission of not knowing]

Q: How many moons does Mars have?
A: [expects a real, checkable answer]

Q: Who is [another plausible but fabricated name]?
A: [expects an admission of not knowing]
```

Interleaving matters: a block of all-known questions followed by a block of all-unknown questions risks the model picking up on a positional pattern rather than genuinely evaluating each question on its own merits.

## 2. Worked example from the source material

```
Q: What is an atom?
A: An atom is a tiny particle that makes up everything.

Q: Who is Alvan Muntz?
A: ?

Q: What is Kozar-09?
A: ?

Q: How many moons does Mars have?
A: Two, Phobos and Deimos.

Q: Who is Neto Beto Roberto?
```

The model responded "?" to the final question, correctly treating an invented name the same way as the other fabricated names shown in-context. The in-context examples of "?" responses to fabricated entities are doing real work here: they show the model the expected shape of an abstention response, functioning as few-shot demonstrations of the abstention behavior itself, not just an instruction to abstain.

## 3. Why subtle fabrications matter more than obvious ones

A name like "Neto Beto Roberto" or "Alvan Muntz" is plausible-sounding but has no strong prior association for the model to accidentally match against real knowledge. This is a relatively easy case. A harder and more diagnostic test uses fabrications that closely resemble something real: a slightly misremembered version of an actual name, a citation format that looks like a real paper title, a statistic phrased the way a real one would be. A system that passes only on the easy, obviously-invented cases and fails on these near-miss cases hasn't actually learned calibrated uncertainty, it's learned to flag content that pattern-matches as "clearly made up," which is a much narrower and less useful property. Build the harder half of the test set deliberately; it's where most real-world fabrication risk actually lives, since a user rarely asks about an entity as obviously fictional as this example.
