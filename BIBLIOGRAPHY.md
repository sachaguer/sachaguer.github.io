# Automated Bibliography Updates

This repository includes an automated system to keep your bibliography up-to-date with your latest publications from the ADS (Astrophysics Data System).

## How it works

The `scripts/bibgen.py` script:

1. Queries the ADS API for publications by "Guerrini, Sacha"
2. Downloads the full BibTeX entries
3. Processes and customizes them (journal abbreviations, altmetric info, etc.)
4. Applies custom configurations from `_data/custom_bib.yml`
5. Updates `_bibliography/papers.bib`

## Setup

### 1. Get an ADS API Key

1. Go to https://ui.adsabs.harvard.edu/user/settings/token
2. Create a new API token
3. Copy the token

### 2. Add the API Key to GitHub Secrets

1. Go to your GitHub repository Settings
2. Navigate to Secrets and variables > Actions
3. Click "New repository secret"
4. Name: `ADS_API_KEY`
5. Value: Your ADS API token
6. Click "Add secret"

## Triggers

The bibliography will be automatically updated in these cases:

1. **When you push changes** to `_data/custom_bib.yml` or `scripts/bibgen.py`
2. **Weekly on Sundays** at 06:00 UTC (to catch new publications)
3. **Manually** by going to Actions > Update Bibliography > Run workflow

## Customization

You can customize individual publications by editing `_data/custom_bib.yml`. Any fields you add there will override the defaults from ADS.

Example:

```yaml
2023MNRAS.521.4359G: # This is the ADS bibcode
  selected: true
  preview: my_paper_image.png
  abstract: "Custom abstract text..."
```

## Manual Run

To manually update your bibliography:

```bash
export ADS_API_KEY="your_api_key_here"
cd scripts
python bibgen.py
```

## Dependencies

The script requires these Python packages (listed in `requirements.txt`):

- requests
- bibtexparser
- beautifulsoup4
- pyyaml
