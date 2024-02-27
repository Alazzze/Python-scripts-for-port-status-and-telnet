import argparse
import getpass
import asyncio
import telnetlib3
import sys

async def receive_data(reader):
    while True:
        try:
            output = await reader.read(4096)
            if output:
                try:
                    decoded_output = output.decode('utf-8')
                    sys.stdout.write(decoded_output)
                    sys.stdout.flush()
                except UnicodeDecodeError:
                    sys.stdout.write(str(output))
                    sys.stdout.flush()
            else:
                sys.stdout.flush()
                await asyncio.sleep(0.1)

        except Exception as e:
            print(f"Error: {e}")
            break

async def send_command(writer, command):
    writer.write(command.encode('utf-8') + b"\n")
    await writer.drain()

async def check_port_status(address, port):
    try:
        reader, writer = await telnetlib3.open_connection(address, port, encoding=False)
        writer.close()
        return "Port is open"
    except OSError as e:
        if "Connect call failed" in str(e):
            return "Port is not available"
        else:
            raise e

async def main():
    parser = argparse.ArgumentParser(description="Telnet script to interact with a switch")
    parser.add_argument("--address", type=str, help="Switch IP address", required=True)
    parser.add_argument("--port", type=int, help="Switch port", required=True)
    args = parser.parse_args()

    host = args.address
    port = args.port

    port_status = await check_port_status(host, port)
    print(f"Port status: {port_status}")
    if port_status == "Port is not available":
        return

    try:
        reader, writer = await telnetlib3.open_connection(host=host, port=port, encoding=False)
        print(f"Successfully connected to {host}:{port}")
    except Exception as e:
        print(f"Error occurred / connection timed out while trying to connect {host}:{port}")
        print(f"Error details: {e}")
        return

    loop = asyncio.get_event_loop()
    loop.create_task(receive_data(reader))

    try:
        login = input("Enter login (press Enter to skip): ")
        password = getpass.getpass("Enter password (press Enter to skip): ")

        if login:
            await send_command(writer, login)
            await asyncio.sleep(2)

        if password:
            await send_command(writer, password)
            await asyncio.sleep(2)

        while True:
            command = input("\nEnter command (type 'exit' or 'quit' to exit): ")
            if command.lower() in ["exit", "quit"]:
                await send_command(writer, command)
                await asyncio.sleep(2)
                break
            await send_command(writer, command)
            await asyncio.sleep(2)
    except Exception as e:
        print(f"Error: {e}")

    writer.close()

if __name__ == "__main__":
    asyncio.run(main())
