import os
import unittest

from referralmanager.cli.dbimport import create_tables, import_referrals, get_session
from referralmanager.cli.models.referrals import AlasccaBloodReferral, AlasccaTissueReferral


class TestDbImport(unittest.TestCase):
    def setUp(self):
        self.blood_signature_ok = AlasccaBloodReferral(
            "191212121212;00159725;20160405;1500;1;301;AB;03098121;03098122;03098123;100029_00159725.pdf")
        self.blood_signature_space = AlasccaBloodReferral(
            "191212121212;00159725;20160405;1500; ;301;AB;03098121;03098122;03098123;100029_00159725.pdf")

    # Test that we get 1 when the signature field has "1"
    def test_signature_ok(self):
        self.assertEquals(self.blood_signature_ok.signed, 1)

    # Test that we get -1 when the signature field has " "
    def test_signature_space(self):
        self.assertEqual(self.blood_signature_space.signed, -1)

    def test_import_bloodreferral(self):
        engine = create_tables('sqlite:///:memory:')
        #engine = create_tables('postgresql+psycopg2://referral_writer:inserter@127.0.0.1:5432/referrals')
        session = get_session(engine)

        blood_searchdir = os.path.join('tests', AlasccaBloodReferral.type_string)
        import_referrals(session, blood_searchdir, AlasccaBloodReferral)

        assert len(session.query(AlasccaBloodReferral).all()) == 2

        # Try to import the same referral again, should do nothing
        import_referrals(session, blood_searchdir, AlasccaBloodReferral)
        assert len(session.query(AlasccaBloodReferral).all()) == 2

        # Test that the signature fields are 1 and -1 respectively
        assert session.query(AlasccaBloodReferral.signed).all() == [(1,), (-1,)]

    def test_import_tissuereferral(self):
        engine = create_tables('sqlite:///:memory:')
        #engine = create_tables('postgresql+psycopg2://referral_writer:inserter@127.0.0.1:5432/referrals')
        session = get_session(engine)

        tissue_searchdir = os.path.join('tests', AlasccaTissueReferral.type_string)
        import_referrals(session, tissue_searchdir, AlasccaTissueReferral)

        assert len(session.query(AlasccaTissueReferral).all()) == 2

        # Try to import the same referral again, should do nothing
        import_referrals(session, tissue_searchdir, AlasccaTissueReferral)
        assert len(session.query(AlasccaTissueReferral).all()) == 2
