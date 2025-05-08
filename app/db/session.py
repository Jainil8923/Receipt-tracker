from generated.prisma import Client

prisma = Client()

async def connect():
    try:
        await prisma.connect()
    except Exception as e:
        raise RuntimeError(f"Database connection failed: {e}")

async def disconnect():
    try:
        await prisma.disconnect()
    except Exception as e:
        raise RuntimeError(f"Database disconnection failed: {e}")