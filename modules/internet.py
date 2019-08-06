from http import client

def have_internet():
    conn = client.HTTPConnection('www.google.com', timeout=5)
    try:
        conn.request('HEAD', '/')
        conn.close()
        return True
    except:
        conn.close()
        return False