# `referral-manager`

[![Build Status](https://travis-ci.org/ClinSeq/referral-manager.svg?branch=master)](https://travis-ci.org/ClinSeq/referral-manager) [![Code Health](https://landscape.io/github/ClinSeq/referral-manager/master/landscape.svg?style=flat)](https://landscape.io/github/ClinSeq/referral-manager/master)

`referral-manager` is a package to download new referrals from the KI Biobank customer FTP and add them to the local mysql referral database. 

## Command line 

`refman` is the main command for the package. It has two subcomponents, `fetch` and `dbimport`. 

### `fetch`

Downloads CSV files and PDF with new referrals from KI Biobank customer FTP. 

The user must specify a local base directory and a remote base directory. This subcommand checks the remote directory (customer ftp) for updated referral files (pdfs and csvs) that are not in the local directory, and syncs those changes, also reorganising the copied files into a "csv" and a "pdf" folder locally. Creates those csv and pdf folders if necessary.

E.g.:
`refman fetch --local-data-dir /nfs/ALASCCA/referrals/blood --remote-data-dir ALASCCA/Scannade_remisser/ALASCCA_blod`
`refman fetch --local-data-dir /nfs/ALASCCA/referrals/tissue --remote-data-dir ALASCCA/Scannade_remisser/ALASCCA_colon_rektum`

`refman --sentry-login <sentrylogin> fetch --referrals-login <remote ftp login.json> --local-data-dir /nfs/PROBIO/referraldb/remote_files --remote-data-dir /ProBio2/Scannade_remisser`

These example commands would fetch referrals from the remote `ALASCCA_blood` and `ALASCCA_colon_rektum` directories.

### `dbimport`

This subcommand imports the information from the local csv files (in a specified directory) into the local postgres database, given a specified referral type.

E.g.:
`refman dbimport --dbcred /nfs/ALASCCA/clinseq-referraldb-config.json --local-data-dir /nfs/ALASCCA/referrals/blood --referral-type AlasccaBloodReferral`

`refman --sentry-login <sentry login file> dbimport --dbcred <db url config.json> --local-data-dir /nfs/PROBIO/referraldb/remote_files/csv --referral-type ProbioBloodReferral`

This example finds CSV files in the directory /nfs/ALASCCA/referrals/blood and imports any new data into the tables corresponding to the AlasccaBloodReferral type. `/nfs/ALASCCA/clinseq-referraldb-config.json` should be a json file like so:

~~~json
{
  "dburi": "sqlite:///:memory:" // replace with proper sqlalchemy connection string
}
~~~

## API

Developers can use the classes `AlasccaBloodReferral` and `AlasccaTissueReferral` to handle referral data in other packages. 
