# Virden Jobs

## TODO
- [ ] Update Readme
- [ ] Doc strings
- [ ] Create Docker image build artifact
- [ ] seperate vjobs and vjobs_ebrandon into new repositories and publish to pypi

Virden Jobs takes jobs postings for jobs in Virden from specific websites and posts them as the specified facebook page.

## Setup

A config.py file needs to be created in the project's root directory. This will contain the Facebook Page ID and the Facebook Graph API token. It should be set up as follows.

```
TOKEN = 'Your Graph API token here'
PAGEID = 'Your Page ID here'
```

To install the required modules with pip runing `pip install -r prod-requirements.txt` in the project's root directory.

## Running

To execute the program run the main.py file from the virden_jobs directory in python. One way to run it is from the project's root directory run `python -m virden_jobs.main`
This will immediately check the job websites and post to Facebook.

In order to schedule running automatically, create a cron job.
