import time
import pywifi
import requests


def get_wifi_scan_results():
    print("SCAN AP INFO...")
    wifi = pywifi.PyWiFi()  # 创建Wi-Fi对象
    iface = wifi.interfaces()[0]  # 获取Wi-Fi接口对象

    iface.scan()

    time.sleep(5)

    scan_results = iface.scan_results()
    return scan_results


def get_manufacturer_from_bssid(mac_address):
    mac_prefix = mac_address[:8]  # 获取前8位MAC地址，即前24位BSSID
    url = f"https://api.macvendors.com/{mac_prefix}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text.strip()
    except requests.RequestException as e:
        print(f"Failed to get OUI vendor: {e}")
    return "Not found"


def compare_manufacturer(scan_results, target_ssid):
    print("analyzing manufacturer...")
    target_bssids = [wifi_info.bssid for wifi_info in scan_results if wifi_info.ssid == target_ssid]
    if len(target_bssids) > 1:
        print(f"find: {len(target_bssids)} different AP with the same name(ssid)")
        manuList = []
        for bssid in target_bssids:
            manuList.append(get_manufacturer_from_bssid(bssid))
        list=set(manuList)
        if len(list)==1:
            print("All from one manufacturer(or not found)")
        else :
            print("Suspicious AP may exists:check the list")
            print(list)
    else:
        print("FAIL to find more than one AP")


def compare_RSS(scan_results, target_ssid):
    print("analyzing signal...")
    target_aps = [wifi_info for wifi_info in scan_results if wifi_info.ssid == target_ssid]

    strongestAP = target_aps[0]
    RSS_list = []
    for ap in target_aps:
        RSS_list.append(ap.signal)
        if ap.signal > strongestAP.signal:
            strongestAP = ap

    # sortList = sorted(RSS_list, reverse=True)
    # print("MAX signal:", sortList[0])
    # val = sortList[0] - sortList[1]
    # print("Subtract the second largest AP signal:", val)
    # return strongestAP
    print("Max RSS:", strongestAP.signal)
    print("check out the list:", RSS_list)


if __name__ == "__main__":
    scan_result = get_wifi_scan_results()
    target_ssid = input("INPUT SSID(NAME): ")
    compare_manufacturer(scan_result, target_ssid)
    compare_RSS(scan_result, target_ssid)
