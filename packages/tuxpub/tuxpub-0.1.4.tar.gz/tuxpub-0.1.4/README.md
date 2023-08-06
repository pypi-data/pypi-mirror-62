# TuxPub

TuxPub is a flask based application which builds a directory listing from S3.

URL strings are based on /folder/ in the S3 bucket.

# Configuration

Configuration is handled through environment variables. The following
configuration variables are used.

- `S3_BUCKET`
  - required: True
  - description: S3 bucket name containing the files to serve. Example:
    `storage.staging.lkft.org`
- `S3_REGION`
  - required: True
  - description: Region containing the S3 bucket. Example: `us-east-1`
- `ROOT_INDEX_LISTING`
  - required: False
  - description: Defaults to `True`. Set to `False` to hide the top level
    directory/file listing.
- `SITE_TITLE`
  - required: False
  - description: Defaults to `Tuxpub`. Set to anything you like for a global
    site title.

# Run Locally

To run locally, install tuxpub, ensure AWS access is available environmentally,
and run:

```shell
S3_BUCKET=storage.staging.lkft.org S3_REGION=us-east-1 ROOT_INDEX_LISTING=True FLASK_APP=tuxpub pipenv run flask run
```

# Lambda/Zappa

This application is intended to be ran and deployed with Zappa/Lambda.

To setup zappa run:

```shell
zappa init
zappa deploy dev
```

An example zappa_settings.json file may look like:
```json
{
    "dev": {
        "app_function": "tuxpub.app",
        "aws_region": "us-east-1",
        "project_name": "lkft-tuxpub",
        "runtime": "python3.7",
        "s3_bucket": "zappa-tuxpub",
        "environment_variables": {
          "S3_BUCKET": "storage.dev.lkft.org",
          "S3_REGION": "us-east-1",
          "ROOT_INDEX_LISTING": "True",
        }
    }
}
```

# Export: Return a list of files

It is possible to return a list of files in an JSON array. Currently only
JSON is supported.

curl http://localhost/path/to/files/?export=json

The important bit to note is ?export=json.

# Root Index listing

By default this application will display the directories and files on the
INDEX page, however a user might not want to allow people to crawl through
the S3 bucket. You can set `ROOT_INDEX_LISTING=False`, which will render a
empty index page.
