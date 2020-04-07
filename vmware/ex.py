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

cluster_id = client.vcenter.Cluster.list(Cluster.FilterSpec(names={cluster_name}))[0].cluster





1.24-1.185-huidu-CentOS_20G_V002,



vcenter_user = 'Administrator@vsphere.local'
vcenter_ip = '192.168.0.97'
vcenter_password = 'Admin123#'

network_name = 'VM Network'
datastore_name = "1.25-dbstore"
content_library_name = 'ovas'
template_name = 'CentOS_20G_V1'
vm_name = 'zijin'
host_ip = '192.168.1.25'



