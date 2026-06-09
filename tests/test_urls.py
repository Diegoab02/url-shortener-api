def test_shorten_url(client):
    response = client.post("/urls/shorten", json={
        "original": "https://www.google.com"
    })
    assert response.status_code == 201
    data = response.json()
    assert "code" in data
    assert data["clicks"] == 0
    assert data["original"] == "https://www.google.com/"


def test_shorten_url_invalida(client):
    response = client.post("/urls/shorten", json={
        "original": "esto-no-es-una-url"
    })
    assert response.status_code == 422


def test_redirect(client):
    post = client.post("/urls/shorten", json={
        "original": "https://www.google.com"
    })
    code = post.json()["code"]

    response = client.get(f"/urls/{code}", follow_redirects=False)
    assert response.status_code in (302, 307)


def test_clicks_incrementan(client):
    post = client.post("/urls/shorten", json={
        "original": "https://www.google.com"
    })
    code = post.json()["code"]

    client.get(f"/urls/{code}", follow_redirects=False)
    client.get(f"/urls/{code}", follow_redirects=False)

    stats = client.get(f"/urls/stats/{code}")
    assert stats.json()["clicks"] == 2


def test_stats(client):
    post = client.post("/urls/shorten", json={
        "original": "https://www.github.com"
    })
    code = post.json()["code"]

    response = client.get(f"/urls/stats/{code}")
    assert response.status_code == 200
    assert response.json()["code"] == code


def test_stats_codigo_inexistente(client):
    response = client.get("/urls/stats/noexiste")
    assert response.status_code == 404


def test_list_urls(client):
    client.post("/urls/shorten", json={"original": "https://www.google.com"})
    client.post("/urls/shorten", json={"original": "https://www.github.com"})

    response = client.get("/urls/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_delete_url(client):
    post = client.post("/urls/shorten", json={
        "original": "https://www.google.com"
    })
    code = post.json()["code"]

    delete = client.delete(f"/urls/{code}")
    assert delete.status_code == 204

    stats = client.get(f"/urls/stats/{code}")
    assert stats.status_code == 404


def test_delete_codigo_inexistente(client):
    response = client.delete("/urls/noexiste")
    assert response.status_code == 404