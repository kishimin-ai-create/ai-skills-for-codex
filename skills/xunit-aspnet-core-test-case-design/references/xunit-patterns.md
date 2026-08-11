# xUnit Patterns

## Comment-only test shape

Record one primary behavior per planned test. Keep names explicit and stable. When writing to a test file, add comments only:

```csharp
// TODO(test): PostImages_WhenRequestIsValid_ReturnsPng
// Given: a valid image request
// When: the client posts the request
// Then: the API returns PNG content with the documented metadata
// Level: ASP.NET Core integration
// Priority: High
```

Mark a plan as a Theory candidate in its comments when the cases share the same behavior and only data varies. Do not write attributes, data providers, methods, or assertions. Keep cases with different failure reasons separate when their observable contract differs.

## Assertions

- Assert the public result: return value, exception contract, HTTP response, persisted state, emitted message, or external side effect.
- For collections, assert the relevant membership, count, or ordering contract rather than incidental implementation details.
- For JSON, parse the document and assert required fields; do not compare formatted JSON strings unless formatting is itself a contract.
- For exceptions, assert the documented exception type and meaningful data. Do not use exceptions for expected domain validation when the design specifies a Result/error value.

## Fixtures and isolation

- Use `IClassFixture<T>` for expensive, read-only setup only when state is safe to share.
- Use `ICollectionFixture<T>` only when an explicit collection-level resource is required; document the serialization and cleanup behavior.
- Keep mutable state per test. Dispose `HttpClient`, temporary files, database scopes, and test servers according to their owner.
- Do not introduce global static state or shared random data to make tests pass.

## Incomplete cases

xUnit has no native `test.todo`. Use comment-only placeholders:

```csharp
// TODO(test): PostImages_WhenUpstreamTimesOut_ReturnsGatewayTimeout
// Blocked by: define the upstream timeout contract
// Expected: return the documented timeout response without internal details
// Priority: High
```

Comments are neither executable nor skipped tests. Report every comment-only placeholder as unimplemented and uncovered. Never convert it into test code unless a later user request explicitly replaces the comment-only constraint.

## Execution

Use the repository's configured commands first. Common commands are:

```powershell
dotnet test
dotnet test path/to/Project.Tests.csproj --filter FullyQualifiedName~Images
dotnet test --list-tests
```

If coverage is configured, use the repository command and report its result. Do not invent a coverage threshold or treat a passing build as proof that unexecuted cases are covered.
