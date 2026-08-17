---
name: dotnet-result-contracts
description: Design, implement, fix, or review .NET success/failure Result types and record payloads containing arrays. Use when public factories must preserve variant invariants, nullable annotations may not prevent invalid runtime states, or byte-array payloads require value equality and stable hashing.
---

# .NET Result Contracts

Keep Result variants valid at creation time and make payload equality match the value represented by the type.

## Workflow

1. Identify every public constructor, factory, conversion, and serializer path that can create the Result or payload.
2. Write the variant truth table before changing code:

   | Variant | Success value | Error value |
   | --- | --- | --- |
   | Success | required | absent |
   | Failure | absent | required |

3. Add a failing test for one observable invalid creation path.
4. Reject missing required values at the public creation boundary. Do not rely only on nullable reference type warnings.
5. Add a failing equality test when a record contains an array and represents the array contents rather than its identity.
6. Implement content equality and verify the equality/hash contract.
7. Run focused tests, the complete relevant suite, build, and configured coverage checks.

## Result Variant Rules

- Make invalid combinations unrepresentable through public factories.
- Validate the required value in each factory before constructing the Result.
- Derive `IsSuccess` only after all creation paths guarantee the corresponding value combination.
- Test public behavior such as `Success(null!)` and `Failure(null!)`; do not use reflection to prove absent creation paths.
- Prefer separate success and failure factories when they make the invariant explicit.

## Array Payload Rules

- Confirm whether the type represents an array instance or the sequence stored in it.
- For binary value payloads, compare bytes by sequence; default record equality compares arrays by reference.
- Ensure equal values return equal hash codes.
- Do not include mutable array contents in a hash code that must remain stable after construction.
- Record the tradeoff: excluding bytes reduces hash distribution, while sequence equality costs time proportional to the compared content.
- Consider an immutable payload type separately when mutation itself must be prevented; do not claim content equality makes an array immutable.

## Review Checklist

- Can a public path create success without data?
- Can a public path create failure without an error?
- Can a failure factory accidentally produce `IsSuccess == true`?
- Do separately allocated arrays with identical contents compare as intended?
- Does mutation change the hash code after insertion into a hash-based collection?
- Do regression tests fail before the fix and pass afterward?
- Are nullability, equality, hashing, performance, and mutability effects reported separately?

## Output

Report the invariant table, reproduced invalid state, root cause, changed public contract, regression tests, verification commands and results, equality/hash tradeoffs, and unresolved mutability risks.
