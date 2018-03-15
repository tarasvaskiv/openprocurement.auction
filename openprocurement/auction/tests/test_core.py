import pytest

from mock import MagicMock, patch
from uuid import uuid4
from openprocurement.auction.core import RunDispatcher, Planning


class TestRunDispatcher(object):
    """Testing all methods from RunDispatcher class"""

    def test_init(self):
        chronograph = MagicMock()
        item = {'status': None}

        with pytest.raises(TypeError) as raised_exception:
            RunDispatcher(chronograph)
        assert raised_exception.value.message == \
               "__init__() takes exactly 3 arguments (2 given)"

        run_dispatcher = RunDispatcher(chronograph, item)
        assert run_dispatcher.chronograph == chronograph
        assert run_dispatcher.item == item

    def test_repr(self):
        chronograph = MagicMock()
        attrs = {'get.return_value': 'belowthreshold'}
        item = MagicMock(**attrs)

        run_dispatcher = RunDispatcher(chronograph, item)
        assert str(run_dispatcher) == '<Auction runner: {}>'.format(
            attrs['get.return_value'])
        item.get.assert_called_once_with('procurementMethodType', 'default')

        attrs = {'get.return_value': None}
        item = MagicMock(**attrs)
        run_dispatcher.item = item

        assert str(run_dispatcher) == '<Auction runner: default>'
        item.get.assert_called_once_with('procurementMethodType', 'default')

    @patch('openprocurement.auction.core.prepare_auction_worker_cmd',
           return_value=[])
    def test_call(self, prepare_auction_worker_cmd):
        document_id = uuid4().hex

        chronograph = MagicMock()
        attrs = {'mode': 'not test', 'api_version': '2.4'}
        item = MagicMock()
        item.__getitem__.side_effect = attrs.__getitem__

        run_dispatcher = RunDispatcher(chronograph, item)
        result = run_dispatcher(document_id)
        assert result == []

        attrs['mode'] = 'test'
        item.__getitem__.side_effect = attrs.__getitem__
        run_dispatcher = RunDispatcher(chronograph, item)
        result = run_dispatcher(document_id)
        assert result == ['--auction_info_from_db', 'true']


class TestPlanning(object):
    """Testing all methods from Planning class"""

    def test_init(self):
        bridge = MagicMock()
        item = {'status': None}

        with pytest.raises(TypeError) as raised_exception:
            Planning(bridge)
        assert raised_exception.value.message == \
               "__init__() takes exactly 3 arguments (2 given)"

        planning = Planning(bridge, item)
        assert planning.bridge == bridge
        assert planning.item == item

    def test_next(self):
        bridge = MagicMock()
        item = {'status': None}
        planning = Planning(bridge, item)

        assert id(next(planning)) == id(planning)

    # TODO: Test all possible combinations.
    @pytest.mark.parametrize('item',
                             [{'status': None}
                              ])
    def test_iter_status(self, item):
        bridge = MagicMock()
        planning = Planning(bridge, item)

        assert [x for x in planning] == []
