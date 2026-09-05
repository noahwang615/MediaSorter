FROM python:3.11-slim

# ffmpeg provides ffprobe, required for video metadata parsing
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY scripts/requirements.txt ./scripts/requirements.txt
RUN pip install --no-cache-dir -r scripts/requirements.txt

COPY scripts/mediasorter.py scripts/make_proofs.py scripts/migrate_to_raw.py ./scripts/

COPY scripts/entrypoint.sh scripts/proof_entrypoint.sh ./
RUN chmod +x ./entrypoint.sh ./proof_entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
