# ASP.NET Core Test Levels

## Unit boundary

Use unit tests for domain and application behavior that does not require the ASP.NET Core host:

- Value object parsing and normalization
- Domain invariants and validation errors
- Service orchestration through a narrow port
- Deterministic mapping and filename generation
- Cancellation and retry decisions using injected collaborators

Use fakes at the port boundary. Verify the service's observable result and required call behavior, not private methods.

## Integration boundary

Use `WebApplicationFactory<Program>` and `HttpClient` for application behavior that depends on the host:

- Route and HTTP method selection
- Model binding and JSON serialization
- Validation and `ProblemDetails`
- Middleware ordering and exception mapping
- Authentication and authorization policies
- CORS and response headers
- Configuration and dependency injection
- Persistence behavior when an actual database boundary is part of the contract

Replace external dependencies through the same boundary used by production. A fake `HttpMessageHandler`, local test server, or test container is preferable to mocking the controller's service method.

## Contract boundary

Use contract tests when compatibility with a public or external HTTP schema is the risk. Verify:

- Method and route
- Required request headers and body fields
- Response status and content type
- Required response fields and error code
- Retry headers and timeout mapping
- Absence of sensitive internal details

Do not duplicate every domain validation case at this level if unit tests already prove it. Keep representative boundary cases that prove translation between HTTP and domain contracts.

## External service scenarios

At minimum, consider:

| Scenario | Observable behavior |
| --- | --- |
| Successful image response | PNG is returned with the expected media type and download metadata |
| Validation rejection before upstream call | Client receives the documented validation error and upstream is not called |
| Upstream rate limit | Client receives the mapped status and safe `Retry-After` value when available |
| Upstream timeout | Client receives the timeout contract without leaking exception details |
| Connection or malformed response | Client receives the mapped failure and no internal response body is exposed |
| Cancellation | Request cancellation stops work and does not create an unintended retry |

## Database and fixtures

When persistence is in scope, choose a test database that exercises the same query and transaction semantics that matter in production. In-memory substitutes are not sufficient for relational behavior, constraints, concurrency, or provider-specific translation.

Each test must own or isolate its data. Define cleanup for success and failure paths, and make parallel execution constraints explicit.

