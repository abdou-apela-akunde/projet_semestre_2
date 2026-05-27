import subprocess

scripts = [
    "nettoyage_db.py",
    "create_tables.py",
    "collecte_dim_geo_professions.py",
    "collecte_dim_activite.py",
    "collecte_dim_financier.py",
    "verification.py"
]

for script in scripts:

    print(f"\n===== EXECUTION {script} =====\n")

    subprocess.run(["python", script], check=True)

print("\nPipeline terminé.")