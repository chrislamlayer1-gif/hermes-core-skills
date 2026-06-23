---
name: security-hardening-checklist
description: Use when handling user input, authentication, data storage, or external integrations. Use when building any feature that accepts untrusted data, manages user sessions, or interacts with third-party services.
version: 1.0.0
author: Hermes Agent (adapted from addyosani/agent-skills)
license: MIT
metadata:
  hermes:
    tags: [security, hardening, checklist, owasp, threat-model]
    platform: [cursor, codex, claude-code]
    related_skills: [requesting-code-review, spec-driven-development]
  triggers:
    - security
    - vulnerability
    - xss
    - inject
    - auth
    - encrypt
    - harden
    - secure

domain: agent-core
subdomain: safety
tokens:
  scan: 330
  load: 2595
  category: detailed
---

# Security Hardening Checklist

## Overview

Security-first development practices. Treat every external input as hostile, every secret as sacred, and every authorization check as mandatory. Security isn't a phase — it's a constraint on every line of code that touches user data, authentication, or external systems.

## When to Use

- Building anything that accepts user input
- Implementing authentication or authorization
- Storing or transmitting sensitive data
- Integrating with external APIs or services
- Adding file uploads, webhooks, or callbacks
- Handling payment or PII data
- **Mini Program specific:** Handling user's WeChat OpenID, UnionID, or phone number

## Process: Threat Model First

Controls bolted on without a threat model are guesses. Before hardening, spend five minutes thinking like an attacker:

1. **Map the trust boundaries.** Where does untrusted data cross into your system? HTTP requests, form fields, file uploads, webhooks, third-party APIs, message queues, and **LLM output**. Every boundary is attack surface.

2. **Name the assets.** What's worth stealing or breaking? Credentials, PII, payment data, admin actions, money movement.

3. **Run STRIDE over each boundary:**

| Threat | Ask | Typical mitigation |
|---|---|---|
| **S**poofing | Can someone impersonate a user/service? | Authentication, signature verification |
| **T**ampering | Can data be altered in transit or at rest? | Integrity checks, parameterized queries, HTTPS |
| **R**epudiation | Can an action be denied later? | Audit logging of security events |
| **I**nformation disclosure | Can data leak? | Encryption, field allowlists, generic errors |
| **D**enial of service | Can it be overwhelmed? | Rate limiting, input size caps, timeouts |
| **E**levation of privilege | Can a user gain rights they shouldn't? | Authorization checks, least privilege |

4. **Write abuse cases next to use cases.** For each feature, ask "how would I misuse this?" — then make that your first test.

If you can't name the trust boundaries for a feature, you're not ready to secure it. Most breaches begin in design, not code.

## The Three-Tier Boundary System

### Always Do (No Exceptions)

- **Validate all external input** at the system boundary (API routes, form handlers, Mini Program input fields)
- **Parameterize all database queries** — never concatenate user input into SQL
- **Encode output** to prevent XSS (use framework auto-escaping, don't bypass it)
- **Use HTTPS** for all external communication
- **Hash passwords** with bcrypt/scrypt/argon2 (never store plaintext)
- **Set security headers** (CSP, HSTS, X-Frame-Options, X-Content-Type-Options)
- **Use httpOnly, secure, sameSite cookies** for sessions
- **Run `npm audit`** (or equivalent) before every release
- **WeChat Mini Program specific:** Use wx.request with HTTPS only, never use wx.request with HTTP

### Ask First (Requires Chris Approval)

- Adding new authentication flows or changing auth logic
- Storing new categories of sensitive data (PII, payment info)
- Adding new external service integrations
- Changing CORS configuration
- Adding new npm dependencies (especially ones with native code)

### Never Do (Absolute Prohibitions)

- Hardcode secrets, API keys, or credentials in source code
- Log passwords, tokens, or PII in plaintext
- Store unhashed passwords anywhere
- Disable CSRF protection
- Trust user-supplied filenames without sanitization
- Bypass framework security features

## Mini Program Specific Security

For WeChat Mini Programs, these are extra concerns:

1. **OpenID/UnionID** — Treat as PII. Never log or expose to other users.
2. **wx.getUserInfo / wx.getPhoneNumber** — Only call when absolutely needed. Handle the data carefully.
3. **LocalStorage** — Don't store sensitive data in wx.setStorageSync. It's not encrypted.
4. **Cloud Functions** — If using微信雲開發, validate the calling context (cloud.callFunction vs HTTP trigger).
5. **Webview** — If using web-view component, validate all URLs loaded in it.
6. **Payment** — If adding 微信支付, follow WeChat's security guide exactly. Never handle payment key on client side.
7. **Rendering** — Be careful with WXS (WeiXin Script). It runs in a sandbox but can still be misused.

## Web Security Quick Reference

### Python
```python
# Bad: SQL injection
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
# Good: parameterized
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

# Bad: shell injection
os.system(f"ls {user_input}")
# Good: safe subprocess
subprocess.run(["ls", user_input], check=True)
```

### JavaScript / TypeScript
```javascript
// Bad: XSS through innerHTML
element.innerHTML = userInput;
// Good: safe textContent
element.textContent = userInput;

// Bad: eval with user data
const result = eval(userInput);
// Good: parse JSON safely
const result = JSON.parse(userInput);
```

### WeChat Mini Program
```javascript
// Bad: insecure request
wx.request({ url: 'http://api.example.com' })
// Good: HTTPS only
wx.request({ url: 'https://api.example.com' })

// Bad: open redirect through web-view
wx.navigateTo({ url: `/pages/webview/webview?url=${userInput}` })
// Good: validate URL against allowlist
const ALLOWED_URLS = ['https://example.com'];
if (ALLOWED_URLS.includes(userInput)) {
  wx.navigateTo({ url: `/pages/webview/webview?url=${encodeURIComponent(userInput)}` })
}
```

## LLM-Specific Security

When building features that use local LLM output in the game:

1. **LLM output is not trusted** — Treat generated text as user input. Sanitize before rendering.
2. **Prompt injection** — If LLM output influences game logic, validate it against an allowlist.
3. **Context leakage** — Don't include secrets/system prompts in user-facing output.
4. **Resource exhaustion** — LLM calls are blocking. Set timeouts and handle failures gracefully.

## Verification Checklist

Before shipping any feature, verify:

- [ ] Threat model done for this feature
- [ ] All external input validated
- [ ] No hardcoded secrets
- [ ] All database queries parameterized
- [ ] Output properly encoded
- [ ] HTTPS everywhere
- [ ] npm audit clean (or documented exceptions)
- [ ] Mini Program: no HTTP URLs in wx.request
- [ ] Mini Program: OpenID/UnionID handled carefully
- [ ] Error messages don't leak internal details
