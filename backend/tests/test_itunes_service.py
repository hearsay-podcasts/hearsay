import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.services.itunes import ITunesArtworkService


class TestBuildArtworkUrls:
    def test_replaces_100x100bb_with_sizes(self):
        service = ITunesArtworkService()
        url = "https://is1-ssl.mzstatic.com/image/thumb/Podcasts/v4/abc/100x100bb.jpg"
        result = service._build_artwork_urls(url)
        assert result == {
            "sm": "https://is1-ssl.mzstatic.com/image/thumb/Podcasts/v4/abc/300x300bb.jpg",
            "md": "https://is1-ssl.mzstatic.com/image/thumb/Podcasts/v4/abc/600x600bb.jpg",
            "lg": "https://is1-ssl.mzstatic.com/image/thumb/Podcasts/v4/abc/100000x100000-999.jpg",
        }

    def test_handles_different_extensions(self):
        service = ITunesArtworkService()
        url = "https://is1-ssl.mzstatic.com/image/thumb/Podcasts/v4/abc/100x100bb.png"
        result = service._build_artwork_urls(url)
        assert result["sm"].endswith("300x300bb.png")
        assert result["md"].endswith("600x600bb.png")
        assert result["lg"].endswith("100000x100000-999.png")

    def test_returns_none_if_pattern_not_found(self):
        service = ITunesArtworkService()
        url = "https://example.com/some-image.jpg"
        result = service._build_artwork_urls(url)
        assert result is None


class TestLookupById:
    @pytest.mark.asyncio
    async def test_returns_artwork_urls_on_success(self):
        service = ITunesArtworkService()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "resultCount": 1,
            "results": [{"artworkUrl100": "https://is1-ssl.mzstatic.com/image/thumb/Podcasts/v4/abc/100x100bb.jpg"}],
        }

        with patch.object(service.client, "get", new_callable=AsyncMock, return_value=mock_response):
            result = await service.lookup_by_id("12345")

        assert result is not None
        assert result["sm"].endswith("300x300bb.jpg")

    @pytest.mark.asyncio
    async def test_returns_none_on_no_results(self):
        service = ITunesArtworkService()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"resultCount": 0, "results": []}

        with patch.object(service.client, "get", new_callable=AsyncMock, return_value=mock_response):
            result = await service.lookup_by_id("99999")

        assert result is None

    @pytest.mark.asyncio
    async def test_returns_none_on_http_error(self):
        service = ITunesArtworkService()

        with patch.object(service.client, "get", new_callable=AsyncMock, side_effect=Exception("timeout")):
            result = await service.lookup_by_id("12345")

        assert result is None


class TestSearchPodcast:
    @pytest.mark.asyncio
    async def test_returns_artwork_urls_for_first_result(self):
        service = ITunesArtworkService()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "resultCount": 2,
            "results": [
                {"artworkUrl100": "https://is1-ssl.mzstatic.com/image/thumb/Podcasts/v4/first/100x100bb.jpg"},
                {"artworkUrl100": "https://is1-ssl.mzstatic.com/image/thumb/Podcasts/v4/second/100x100bb.jpg"},
            ],
        }

        with patch.object(service.client, "get", new_callable=AsyncMock, return_value=mock_response):
            result = await service.search_podcast("My Podcast")

        assert result is not None
        assert "first" in result["sm"]

    @pytest.mark.asyncio
    async def test_returns_none_on_no_results(self):
        service = ITunesArtworkService()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"resultCount": 0, "results": []}

        with patch.object(service.client, "get", new_callable=AsyncMock, return_value=mock_response):
            result = await service.search_podcast("Nonexistent Podcast")

        assert result is None


class TestGetArtworkUrls:
    @pytest.mark.asyncio
    async def test_uses_lookup_when_itunes_id_provided(self):
        service = ITunesArtworkService()
        expected = {"sm": "s", "md": "m", "lg": "l"}

        with patch.object(service, "lookup_by_id", return_value=expected) as mock_lookup:
            result = await service.get_artwork_urls(itunes_id="123", title="Test")

        mock_lookup.assert_called_once_with("123")
        assert result == expected

    @pytest.mark.asyncio
    async def test_falls_back_to_search_when_lookup_fails(self):
        service = ITunesArtworkService()
        expected = {"sm": "s", "md": "m", "lg": "l"}

        with patch.object(service, "lookup_by_id", return_value=None) as mock_lookup, \
             patch.object(service, "search_podcast", return_value=expected) as mock_search:
            result = await service.get_artwork_urls(itunes_id="123", title="Test Pod")

        mock_lookup.assert_called_once_with("123")
        mock_search.assert_called_once_with("Test Pod")
        assert result == expected

    @pytest.mark.asyncio
    async def test_uses_search_when_no_itunes_id(self):
        service = ITunesArtworkService()
        expected = {"sm": "s", "md": "m", "lg": "l"}

        with patch.object(service, "search_podcast", return_value=expected) as mock_search:
            result = await service.get_artwork_urls(itunes_id=None, title="Test Pod")

        mock_search.assert_called_once_with("Test Pod")
        assert result == expected

    @pytest.mark.asyncio
    async def test_returns_none_when_all_methods_fail(self):
        service = ITunesArtworkService()

        with patch.object(service, "lookup_by_id", return_value=None), \
             patch.object(service, "search_podcast", return_value=None):
            result = await service.get_artwork_urls(itunes_id="123", title="Test")

        assert result is None
