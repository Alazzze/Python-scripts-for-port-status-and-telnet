import argparse
import asyncio
from telnetlib3 import open_connection

async def check_port(address, port):
    try:
        reader, writer = await open_connection(address, port)
        writer.close()  # Close the writer to terminate the connection
        # Removed the await writer.wait_closed() line since it's not supported by telnetlib3
        return True
    except (ConnectionRefusedError, OSError):
        return False

async def wait_for_port(address, port, max_timeout=15, interval=2):
    print(f"Waiting for {max_timeout} sec - port available on host {address} (max wait timeout ~ {max_timeout} sec)")
    
    for _ in range(max_timeout // interval):
        if await check_port(address, port):
            print("Port is open")
            return True  # Return True when the port is open
        else:
            print("Port is not available")
            await asyncio.sleep(interval)

    print(f"Timeout reached. Port is not available on {address}:{port}")
    return False  # Return False when the port did not open in time

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
    port_status = loop.run_until_complete(wait_for_port(args.address, args.port, args.timeout))
    if not port_status:
        exit(1)  # Exit with a non-zero status to indicate the port is not available

if __name__ == "__main__":
    main()
