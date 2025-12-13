import httpx
import pytest

FEED_DATA = {
    "url": "https://feeds.npr.org/1001/rss.xml",
    "title": "NPR News",
    "site_url": "https://www.npr.org/",
    "poll_frequency": 900,
    "description": "NPR News RSS Feed",
}


@pytest.mark.asyncio
async def test_create_feed(client: httpx.AsyncClient):
    """Tests a post request to /feeds/"""

    response = await client.post("/feeds/", json=FEED_DATA)

    assert response.status_code == 201
    data = response.json()
    assert data["url"] == FEED_DATA["url"]
    assert data["title"] == FEED_DATA["title"]
    assert data["site_url"] == FEED_DATA["site_url"]
    assert data["description"] == FEED_DATA["description"]
    assert data["poll_frequency"] == FEED_DATA["poll_frequency"]
    assert "id" in data  # Ensure UUID is returned
    assert data["is_active"] is True  # default value check


@pytest.mark.asyncio
async def test_get_feed(client: httpx.AsyncClient):
    """Tests a get request to /feeds/{feed_id}"""

    create_response = await client.post("/feeds/", json=FEED_DATA)
    feed_id = create_response.json()["id"]

    get_response = await client.get(f"/feeds/{feed_id}")

    assert get_response.status_code == 200
    data = get_response.json()
    assert data["id"] == feed_id
    assert data["url"] == FEED_DATA["url"]


@pytest.mark.asyncio
async def test_get_all_feeds(client: httpx.AsyncClient):
    """Tests a get request to /feeds/"""

    # Create two feeds
    await client.post("/feeds/", json=FEED_DATA)
    another_feed_data = FEED_DATA.copy()
    another_feed_data["url"] = "https://feeds.npr.org/1002/rss.xml"
    await client.post("/feeds/", json=another_feed_data)

    get_response = await client.get("/feeds/")

    assert get_response.status_code == 200
    data = get_response.json()
    assert isinstance(data, list)
    assert len(data) >= 2  # At least two feeds should be present


@pytest.mark.asyncio
async def test_read_nonexistent_feed(client: httpx.AsyncClient):
    """
    Test GET /feeds/{uuid} returns 404 for random UUID
    """
    random_uuid = "123e4567-e89b-12d3-a456-426614174000"
    response = await client.get(f"/feeds/{random_uuid}")

    assert response.status_code == 404
