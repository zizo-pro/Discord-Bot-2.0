async def ping(ctx,client):
	await ctx.send_message(f"Pong in! {round(client.latency*1000)}ms")