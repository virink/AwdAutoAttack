import aiohttp,asyncio

session = aiohttp.ClientSession()

def ggg():
    r =  session.get("http://www.baidu.com")
    print(dir(r))
    result = r.json()
    print(result)


if __name__ == "__main__":
    a = ggg()
    session.close()
