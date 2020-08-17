'''
通过一个国外的代理服务器加速下载
'''


from fabric import Connection

conn = Connection('root@fqq.haoyu95.cn')


image_path = 'registry.cn-shenzhen.aliyuncs.com/haoyu36'


def down_image(image):
    '''
    下载镜像并推送到个人镜像仓库
    :param image: 需要下载的 image，格式: <name>:<tag>
    '''
    if ':' in image:
        image_name, image_tag = image, 'latest'
    else:
        image_name, image_tag = image.split(':')
    
    conn.run(f'{image_name}:{image_tag}')
    conn.run('docker tag ')
















