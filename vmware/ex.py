# 列出所哟虚拟机
client.vcenter.VM.list()


# 过滤虚拟机信息
my_vm = client.vcenter.VM.list(client.vcenter.VM.FilterSpec(names={'test-188'}))[0]


# 虚拟机的一些属性
my_vm.to_dict()
my_vm.vm
my_vm.name
my_vm.cpu_count
my_vm.memory_size_mib


# 查询指定的集群 ID
client.vcenter.Cluster.list(Cluster.FilterSpec(names={'wiqun'}))[0].cluster


# 查询网络
client.vcenter.Network.list(Network.FilterSpec())


# 查询资源池
client.vcenter.ResourcePool.list(ResourcePool.FilterSpec())


# 获取 stub_config
stub_config = client._stub_config


# 根据内容库的名字以及它的类型来获得内容库 id
library_service = Library(stub_config)
library_id = library_service.find(Library.FindSpec(name='ova'))[0]


# 根据内容库 ID 获取内容库中的模板
template_name = 'Base-CentOS-30G'
library_item_service = Item(stub_config)
library_item_id = library_item_service.find(Item.FindSpec(name=template_name, library_id=library_id))[0]
library_item_obj = library_item_service.get(library_item_id)



# 创建部署目标
library_item = LibraryItem(stub_config)
deployment_target = library_item.DeploymentTarget(resource_pool_id=resource_pool_id)







# 创建 ResourcePoolDeploymentSpec
deployment_spec = library_item.ResourcePoolDeploymentSpec(
    name="test",
    annotation="",
    accept_all_eula=True,
    network_mappings={"VM Network": network_id},
    storage_mappings={"group1": storage_group_mapping},
)




import urllib3
import requests
from com.vmware.vcenter.ovf_client import LibraryItem, DiskProvisioningType, ImportFlag
from com.vmware.vcenter_client import Folder, ResourcePool, Cluster, Network, Datastore, Host

from vmware.vapi.vsphere.client import create_vsphere_client
from com.vmware.content_client import (Library,
                                       LibraryModel,
                                       LocalLibrary,
                                       SubscribedLibrary)
from com.vmware.content.library_client import (Item,
                                               ItemModel,
                                               StorageBacking,
                                               SubscribedItem)

user = 'Administrator@vsphere.local'
ip = '192.168.1.201'
password = 'Admin123#'
network_name = 'VM Network'
cluster_name = 'dev'
datastore_name = "192.168.1.25-dbstore"
# folder_name = ""
content_library_name = 'ova'
template_name = 'Base-CentOS-30G'
vm_name = 'aijin'
host_ip = '192.168.1.25'

session = requests.session()
session.verify = False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
client = create_vsphere_client(server=ip, username=user, password=password, session=session)


stub_config = client._stub_config
library_item = LibraryItem(stub_config)
network_id = client.vcenter.Network.list(
            Network.FilterSpec(names={network_name},
                               types={Network.Type.STANDARD_PORTGROUP}))[0].network

cluster_id = client.vcenter.Cluster.list(Cluster.FilterSpec(names={cluster_name}))[0].cluster
resource_pool_id = client.vcenter.ResourcePool.list(ResourcePool.FilterSpec(clusters={cluster_id}))[0].resource_pool

host_id = client.vcenter.Host.list(Host.FilterSpec(names={host_ip}))[0].host


datastore_id = client.vcenter.Datastore.list(Datastore.FilterSpec(names={datastore_name}))[0].datastore
library_service = Library(stub_config)
library_id = library_service.find(Library.FindSpec(name=content_library_name))[0]

library_item_service = Item(stub_config)
library_item_id = library_item_service.find(Item.FindSpec(name=template_name, library_id=library_id))[0]

ovf_lib_item_service = LibraryItem(stub_config)

deployment_target = library_item.DeploymentTarget(resource_pool_id=resource_pool_id, host_id=host_id)
# deployment_target = library_item.DeploymentTarget(host_id=host_id)



# ovf_lib_item_service.filter(library_item_id, deployment_target)

storage_group_mapping = ovf_lib_item_service.StorageGroupMapping(
    type=ovf_lib_item_service.StorageGroupMapping.Type('DATASTORE'),
    datastore_id=datastore_id,
    provisioning=DiskProvisioningType('thin')
)

deployment_spec = library_item.ResourcePoolDeploymentSpec(
    name=vm_name,
    annotation="take care",
    accept_all_eula=True,
    network_mappings={"你的配置": network_id},
    storage_mappings={"你的配置": storage_group_mapping},
)

result = library_item.deploy(library_item_id, deployment_target, deployment_spec)



