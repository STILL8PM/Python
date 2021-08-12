# 保存图片
def save_base_image(img_str, filename):
    img_data = base64.b64decode(img_str)
    with open(filename, 'wb') as f:
        f.write(img_data)

# 获取token
def get_token():
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + client_id + '&client_secret=' + client_secret
    request = urllib.request.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib.request.urlopen(request)
    token_content = response.read()
    if token_content:
        token_info = json.loads(token_content)
        token_key = token_info['access_token']
    return token_key

# 人像分割
def body_seg_fore(filename, resultfilename):
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_seg"

    # 二进制方式打开图片文件
    f = open(filename, 'rb')
    img = base64.b64encode(f.read())

    params = dict()
    params['image'] = img
    params['type'] = 'foreground'
    params = urllib.parse.urlencode(params).encode("utf-8")
    # params = json.dumps(params).encode('utf-8')

    access_token = get_token()
    request_url = request_url + "?access_token=" + access_token
    request = urllib.request.Request(url=request_url, data=params)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    response = urllib.request.urlopen(request)
    content = response.read()
    if content:
        # print(content)
        content = content.decode('utf-8')
        # print(content)
        data = json.loads(content)
        # print(data)
        img_str = data['foreground']
        save_base_image(img_str, resultfilename)
