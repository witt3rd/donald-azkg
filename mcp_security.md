---
tags: [mcp, protocol, security, authentication, authorization, privacy]
last_refresh: 2025-10-12
---
# MCP Security

Comprehensive security framework for MCP emphasizing user consent, least privilege, and transparent data handling.

## Security Philosophy

MCP implements a comprehensive security model that emphasizes **user consent and control** throughout all interactions[2]. The protocol requires explicit user consent before any data access or tool execution occurs, ensuring that users maintain full awareness and control over AI actions[2].

### Core Security Principles

**1. User Consent First**
- Explicit approval required for all operations
- Users see what data will be accessed
- Users approve tool executions before they occur
- No silent data transmission[2]

**2. Transparency**
- Clear disclosure of data access patterns
- Visible tool parameters and effects
- Audit trails for all operations
- No hidden behaviors

**3. Least Privilege**
- Minimal necessary permissions
- Scoped server access
- Granular authorization controls
- Defense in depth[3]

**4. Data Privacy**
- User data never shared without consent
- No unauthorized transmission
- Privacy-preserving designs
- Clear data handling policies[2]

## Authentication Mechanisms

MCP supports multiple authentication methods to accommodate different deployment scenarios and security requirements[6][15].

### API Key Authentication

**Use case:** Simple authentication for trusted environments

**Implementation:**
```json
{
  "mcpServers": {
    "my-server": {
      "command": "mcp-server",
      "env": {
        "API_KEY": "your-api-key-here"
      }
    }
  }
}
```

**Best practices:**
- Store API keys in environment variables
- Never commit keys to source control
- Rotate keys regularly
- Use different keys per environment

### OAuth Flows

**Use case:** Third-party service integration with delegated access

**MCP servers are classified as OAuth Resource Servers** (2025 update), enabling robust authorization discovery where each server advertises its own authorization server[2].

**Authorization is optional but strongly recommended when:**
- Server accesses user-specific data (emails, documents, databases)
- Need to audit who performed which actions
- Server grants access to APIs requiring user consent
- Building for enterprise environments with strict access controls
- Implementing rate limiting or usage tracking per user

**Transport-specific considerations:**
- **STDIO transport:** Can use environment-based credentials or third-party library credentials directly embedded in the server (runs locally with flexible credential acquisition options)
- **HTTP transport:** OAuth flows designed for remotely-hosted servers where client uses OAuth to establish user authorization

**Supported flows:**
- Authorization Code flow with PKCE (most secure, follows OAuth 2.1)
- Client Credentials flow (service-to-service)
- Device Code flow (limited input devices)

**Benefits:**
- User controls permissions
- Time-limited access tokens
- Revocable access
- Standard protocol

**Critical 2025 Requirements:**
- **Resource Indicators (RFC 8707):** MCP clients MUST use Resource Indicators to specify the intended server ("audience") during token requests. This prevents token mis-redemption and limits token scope to specific servers[2].
- **Audience-scoped tokens:** Generic bearer tokens across multiple servers are now deprecated and considered insecure. Each token must be tightly bound to its destination server[2].

**Implementation considerations:**
- Handle token refresh
- Store tokens securely
- Clear tokens on logout
- Validate token scopes
- Implement Resource Indicators in all token requests
- Never reuse tokens across different MCP servers

### Environment Variable Credentials

**Use case:** Local development and system service authentication

**Example configuration:**
```json
{
  "mcpServers": {
    "database-server": {
      "command": "mcp-db-server",
      "env": {
        "DB_HOST": "${DB_HOST}",
        "DB_USER": "${DB_USER}",
        "DB_PASSWORD": "${DB_PASSWORD}"
      }
    }
  }
}
```

**Security considerations:**
- Use system environment variables
- Never log credential values
- Restrict environment variable access
- Consider using secret management services

### Enterprise Authentication

**Use case:** Enterprise deployments with existing identity infrastructure

**Critical Note:** MCP has no native authentication or authorization guardrails by default. Authentication, authorization, audit logging, and sandboxing must be implemented by deployers[1][4][6].

**Supported methods:**
- SAML integration
- Active Directory/LDAP
- SSO providers
- OAuth Resource Server integration (required 2025 standard)[2]
- Custom authentication connectors[15]
- OpenID Connect (OIDC) Discovery
- OAuth 2.0 Authorization Server Metadata (RFC 8414)

**Integration points:**
- Microsoft Copilot Studio connector framework[15]
- Custom authentication handlers
- Identity provider integration
- Role-based access control
- Dynamic Client Registration (DCR) support

**2025 Enterprise Requirements:**
- **Mandatory authentication:** Unauthenticated MCP server access now considered critical misconfiguration[1][2]
- **Policy controls:** Endpoint agents with allow/block policies to monitor and vet MCP servers[4]
- **Runtime enforcement:** Automated policy checks before allowing model→MCP access[4]
- **Protected Resource Metadata (PRM):** Servers must respond with 401 Unauthorized and WWW-Authenticate header containing `resource_metadata` parameter pointing to OAuth Protected Resource Metadata document (RFC 9728)

## Authorization Model

### Authorization Flow Overview

**Standard OAuth 2.1 flow with MCP extensions:**

1. **Initial Handshake:** Server responds with `401 Unauthorized` and `WWW-Authenticate` header containing Protected Resource Metadata URI
2. **Protected Resource Metadata Discovery:** Client fetches PRM document (RFC 9728) to learn authorization server, supported scopes, and resource information
3. **Authorization Server Discovery:** Client fetches authorization server metadata via OIDC Discovery or OAuth 2.0 Metadata endpoints
4. **Client Registration:** Either pre-registered credentials or Dynamic Client Registration (DCR) via RFC 7591
5. **User Authorization:** Authorization Code flow with PKCE where user grants permissions in browser
6. **Token Exchange:** Client exchanges authorization code for access token and refresh token
7. **Authenticated Requests:** Client includes access token in `Authorization: Bearer` header

**Protected Resource Metadata document example:**
```json
{
  "resource": "https://your-server.com/mcp",
  "authorization_servers": ["https://auth.your-server.com"],
  "scopes_supported": ["mcp:tools", "mcp:resources"]
}
```

**Authorization Server Metadata example:**
```json
{
  "issuer": "https://auth.your-server.com",
  "authorization_endpoint": "https://auth.your-server.com/authorize",
  "token_endpoint": "https://auth.your-server.com/token",
  "registration_endpoint": "https://auth.your-server.com/register"
}
```

### User-Based Authorization

**Host-level control:**
- User explicitly authorizes server connections
- User approves resource access requests
- User consents to tool executions
- User can revoke access at any time[2]

**Implementation:**
```text
User Request → Host → Consent Dialog → User Approval → Server Execution
```

### Server-Level Authorization

**Scope limitation:**
Each server should have limited scope[3]:
- Access only necessary resources
- Expose only required tools
- No cross-server permissions
- Minimal blast radius

**Example scoped servers:**
```text
file-server → Only access ~/Documents folder
email-server → Only send email, no inbox access
db-server → Only read from specific tables
```

### Resource-Level Authorization

**Granular permissions:**
- Individual resource access control
- User-specific resource filtering
- Dynamic permission evaluation
- Context-aware authorization

**Example:**
```json
{
  "resource": "db://customers/records",
  "permissions": {
    "read": ["user:john@example.com", "role:sales"],
    "filter": "region = user.region"
  }
}
```

### Tool-Level Authorization

**Execution control:**
- Per-tool permission requirements
- Parameter validation and sanitization
- Side effect disclosure
- Approval workflows for dangerous operations

**Example dangerous tools:**
```text
delete_database_record → Require explicit confirmation
send_mass_email → Show recipient count, require approval
execute_system_command → Restricted or disabled by default
```

## Data Privacy and Protection

### User Consent Requirements

**Before accessing user data:**
1. **Disclose what data** will be accessed
2. **Explain why** data access is needed
3. **Show where** data will be sent
4. **Obtain explicit approval** from user
5. **Log consent** for audit purposes[2]

**Example consent flow:**
```text
AI: "I need to access your calendar to schedule this meeting."
Host: [Shows consent dialog]
      "Allow access to Calendar?"
      - Events: Read access
      - Destination: calendar-server (localhost)
User: [Approves or Denies]
```

### Data Transmission Controls

**Host responsibilities:**
- Prevent unauthorized data transmission
- Verify server identity before sending data
- Encrypt data in transit
- Log all data access[2]

**Server responsibilities:**
- Only request necessary data
- Specify data usage clearly
- Implement data minimization
- Support data deletion requests

### Privacy-Preserving Patterns

**Data filtering:**
```text
Instead of: "Send entire user database to server"
Do: "Send only fields needed: name, email (filter out SSN, payment info)"
```

**Local processing:**
```text
Instead of: "Send documents to cloud for analysis"
Do: "Process documents locally via stdio transport"
```

**Aggregation:**
```text
Instead of: "Access individual transaction records"
Do: "Access pre-aggregated summary statistics"
```

## Access Control Implementation

### Least Privilege Principle

**Deploy narrowly scoped servers:**[3]

**Bad: Monolithic server**
```text
company-server
  - Full database access
  - All file system access
  - Email sending
  - Calendar management
  - CRM access
```

**Good: Focused servers**
```text
customer-db-server → Read-only access to customer table
email-server → Only send, no inbox access
calendar-server → Current user's calendar only
crm-server → Read-only sales data
```

**Benefits:**
- Reduced attack surface
- Easier security auditing
- Clearer permission boundaries
- Simplified compliance

### Permission Scoping

**Resource scoping:**
```json
{
  "server": "file-server",
  "allowed_paths": [
    "~/Documents/Projects/",
    "~/Documents/Work/"
  ],
  "denied_paths": [
    "~/.ssh/",
    "~/Documents/Personal/"
  ]
}
```

**Tool scoping:**
```json
{
  "server": "database-server",
  "allowed_operations": ["read", "query"],
  "denied_operations": ["write", "delete", "admin"],
  "rate_limit": {
    "queries_per_minute": 10
  }
}
```

### Multi-Layer Security

**Defense in depth:**

1. **Host-level:** User authorization
2. **Transport-level:** Encrypted connections
3. **Server-level:** Authentication and scope limits
4. **Resource-level:** Per-resource permissions
5. **Tool-level:** Parameter validation and approval
6. **Audit-level:** Comprehensive logging

## Enterprise Security Integration

### Virtual Network Integration

For enterprise deployments:[15]

**Network isolation:**
- Servers deployed within corporate VNet
- No public internet exposure
- Firewall rules enforced
- Private endpoints for services

**Benefits:**
- Compliance with network policies
- Integration with existing security infrastructure
- Controlled data flow
- Reduced attack surface

### Data Loss Prevention (DLP)

**DLP integration:**[15]
- Scan data before transmission
- Block sensitive data patterns (SSN, credit cards)
- Alert on policy violations
- Enforce data handling policies

**Implementation:**
```text
User Data → DLP Scanner → Policy Check → [Allow/Block] → MCP Server
```

### Audit and Compliance

**Comprehensive logging (2025 Enhanced Requirements):**
- All authentication attempts
- Resource access patterns
- Tool executions and parameters
- User consent decisions
- Errors and security events
- **Full model→MCP→tool interaction chains** for end-to-end auditability[4]
- **MCP server inventory** with continuous tracking[4]
- **Policy violation alerts** and automated remediation playbooks[4]

**Log data:**
```json
{
  "timestamp": "2025-04-11T10:30:00Z",
  "user": "john@example.com",
  "action": "tool_execution",
  "server": "email-server",
  "tool": "send_email",
  "parameters": {
    "to": "customer@example.com",
    "subject": "Re: Support request"
  },
  "result": "success",
  "consent": "granted",
  "token_audience": "email-server.example.com",
  "policy_check": "passed"
}
```

**Compliance support:**
- GDPR compliance (consent, data access, deletion)
- SOC 2 requirements (audit trails, access controls)
- HIPAA compliance (PHI protection)
- Industry-specific regulations
- **Explicit data scoping mandates** for sensitive data access[6]
- **User consent requirements** when bridging models to datasets[6]

## Security Best Practices

### For Server Developers

**1. Input Validation (CRITICAL - 2025 Priority)**
- Validate all parameters rigorously - command injection and RCE vulnerabilities are actively exploited[1][3]
- Sanitize user inputs and model-generated inputs
- Prevent injection attacks through strict allowlisting
- Use parameterized queries and commands
- Never execute unsanitized commands from LLM outputs
- Implement sandboxing for all command execution
- Regular security audits for command handling code

**2. Token Validation (CRITICAL)**
- **Always verify tokens** - use well-tested libraries, not custom implementations
- **Validate audience claim** - ensure token's `aud` claim matches your server's resource indicator
- **Use token introspection** - verify tokens with authorization server's introspection endpoint
- **Check token expiration** - reject expired tokens immediately
- **Verify required scopes** - ensure token contains necessary scopes for requested operation
- **Never skip validation** - receiving a token doesn't mean it's valid or meant for your server

**3. Error Handling**
- Don't leak sensitive information in errors
- Use generic error messages for users
- Log detailed errors securely with correlation IDs
- Handle timeouts and failures gracefully
- Return proper 401 challenges with `WWW-Authenticate` header including `Bearer`, `realm`, and `resource_metadata`

**4. Secure Credential Management**
- Never log credentials, tokens, authorization codes, or secrets
- Scrub `Authorization` headers and query strings from logs
- Use environment variables or secret managers
- Rotate credentials regularly
- Support credential revocation
- Separate app vs. resource server credentials - don't reuse MCP server's client secret for end-user flows

**5. Rate Limiting**
- Implement request rate limits
- Prevent abuse and DoS
- Provide clear error messages when limits exceeded
- Monitor for unusual patterns

### For Client/Host Developers

**1. User Consent (Enhanced 2025 Requirements)**
- Always obtain explicit consent
- Show clear, understandable consent dialogs
- Allow granular approval decisions
- Support consent revocation
- **Implement guardrails and runtime controls** - MCP provides no default protections[1][4][6]
- **Deploy endpoint policy agents** to monitor and vet server access[4]
- **Require authentication by default** - no unauthenticated server access[1][2]

**2. OAuth Flow Implementation**
- **Discover Protected Resource Metadata** - fetch PRM document from server's `resource_metadata` URI
- **Discover Authorization Server** - fetch metadata via OIDC Discovery or OAuth 2.0 Metadata endpoints
- **Handle Client Registration** - support both pre-registered credentials and Dynamic Client Registration (DCR)
- **Support authorization code with PKCE** - most secure flow for user authorization
- **Implement token refresh** - handle token expiration gracefully
- **Use Resource Indicators (RFC 8707)** - always specify audience during token requests
- **Store tokens securely** - use encrypted storage with proper access controls

**3. Server Verification**
- Verify server identity
- Check server signatures if available
- Maintain server allowlist
- Warn on untrusted servers
- Validate Protected Resource Metadata responses

**4. Secure Transport**
- Use HTTPS for remote connections (enforce in production)
- Accept plain HTTP only for `localhost` during development
- Encrypt sensitive data
- Validate certificates
- Implement certificate pinning for high-security scenarios

**5. Audit Trails (Enhanced Observability - 2025)**
- Log all significant events
- Include context for audit review with correlation IDs
- Protect logs from tampering
- Implement log retention policies
- **Track full model→MCP→tool chains** for end-to-end visibility[4]
- **Maintain continuous MCP server inventory**[4]
- **Implement automated risk assessment** of server configurations[4]

### For End Users

**1. Review Permissions**
- Understand what each server can access
- Review consent requests carefully
- Revoke unused server permissions
- Question overly broad permission requests

**2. Server Selection**
- Use servers from trusted sources
- Review server documentation
- Check community reputation
- Prefer open-source servers for transparency

**3. Monitor Activity**
- Review audit logs periodically
- Watch for unexpected behavior
- Report security concerns
- Keep software updated

## Threat Modeling

### Common Threats

**1. Command Injection and RCE (Critical - 2025 Trend)**
- Risk: Command injection and remote code execution vulnerabilities discovered in modern MCP servers, especially developer-created integrations with unsafe command handling[1][3]
- Mitigation: Rigorous input validation, parameterized commands, sandboxing, security audits
- Impact: Can lead to complete server compromise and lateral movement

**2. Prompt Injection (Emerging Threat)**
- Risk: LLMs manipulated through MCP interface to invoke uncontrolled actions[7]
- Mitigation: Strict prompt validation, action allowlisting, user confirmation for sensitive operations
- Impact: Unauthorized tool execution, data access, privilege escalation

**3. Malicious Server**
- Risk: Server requests excessive permissions
- Mitigation: Least privilege, user review, scoped permissions, endpoint policy controls

**4. Data Exfiltration**
- Risk: Server transmits data without consent
- Mitigation: Consent requirements, DLP, audit logging, explicit data scoping

**5. Credential Theft**
- Risk: Server credentials compromised
- Mitigation: Secure storage, rotation, environment variables, audience-scoped tokens

**6. Token Mis-Redemption (Mitigated in 2025)**
- Risk: Generic tokens used across multiple servers enabling unauthorized access
- Mitigation: Resource Indicators (RFC 8707), audience-scoped tokens[2]
- Status: Token reuse now deprecated

**7. Privilege Escalation**
- Risk: Server accesses unauthorized resources, poor privilege boundaries enable lateral movement[3][4]
- Mitigation: Strict scoping, permission checks, sandboxing, runtime policy enforcement

**8. Unsafe Model Actions**
- Risk: Lack of default controls allows unsafe agent actions and privilege escalation[3][4]
- Mitigation: Guardrails, action approval workflows, runtime monitoring

### Security Testing

**Test scenarios:**
1. Attempt access without consent
2. Try accessing out-of-scope resources
3. Submit malicious parameters
4. Test authentication bypass attempts
5. Verify audit logging completeness
6. Check for information disclosure in errors
7. **Command injection testing** - test for unsafe command handling[1][3]
8. **Prompt injection vectors** - attempt to manipulate LLM actions via MCP[7]
9. **Token mis-redemption** - verify audience-scoped token enforcement[2]
10. **Privilege escalation paths** - test for lateral movement opportunities[3][4]
11. **Policy control bypass** - attempt to circumvent runtime enforcement[4]

## 2025 Security Status Summary

**Critical Updates:**
- OAuth Resource Server classification with mandatory Resource Indicators (RFC 8707)[2]
- Command injection and RCE vulnerabilities actively exploited in MCP servers[1][3]
- Prompt injection emerging as significant threat vector[7]
- Token reuse across servers now deprecated - audience-scoped tokens required[2]
- Unauthenticated server access considered critical misconfiguration[1][2]
- No native guardrails - authentication, authorization, and sandboxing must be implemented[1][4][6]

**Enterprise Requirements:**
- Mandatory OAuth integration with proper token scoping[2]
- Endpoint policy controls and runtime enforcement[4]
- End-to-end observability with full interaction chain logging[4]
- Continuous server inventory and automated risk assessment[4]
- Explicit data scoping and user consent for sensitive data access[6]

**Deprecated Practices:**
- Generic bearer tokens across multiple servers
- Optional authentication in production environments
- Implicit trust assumptions for data privacy
- Ad hoc observability without full chain tracking

## References

[1] https://equixly.com/blog/2025/03/29/mcp-server-new-security-nightmare/
[2] https://auth0.com/blog/mcp-specs-update-all-about-auth/
[3] https://www.akto.io/blog/mcp-security-risks
[4] https://zenity.io/blog/security/securing-the-model-context-protocol-mcp
[6] https://businessinsights.bitdefender.com/security-risks-agentic-ai-model-context-protocol-mcp-introduction
[7] https://www.pomerium.com/blog/june-2025-mcp-content-round-up
[15] Previous enterprise integration references
[16] https://modelcontextprotocol.io/docs/tutorials/security/authorization - Official MCP authorization tutorial
[17] https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization - MCP authorization specification
[18] https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-13 - OAuth 2.1
[19] https://datatracker.ietf.org/doc/html/rfc8414 - OAuth 2.0 Authorization Server Metadata
[20] https://datatracker.ietf.org/doc/html/rfc7591 - Dynamic Client Registration
[21] https://datatracker.ietf.org/doc/html/rfc9728 - Protected Resource Metadata
[22] https://datatracker.ietf.org/doc/html/rfc8707 - Resource Indicators

## Related Concepts

### Prerequisites
- [[mcp_overview]] - Need to understand MCP fundamentals before security model
- [[mcp_architecture]] - Security model built on top of MCP architecture

### Related Topics
- [[mcp_resources]] - Security considerations for resource access control
- [[mcp_tools]] - Critical security for tool execution and side effects
- [[filesystem]] - Filesystem access requires careful security considerations

### Extends
- [[mcp_architecture]] - Adds comprehensive security layer to architecture

### Extended By
- [[mcp_implementation]] - Need to understand security requirements for implementation