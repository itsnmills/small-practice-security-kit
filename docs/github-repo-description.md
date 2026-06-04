# GitHub Repo Description

GitHub repository descriptions are remote metadata, so they cannot be committed through this repo as a file change.

Recommended description:

```text
PHI-avoidant security readiness packet builder for small healthcare practices.
```

If the GitHub CLI is installed and authenticated, update the repository metadata with:

```bash
gh repo edit itsnmills/small-practice-security-kit --description "PHI-avoidant security readiness packet builder for small healthcare practices."
```

If `gh` is unavailable or not authenticated, update it in the GitHub UI:

1. Open `https://github.com/itsnmills/small-practice-security-kit`.
2. Use the repository description edit control near the top of the repo page.
3. Paste the recommended description above and save.

Keep the description short and avoid claims that the repo certifies HIPAA compliance, provides legal advice, makes breach-notification decisions, or replaces qualified professionals.
