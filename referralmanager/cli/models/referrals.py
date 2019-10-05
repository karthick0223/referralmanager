# coding=utf-8
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.types import Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ProbioBloodReferral(Base):
    __tablename__ = "probio_bloodreferrals"
    crid = Column(Integer, primary_key=True, nullable=False) 
    pnr  = Column(String, nullable=False)
    rid  = Column(String, nullable=False)
    datum = Column(Date, nullable=False)      
    tid  = Column(String, nullable=False)        
    sign = Column(Integer)        
    countyletter  = Column(String, nullable=False)
    new = Column(String, nullable=False)          
    progression = Column(String, nullable=False)
    follow_up    = Column(String, nullable=False)
    cf_dna1 = Column(String, nullable=False)
    cf_dna2 = Column(String, nullable=False)
    cf_dna3 = Column(String, nullable=False)
    kommentar = Column(String, nullable=False)
    filnamn = Column(String, nullable=False)
    def __init__(self, row_dict):
        """ Create an object from a single line in a csv file
        Element order:
        pnr;rid;datum;tid;sign;county_letter;new;progression;follow_up;cf_dna1;cf_dna2;cf_dna3;kommentar;filnamn
        """
        self.crid = row_dict.get('rid', None)
        self.pnr  = row_dict.get('pnr', None)
        self.rid  = row_dict.get('rid', None)
        self.datum = row_dict.get('datum', None)
        self.tid  = row_dict.get('tid', None)
        self.sign = row_dict.get('sign', None)
        self.countyletter  = row_dict.get('countyletter', None)
        self.new = row_dict.get('new', None)
        self.progression = row_dict.get('progression', None)
        self.follow_up    = row_dict.get('follow_up', None)
        self.cf_dna1 = row_dict.get('CF_DNA1', None)
        self.cf_dna2 = row_dict.get('CF_DNA2', None)
        self.cf_dna3 = row_dict.get('CF_DNA3', None)
        self.kommentar = row_dict.get('kommentar', None)
        self.filnamn = row_dict.get('filnamn', None)


        self.datum = datetime.strptime(self.datum, "%Y%m%d")

        # If the signed field is not an integer (e.g. due to missing signature on the referral), change it to -1
        try:
            self.sign = int(self.sign)
        except ValueError:
            self.sign = -1

class PsffBloodReferral(Base):
    __tablename__ = "psff_bloodreferrals"
    crid = Column(Integer, primary_key=True, nullable=False)
    rid  = Column(String, nullable=False)
    datum = Column(Date, nullable=False)
    tid  = Column(String, nullable=False)
    sign = Column(Integer)
    blood1 = Column(String, nullable=False)
    blood2 = Column(String, nullable=False)
    blood3 = Column(String, nullable=False)
    blood4 = Column(String, nullable=False)
    comment = Column(String, nullable=False)
    filnamn = Column(String, nullable=False)
    cdk = Column(String, nullable=False)
    def __init__(self, row_dict):
        """ Create an object from a single line in a csv file
        Element order:
        pnr;rid;datum;tid;sign;county_letter;new;progression;follow_up;cf_dna1;cf_dna2;cf_dna3;kommentar;filnamn
        """
        self.crid = row_dict.get('rid', None)
        self.rid  = row_dict.get('rid', None)
        self.datum = row_dict.get('datum', None)
        self.tid  = row_dict.get('tid', None)
        self.sign = row_dict.get('sign', None)
        self.blood1 = row_dict.get('blood1', None)
        self.blood2 = row_dict.get('blood2', None)
        self.blood3 = row_dict.get('blood3', None)
        self.blood4 = row_dict.get('blood4', None)
        self.comment = row_dict.get('comment', None)
        self.filnamn = row_dict.get('filnamn', None)
        self.cdk = row_dict.get('cdk', None)


        self.datum = datetime.strptime(self.datum, "%Y%m%d")

        # If the signed field is not an integer (e.g. due to missing signature on the referral), change it to -1
        try:
            self.sign = int(self.sign)
        except ValueError:
            self.sign = -1


class AlasccaBloodReferral(Base):
    __tablename__ = "alascca_bloodreferrals"
    crid = Column(Integer, primary_key=True, nullable=False)
    pnr = Column(String, nullable=False)
    collection_date = Column(Date, nullable=False)
    collection_time = Column(Integer)
    signed = Column(Integer)
    hospital_code = Column(Integer)
    county = Column(String)
    barcode1 = Column(Integer)
    barcode2 = Column(Integer)
    barcode3 = Column(Integer)
    file_name = Column(String)
    type_string = 'ALASCCA_blod'

    def __init__(self, line, separator=";"):
        """ Create an object from a single line in a csv file
        Element order:
        pnr;rid;datum;tid;sign;hospital;county;blood1;blood2;blood3;filnamn
        """
        elm = line.strip("\n").split(separator)
        (self.pnr, self.crid, self.collection_date, self.collection_time, self.signed, self.hospital_code, self.county,
         self.barcode1, self.barcode2, self.barcode3, self.file_name) = elm

        self.collection_date = datetime.strptime(self.collection_date, "%Y%m%d")

        # If the signed field is not an integer (e.g. due to missing signature on the referral), change it to -1
        try:
            self.signed = int(self.signed)
        except ValueError:
            self.signed = -1


class AlasccaTissueReferral(Base):
    __tablename__ = "alascca_tissuereferrals"
    crid = Column(Integer, primary_key=True, nullable=False)
    pnr = Column(String, nullable=False)
    collection_date = Column(Date, nullable=False)
    radiotherapy = Column(Integer)
    sectioning_date = Column(Date)
    pad = Column(String)
    hospital_code = Column(Integer)
    county = Column(String)
    barcode1 = Column(Integer)
    barcode2 = Column(Integer)
    comments = Column(String)
    file_name = Column(String)
    type_string = 'ALASCCA_colon_rektum'

    def __init__(self, line, separator=";"):
        """ Create an object from a single line in a csv file
        Element order:
        pnr;rid;datum;strål_radio;snittningsdatum;PAD-nummer;sjukhus;län;tissue1;tissue2;kommentar;filnamn
        """
        elm = line.strip("\n").split(separator)
        (self.pnr, self.crid, self.collection_date, self.radiotherapy, self.sectioning_date, self.pad,
         self.hospital_code, self.county, self.barcode1, self.barcode2, self.comments, self.file_name) = elm

        self.collection_date = datetime.strptime(self.collection_date, "%Y%m%d")
        try:
            self.sectioning_date = datetime.strptime(self.sectioning_date, "%Y%m%d")
        except ValueError:
            # Currently just setting the sectioning date to None if it is not a valid datetime value:
            self.sectioning_date = None
