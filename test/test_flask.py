import pytest, requests

def test_flask():
    response = requests.get('https://isp-proxy.tacc.utexas.edu/geovbra-2/')
    assert response.status_code == 200
def test_read_flask():
    response = requests.get('https://isp-proxy.tacc.utexas.edu/geovbra-2/read')
    assert response.status_code == 200
def test_create_flask():
    response = requests.get('https://isp-proxy.tacc.utexas.edu/geovbra-2/create')
    assert response.status_code == 200
def test_update_flask():
    response = requests.get('https://isp-proxy.tacc.utexas.edu/geovbra-2/update')
    assert response.status_code == 200
def test_delete_flask():
    response = requests.get('https://isp-proxy.tacc.utexas.edu/geovbra-2/delete')
    assert response.status_code == 200


if __name__ == "__main__":
    pytest.main()
