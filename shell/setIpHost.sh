#!/bin/bash
if [[ $(whoami) == "root" ]];then
echo "当前执行权限: root"
else
echo "当前用户:" $(whoami)
echo "请使用管理员权限执行脚本."
exit
fi


ifcfg_path=`ls /etc/sysconfig/network-scripts/ifcfg-ens*`
echo "当前网卡路径${ifcfg_path}"
cp ${ifcfg_path} "${ifcfg_path}.bak"


while read -p "是否设置本机静态IP,退出输入:n,设置IP输入:y  [y|n]" yn
do
	[ -z ${yn} ] && yn=${yn:-y}
	if [[ ${yn} == [Nn] ]];then
		exit
	elif [[ ${yn} == [Yy] ]];then
		while read -p "输入本机IP地址,如192.168.31.123 :" ip
		do
			read -p "将设置ip地址为${ip},请确认[y|n]:" yn
			[ -z ${yn} ] && yn=${yn:-y}
			if [[ ${yn} == [Yy] ]];then
				read -p "输入DNS, 如:192.168.31.1 (Default:192.168.31.1):" dns
				read -p "输入网关,如192.168.31.1 (Default:192.168.31.1):" gateway
				read -p "输入掩码,如255.255.255.0 (Default:255.255.255.0):" mask
				
				echo "IP: "${ip}
				echo "DNS:"${dns:-"192.168.31.1"}
				echo "网关:"${gateway:-"192.168.31.1"}
				echo "掩码:"${mask:-"255.255.255.0"}
				read -p "以上配置是否正确？若是写错请按n重新配置. 请确认[y|n]:" yn
				[ -z ${yn} ] && yn=${yn:-y}
				if [[ ${yn} == [Yy] ]];then
					sed -i 's/^ONBOOT.*$/ONBOOT=yes/g' ${ifcfg_path}
					sed -i 's/^BOOTPROTO.*$/BOOTPROTO=static/g' ${ifcfg_path}
					echo -e "IPADDR=${ip}\nGATEWAY=${gateway:-"192.168.31.1"}\nNETMASK=${mask:-"255.255.255.0"}\nDNS1=${dns:-"192.168.31.1"}" >> ${ifcfg_path}
				else
					continue
				fi
			else
				continue
			fi

			read -p "是否将${ip//./-}作为hostname?请确认[y|n]:" yn
			[ -z ${yn} ] && yn=${yn:-y}
			if [[ ${yn} == [Yy] ]];then
				hostnamectl set-hostname ${ip//./-}
			else 
				read -p "请手动输入hostname: " hname
				read -p '确认以"'${hname}'"为hostname [y|n]:' yn
				if [[ ${yn} == [Yy] ]];then
					hostnamectl set-hostname ${hname}
				fi
			fi
			read -p '需要重启生效,是否重启 [y|n]: ' yn
			[ -z ${yn} ] && yn=${yn:-y}
			if [[ ${yn} == [Yy] ]];then
				reboot
			fi
			exit
		done
	fi
done

