# ekrhizoc
ekrhizoc (E6c): A web crawler

## Contents
1. [Definition](#definition)
2. [Use Case](#use-case)
3. [Configuration](#configuration)
4. [Development](#development)
5. [Testing](#testing)
6. [Versioning](#versioning)
7. [Deployment](#deployment)
8. [Production](#production)

## Definition

εκρίζωση (Greek)
ekrízosi / uprooting, eradication

Also known as __E6c__.

## Use Case

Implementation of a simple python web crawler.  
Input: URL (seed).  
Output: simple textual sitemap (to show links between pages).

### Requirements

* The crawler is limited to *__one__* subdomain (exclude external links).
* No use of web crawling libraries/frameworks (e.g. scrapy).
* (Optional) Use of HTML handling Libraries/Frameworks.
* Production-ready code.

### Assumptions

* The input URL (seed) is limited to __only__ one at every run.
* The targeted URL(s) are static pages (no backend javascript parsing required).
* Links to be extracted from HTML anchor `<a>` elements.
* Valid links include
    - Valid URL
        + Non empty
        + Matches a valid url pattern
        + Does not exceed the `E6C_MAX_URL_LENGTH` length in characters
        + Possible to convert a relative urls to a full url
    - Link is not visited before
    - Link is not part of an ignored file type
    - Link has the same domain as the seed url
    - Link is not restricted by the robots.txt file

### Design

This project implements a Basic Universal Crawler based on breadth first search graph traversal.

## Configuration

Behaviour of the application can be configured via Environment Variables.

| Environment Variable | Description | Type | Default Value |
| -------------- | -------------- | -------------- | -------------- |
| `E6C_LOG_LEVEL` | Level of logging - overrides verbose/quiet flag | string | - |
| `E6C_LOG_DIR` | Directory to save logs | string | - |
| `E6C_BIN_DIR` | Directory to save any output (bin) | string | bin |
| `E6C_IGNORE_FILETYPES` | File types of websites to ignore (e.g. ".filetype1,.filetype2") | string | ".png,.pdf,.txt,.doc,.jpg,.gif" |
| `E6C_URL_REQUEST_TIMER` | Time (in seconds) to wait per request (not to populate server with multiple requests) | float | 0.1 |
| `E6C_MAX_URLS` | The maximum number of urls to fetch/crawl | integer | 10000 |
| `E6C_MAX_URL_LENGTH` | The maximum length (character count) of a url to fetch/crawl | integer | 300 |

## Development

### Configure for local development

* Clone [repo](https://github.com/nichelia/ekrhizoc) on your local machine
* Install [`conda`](https://www.anaconda.com) or [`miniconda`](https://docs.conda.io/en/latest/miniconda.html)
* Create symlink for githooks (based on [`isort`](https://github.com/timothycrosley/isort), [`black`](https://github.com/psf/black)):  
`$ make git-hooks`
* Create your local project environment (based on [`conda`](https://www.anaconda.com), [`poetry`](https://python-poetry.org)):  
`$ make env`
* (Optional) Update existing local project environment:  
`$ make env-update`

### Run locally

On a terminal, run the following (execute on project's root directory):

* Activate project environment:  
`$ . ./scripts/helpers/environment.sh`
* Run the CLI using `poetry`:  
`$ poetry run ekrhizoc`

### Contribute

[ Not Available ]

## Testing

[ Work in progress... ]

To run the tests, open a terminal and run the following (execute on project's root directory):

* Activate project environment:  
`$ . ./scripts/helpers/environment.sh`
* To run pytest:  
`$ pytest -v`
* To check test coverage:  
`$ pytest --cov=. --cov-report=term-missing`

## Versioning

Increment the version number:  
`$ poetry version {bump rule}`  
where valid bump rules are:

1. patch
2. minor
3. major
4. prepatch
5. preminor
6. premajor
7. prerelease

### Changelog

Use `CHANGELOG.md` to track the evolution of this package.  
The `[UNRELEASED]` tag at the top of the file should always be there to log the work until a release occurs.  

Work should be logged under one of the following subtitles:
* Added
* Changed
* Fixed
* Removed

On a release, a version of the following format should be added to all the current unreleased changes in the file.  
`## [major.minor.patch] - YYYY-MM-DD`

## Deployment

### Pip package

On a terminal, run the following (execute on project's root directory):

* Activate project environment:  
`$ . ./scripts/helpers/environment.sh`
* To build pip package:  
`$ make build-package`
* To publish pip package (requires credentials to PyPi):  
`$ make publish-package`

### Docker image

On a terminal, run the following (execute on project's root directory):

* Activate project environment:  
`$ . ./scripts/helpers/environment.sh`
* To build docker image:  
`$ make build-docker`

## Production

For production, a Docker image is used.
This image is published publicly on [docker hub](https://hub.docker.com/repository/docker/nichelia/ekrhizoc).

* First pull image from docker hub:  
`$ docker pull nichelia/ekrhizoc:[version]`
* First pull image from docker hub:  
`$ docker run --rm -it -v ~/ekrhizoc_bin:/usr/src/bin nichelia/ekrhizoc:[version]`  
This command mounts the application's bin (outcome) to user's root directory under ekrhizoc_bin folder.

where version is the published application version (e.g. 0.1.0)

