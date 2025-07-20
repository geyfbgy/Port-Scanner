
import socket
import time

def scan_port(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)  # increased timeout
        result = s.connect_ex((target, port))
        s.close()
        
        if result == 0:
            print(f"[+] Port {port} is OPEN")
            return True
        else:
            print(f"[-] Port {port} is CLOSED")
            return False
            
    except socket.gaierror:
        print(f"[-] Hostname {target} could not be resolved")
        return None
    except socket.error as e:
        print(f"[-] Could not connect to {target}:{port} - {e}")
        return False
    except Exception as e:
        print(f"[-] Unexpected error scanning port {port}: {e}")
        return False

def main():
    print("=== Simple Python Port Scanner ===")
    
    try:
        target = input("Enter target IP or hostname: ").strip()
        if not target:
            print("[!] Target cannot be empty")
            return
            
        start_port = int(input("Enter start port (e.g., 20): ").strip())
        end_port = int(input("Enter end port (e.g., 1024): ").strip())
        
        if start_port < 1 or end_port > 65535 or start_port > end_port:
            print("[!] Invalid port range. Ports must be between 1-65535 and start <= end")
            return
            
    except ValueError:
        print("[!] Please enter valid port numbers")
        return

    print(f"\n[*] Scanning {target} from port {start_port} to {end_port}...")
    start_time = time.time()
    
    open_ports = []
    total_ports = end_port - start_port + 1

    try:
        for i, port in enumerate(range(start_port, end_port + 1), 1):
            print(f"[*] Progress: {i}/{total_ports} - Scanning port {port}...", end='\r')
            result = scan_port(target, port)
            if result is True:
                open_ports.append(port)
            elif result is None:  # hostname resolution failed
                break
                
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user.")
    except Exception as e:
        print(f"[!] Error during scan: {e}")

    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n[✓] Scan complete in {duration:.2f} seconds.")
    print(f"[✓] Found {len(open_ports)} open ports: {open_ports}")

if __name__ == "__main__":
    main()
