#!/bin/bash

# Backup Arkana para OneDrive
# Executa: ./scripts/backup-to-onedrive.sh

BACKUP_DIR="$HOME/OneDrive/Backups/Arkana"
DATE=$(date +%Y%m%d_%H%M%S)

echo "🔄 Iniciando backup Arkana - $DATE"

# Criar diretório
mkdir -p "$BACKUP_DIR/$DATE"

# Backup MongoDB
echo "📦 Backup MongoDB..."
docker exec arkana-mongodb mongodump --archive=/tmp/mongodb_backup.gz --gzip
docker cp arkana-mongodb:/tmp/mongodb_backup.gz "$BACKUP_DIR/$DATE/mongodb.gz"

# Backup Redis
echo "📦 Backup Redis..."
docker exec arkana-redis redis-cli --pass ${REDIS_PASSWORD:-changeme} SAVE
docker cp arkana-redis:/data/dump.rdb "$BACKUP_DIR/$DATE/redis.rdb"

# Backup MinIO
echo "📦 Backup MinIO..."
docker exec arkana-minio tar czf /tmp/minio_backup.tar.gz /data
docker cp arkana-minio:/tmp/minio_backup.tar.gz "$BACKUP_DIR/$DATE/minio.tar.gz"

# Backup configs
echo "📦 Backup configs..."
cp -r monitoring "$BACKUP_DIR/$DATE/"
cp docker-compose.avila-full.yml "$BACKUP_DIR/$DATE/"
cp .env.production "$BACKUP_DIR/$DATE/.env.production.backup"

# Limpar backups antigos (manter últimos 30 dias)
find "$BACKUP_DIR" -type d -mtime +30 -exec rm -rf {} + 2>/dev/null

echo "✅ Backup concluído em: $BACKUP_DIR/$DATE"
echo "📊 Tamanho: $(du -sh $BACKUP_DIR/$DATE | cut -f1)"
