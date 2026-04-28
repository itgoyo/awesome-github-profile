# Awesome GitHub Profile README

A curated list of awesome GitHub Profile READMEs sorted by stars.

## Structure

```
awesome-github-profile/
├── README.md          # Main list — sorted by GitHub stars
├── CONTRIBUTING.md    # How to contribute
├── LICENSE            # CC BY 4.0
└── scripts/
    └── update_stars.py  # Script to refresh star counts
```

## Data Sources

- Profile list sourced from [abhisheknaiidu/awesome-github-profile-readme](https://github.com/abhisheknaiidu/awesome-github-profile-readme)
- Star counts fetched via GitHub API
- Last updated: 2024

## Development

To refresh star counts:

```bash
pip install requests
python scripts/update_stars.py
```

Requires `GITHUB_TOKEN` environment variable for higher rate limits.
