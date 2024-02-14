import argparse
import asyncio
from telnetlib3 import open_connection

async def check_port(address, port):
    try:
        reader, writer = await open_connection(address, port)
        writer.close()
        return True
    except (ConnectionRefusedError, OSError):
        return False

async def wait_for_port(address, port, max_timeout=15, interval=2):
    print(f"Waiting for {max_timeout} sec - port available on host {address} (max wait timeout ~ {max_timeout} sec)")
    
    for _ in range(max_timeout // interval):
        if await check_port(address, port):
            print("Port is open")
            return
        else:
            print("Port is not available")
            await asyncio.sleep(interval)

    print(f"Timeout reached. Port is not available on {address}:{port}")
    exit()

def main():
    parser = argparse.ArgumentParser(description="Check if a port is open or wait for it to become available.")
    parser.add_argument("--address", required=True, help="Host address")
    parser.add_argument("--port", type=int, required=True, help="Port number")
    parser.add_argument("--timeout", type=int, default=15, help="Max wait timeout in seconds")

    args = parser.parse_args()

    if args.timeout <= 0:
        print("Timeout must be a positive integer.")
        return

    loop = asyncio.get_event_loop()
    
    if args.timeout > 0:
        loop.run_until_complete(wait_for_port(args.address, args.port, args.timeout))
    else:
        is_port_open = loop.run_until_complete(check_port(args.address, args.port))
        if is_port_open:
            print("Port is open")
        else:
            print("Port is not available")
            exit()

if __name__ == "__main__":
    main()
