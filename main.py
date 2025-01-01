import asyncio
import logging
from livekit import rtc, agents
from livekit.agents import (
    JobContext,
    WorkerOptions,
    cli,
)

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("livekit-agent")

async def entrypoint(ctx: JobContext):
    logger.info(f"Conectando à sala {ctx.room.name}")
    await ctx.connect(auto_subscribe=agents.AutoSubscribe.AUDIO_ONLY)

    # Lógica para receber chamadas
    async def on_track_published(publication: rtc.RemoteTrackPublication, participant: rtc.RemoteParticipant):
        if publication.kind == rtc.TrackKind.KIND_AUDIO:
            logger.info(f"Áudio recebido de {participant.identity}")
            track = await publication.track
            # Aqui você pode processar o áudio recebido

    ctx.room.on("track_published", on_track_published)

    # Lógica para fazer chamadas
    if ctx.job.metadata:  # Se houver metadados, é uma chamada de saída
        phone_number = ctx.job.metadata
        logger.info(f"Discando para {phone_number} na sala {ctx.room.name}")

        # Cria um participante SIP para fazer a chamada
        await ctx.api.sip.create_sip_participant(
            rtc.CreateSIPParticipantRequest(
                room_name=ctx.room.name,
                sip_trunk_id="<sip_trunk_id>",  # Substitua pelo ID do seu tronco SIP
                sip_call_to=phone_number,
                participant_identity="phone_user",
            )
        )

        # Aguarda o participante SIP se conectar
        participant = await ctx.wait_for_participant(identity="phone_user")
        logger.info(f"Participante SIP conectado: {participant.identity}")

        # Lógica para interagir com o participante SIP
        while True:
            await asyncio.sleep(1)

    # Manter o agente em execução
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    # Inicia o agente
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            agent_name="voice-agent",  # Nome do agente para despacho
        )
    )
