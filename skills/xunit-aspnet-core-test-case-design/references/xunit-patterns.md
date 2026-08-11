# xUnit Patterns

## Skipped scaffold shape

Create one file and class per subject. Record one primary behavior per function, and place every planning comment inside that function:

```csharp
namespace Example.Api.Tests.Images;

public sealed class PostImagesTests
{
    [Fact(Skip = "TODO: Implement from documented test plan.")]
    public void PostImages_WhenRequestIsValid_ReturnsPng()
    {
        // ID: IMAGES-01
        // Source: docs/api/images.md
        // Given: a valid image request
        // When: the client posts the request
        // Then: the API returns PNG content with the documented metadata
        // Level: ASP.NET Core integration
        // Priority: High
    }
}
```

Mark a plan as a Theory candidate inside the function when cases share the same behavior and only data varies. Keep it as a skipped Fact until data and assertions are implemented. Do not add assertions, fixtures, fakes, stubs, or production implementation during scaffolding. Keep cases with different failure reasons separate when their observable contract differs.

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

xUnit has no native `test.todo`. Use a skipped function so the runner reports the case without treating an empty body as passing:

```csharp
[Fact(Skip = "TODO: Blocked until the upstream timeout contract is defined.")]
public void PostImages_WhenUpstreamTimesOut_ReturnsGatewayTimeout()
{
    // ID: IMAGES-02
    // Source: docs/api/images.md
    // Given: the upstream request exceeds its timeout
    // When: the client posts a valid request
    // Then: the API returns the documented timeout response without internal details
    // Blocked by: define the upstream timeout contract
    // Priority: High
}
```

Skipped functions are not passing tests or coverage. Report them separately, keep the Skip reason actionable, and remove Skip only when the test has assertions and has first been observed failing for the intended reason.

## Execution

Use the repository's configured commands first. Common commands are:

```powershell
dotnet test
dotnet test path/to/Project.Tests.csproj --filter FullyQualifiedName~Images
dotnet test --list-tests
```

If coverage is configured, use the repository command and report its result. Do not invent a coverage threshold or treat a passing build as proof that unexecuted cases are covered.
