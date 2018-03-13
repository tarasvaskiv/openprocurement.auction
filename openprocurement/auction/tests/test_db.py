import pytest
import iso8601
from datetime import datetime
from dateutil.tz import tzlocal

from openprocurement.auction.tests.utils import test_public_document, \
    put_test_doc


@pytest.mark.usefixtures("db2")
class TestTemplateViews(object):

    def test_chronograph_view(self, db2):
        with put_test_doc(db2, dict(test_public_document)):  # dict makes copy of object
            for data in db2.view('chronograph/start_date').rows:
                assert data.get('value') == {u'start': test_public_document['stages'][0]['start'],
                                             u'procurementMethodType': u'',
                                             u'auction_type': test_public_document['auction_type'],
                                             u'mode': u'', u'api_version': test_public_document['TENDERS_API_VERSION']}

    def test_start_date_view(self, db2):
        """This test checks if view returns correct 1 stage time. Utc is ignored due couchdb javascript"""

        with put_test_doc(db2, dict(test_public_document)):
            for data in db2.view('auctions/by_startDate').rows:
                result_from_couchdb = data.get('key')
                assert data.get('value') is None
                assert iso8601.parse_date(test_public_document["stages"][0]["start"]).time() == \
                       datetime.fromtimestamp(result_from_couchdb / 1000).time()

    def test_end_date_view(self, db2):
        """This test checks if view returns correct (endDate of doc) or doc.stages[0].start"""

        with put_test_doc(db2, dict(test_public_document)):
            for data in db2.view('auctions/by_endDate').rows:
                result_from_couchdb = data.get('key')
                assert data.get('value') is None
                assert iso8601.parse_date(test_public_document["stages"][0]["start"]).time() == \
                       datetime.fromtimestamp(result_from_couchdb / 1000).time()

        # here we test when couchdb returns endDate
        temp_test_public_document = dict(test_public_document)
        temp_date  = datetime.now(tzlocal()).replace(microsecond=0).isoformat()
        temp_test_public_document['endDate'] = temp_date

        with put_test_doc(db2, temp_test_public_document):
            for data in db2.view('auctions/by_endDate').rows:
                result_from_couchdb = data.get('key')
                assert data.get('value') is None
                assert iso8601.parse_date(temp_date).time() == \
                       datetime.fromtimestamp(result_from_couchdb / 1000).time()

    def test_pre_announce_view(self, db2):
        with put_test_doc(db2, dict(test_public_document)):
            for data in db2.view('auctions/PreAnnounce').rows:
                assert data.get('key') is None
                assert data.get('value') is None

        temp_test_public_document = dict(test_public_document)
        temp_test_public_document['current_stage'] = 0
        with put_test_doc(db2, temp_test_public_document):
            data = db2.view('auctions/PreAnnounce').rows
            assert data == []

