from generated.prisma import Client

prisma = Client()

async def connect():
    await prisma.connect()

async def disconnect():
    await prisma.disconnect()