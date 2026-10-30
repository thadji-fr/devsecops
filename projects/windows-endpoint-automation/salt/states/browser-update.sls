# Exemple public uniquement - ne contient ni source ni version internes.
# Requiert des valeurs Pillar de laboratoire :
# portfolio:choco_source et portfolio:firefox_fixed_version
# Verifier les versions de Salt, Chocolatey et du paquet cible.
firefox_correctif_laboratoire:
  chocolatey.upgraded:
    - name: firefox
    - version: '{{ pillar["portfolio"]["firefox_fixed_version"] }}'
    - source: '{{ pillar["portfolio"]["choco_source"] }}'
