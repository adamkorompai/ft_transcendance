#!/bin/sh

# Chemin du fichier à vérifier
fichier_a_verifier="/certificates/cert.pem"

# Boucle tant que le fichier n'existe pas
while [ ! -f "$fichier_a_verifier" ]; do
    echo "Le fichier $fichier_a_verifier n'existe pas encore. Attente de 5 secondes..."
    sleep 5
done

echo "Le fichier $fichier_a_verifier a été trouvé !"
# /bin/prometheus --config.file=/etc/prometheus/prometheus.yml \
/bin/prometheus \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.path=/prometheus \
  --storage.tsdb.retention.time=30d
