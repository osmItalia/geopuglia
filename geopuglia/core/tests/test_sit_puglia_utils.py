import mock
import pytest

from core.sit_puglia_utils import build_url, download_and_save


TEST_URLS = {'test': '{foglio}-{filename}'}

TEST_FILE_URL = 'www.test.com/test.zip'

@pytest.mark.parametrize(('tavoletta', 'expected_result'), [
    (10, '1-1101'),
    (8, '1-1081')
])
def test_build_url(tavoletta, expected_result):
    """
    Check that if tavoletta <= 9 then a leading 0 is added
    """
    with mock.patch('core.sit_puglia_utils.URLS', TEST_URLS):
        url_to_test = build_url(download_type='test',
                                foglio='1',
                                tavoletta=tavoletta,
                                quadrante='1')
        assert url_to_test == expected_result
        assert isinstance(url_to_test, str)


@mock.patch('__builtin__.open')
@mock.patch('core.sit_puglia_utils.requests')
def test_download_and_save_response_ok(mocked_requests, mocked_open):
    mocked_requests.get.return_value = mock.MagicMock(ok=True)
    download_and_save(TEST_FILE_URL)
    mocked_requests.get.assert_called_once_with(TEST_FILE_URL, stream=True)
    assert mocked_open.assert_called_once_with('./downloads/test.zip', "wb")


@mock.patch('__builtin__.open', )
@mock.patch('core.sit_puglia_utils.requests')
def test_download_and_save_response_not_ok(mocked_requests, mocked_open):
    mocked_requests.get.return_value = mock.MagicMock(ok=False)
    download_and_save(TEST_FILE_URL)
    mocked_requests.get.assert_called_once_with(TEST_FILE_URL, stream=True)
    download_and_save('test')
    assert not mocked_open.called
