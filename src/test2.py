import requests

url = 'https://yinxingxue.github.io/papers/ase2020_CCGraph%20A%20PDG%20based%20Code%20Clone%20Detector%20With%20Approximate%20Graph%20Matching.pdf'
response = requests.get(url, stream=True)

# 检查响应状态码是否为200，表示请求成功
if response.status_code == 200:
    # 以二进制写入模式打开文件
    with open('test.pdf', 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)
        print('PDF 文件已下载到本地')
else:
    print('请求失败')