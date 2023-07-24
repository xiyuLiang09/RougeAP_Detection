import subprocess
import os

def ping_site():
    try:
        os.system("chcp 437")
        # 运行ping命令，并获取输出
        output = subprocess.check_output(['ping', '-n', '20', 'google.com'], shell=True, text=True)
        # 从输出中解析出平均TTL和RTT
        lines = output.strip().split('\n')
        # Initialize empty lists to store TTL and time values
        time_values = []

        second_line = lines[1]
        print(second_line)
        ttl_start = second_line.find('TTL=') + 4
        ttl_value = int(second_line[ttl_start:])
        # Loop through the data to extract TTL and time values
        for line in lines:
            if 'time=' in line:

                time_start = line.find('time=') + 5
                time_end = line.find('ms', time_start)
                time_values.append(int(line[time_start:time_end]))

        # Remove the maximum and minimum values from the lists
        time_values.remove(max(time_values))
        time_values.remove(min(time_values))

        # Calculate the average TTL and time

        average_time = sum(time_values) / len(time_values)
        return ttl_value,average_time


    except subprocess.CalledProcessError:
        print("Ping failed.")
        return None, None


if __name__ == '__main__':
    ttl_1, avg_rtt_1 = ping_site()
    print("ttl:", ttl_1)
    print("avg_rtt", avg_rtt_1)
    input("now switch your connection(then press enter to continue):")
    ttl_2, avg_rtt_2 = ping_site()
    print("ttl:", ttl_2)
    print("avg_rtt", avg_rtt_2)

