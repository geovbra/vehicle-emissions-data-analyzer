import pytest, requests

def test_flask():
    response = requests.get('https://isp-proxy.tacc.utexas.edu/geovbra-2/')
    assert response.status_code == 200

if __name__ == "__main__":
    pytest.main()
