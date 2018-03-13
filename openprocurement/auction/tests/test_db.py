import pytest
import iso8601
from datetime import datetime
from openprocurement.auction.tests.utils import test_public_document, \
    test_public_document_with_mode, \
    test_public_document_end_date, test_public_document_current_stage


class TestTemplateViews(object):
    @pytest.mark.parametrize(
        'save_doc', [dict(test_public_document)], indirect=['save_doc'])
    def test_chronograph_view(self, db2, save_doc):
        for data in db2.view('chronograph/start_date').rows:
            assert data.get('value') == {u'start': test_public_document['stages'][0]['start'],
                                         u'procurementMethodType': u'',
                                         u'auction_type': test_public_document['auction_type'],
                                         u'mode': u'', u'api_version': test_public_document['TENDERS_API_VERSION']}

    @pytest.mark.parametrize(
        'save_doc', [dict(test_public_document_with_mode)], indirect=['save_doc'])
    def test_chronograph_view_mode(self, db2, save_doc):
        for data in db2.view('chronograph/start_date').rows:
            assert data.get('value') == {u'start': test_public_document['stages'][0]['start'],
                                         u'procurementMethodType': u'',
                                         u'auction_type': test_public_document['auction_type'],
                                         u'mode': test_public_document_with_mode['mode'], u'api_version': test_public_document['TENDERS_API_VERSION']}

    @pytest.mark.parametrize(
        'save_doc', [dict(test_public_document)], indirect=['save_doc'])
    def test_start_date_view(self, db2, save_doc):
        """This test checks if view returns correct 1 stage time. Utc is ignored due couchdb javascript"""
        for data in db2.view('auctions/by_startDate').rows:
            result_from_couchdb = data.get('key')
            assert data.get('value') is None
            assert iso8601.parse_date(test_public_document['stages'][0]['start']).time() == \
                   datetime.fromtimestamp(result_from_couchdb / 1000).time()

    @pytest.mark.parametrize(
        'save_doc', [dict(test_public_document)], indirect=['save_doc'])
    def test_end_date_view_1(self, db2, save_doc):
        """This test checks if view returns correct (endDate of doc) or doc.stages[0].start"""
        for data in db2.view('auctions/by_endDate').rows:
            result_from_couchdb = data.get('key')
            assert data.get('value') is None
            assert iso8601.parse_date(test_public_document['stages'][0]['start']).time() == \
                   datetime.fromtimestamp(result_from_couchdb / 1000).time()

    @pytest.mark.parametrize(
        'save_doc', [dict(test_public_document_end_date)], indirect=['save_doc'])
    def test_end_date_view_2(self, db2, save_doc):
        """Here we test when couchdb returns endDate"""

        for data in db2.view('auctions/by_endDate').rows:
            result_from_couchdb = data.get('key')
            assert data.get('value') is None
            assert iso8601.parse_date(test_public_document_end_date['endDate']).time() == \
                   datetime.fromtimestamp(result_from_couchdb / 1000).time()

    @pytest.mark.parametrize(
        'save_doc', [dict(test_public_document)], indirect=['save_doc'])
    def test_pre_announce_view_1(self, db2, save_doc):
        for data in db2.view('auctions/PreAnnounce').rows:
            assert data.get('key') is None
            assert data.get('value') is None

    @pytest.mark.parametrize(
        'save_doc', [dict(test_public_document_current_stage)], indirect=['save_doc'])
    def test_pre_announce_view_2(self, db2, save_doc):
        data = db2.view('auctions/PreAnnounce').rows
        assert data == []

