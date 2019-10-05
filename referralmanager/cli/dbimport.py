import importlib
import json
import logging
import os

import click
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
import csv
from referralmanager.cli.models.referrals import Base, AlasccaBloodReferral, AlasccaTissueReferral, PsffBloodReferral, ProbioBloodReferral


@click.command()
@click.option('--dbcred', type=click.File('r'), required=True)
@click.option('--local-data-dir', type=str, required=True)
@click.option('--referral-type', type=click.Choice(['ProbioBloodReferral', 'PsffBloodReferral', 'AlasccaBloodReferral', 'AlasccaTissueReferral']), required=True)
@click.pass_context
def dbimport(ctx, dbcred, local_data_dir, referral_type):
    logging.info("Running database import from dir {}".format(local_data_dir))
    cred_conf = json.load(dbcred)

    engine = create_tables(cred_conf['dburi'])
    session = get_session(engine)

    module = importlib.import_module('referralmanager.cli.models.referrals')
    referral_class = getattr(module, referral_type)

    import_referrals(session, local_data_dir, referral_class)


def create_tables(uri):
    engine = create_engine(uri, echo=True)
    Base.metadata.create_all(engine)
    return engine


def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()


def import_referrals(session, searchdir, referral_class, fileending="csv"):
    files = [f for f in os.listdir(searchdir) if f.endswith(fileending)]
    for fn in files:
        with open(os.path.join(searchdir, fn), 'r', encoding='latin_1') as f:
            row_pointer = csv.DictReader(f, delimiter =';')
            for each_row in row_pointer:
                each_row = dict(each_row)
                ref = referral_class(each_row)
                try:
                    session.add(ref)
                    session.commit()
                except IntegrityError:
                    session.rollback()
