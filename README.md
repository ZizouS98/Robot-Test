#  Robot Test Project — Automatisation complète (simulation & matériel)

##  Description
Ce projet a pour objectif de **valider le pilotage d’un robot simple** via un protocole ASCII (commandes `/AR move`, `/AR get`, `/AR set`).  
Il comprend à la fois :
- un **simulateur logiciel** du robot (`SimSerial`),  
- une interface cliente (`RobotClient`),  
- et un ensemble de **tests automatisés Pytest** couvrant l’intégralité du plan de validation.

---

##  Structure du projet
```
robot_test_project_full/
│
├── src/
│   ├── simulator.py        # Simule un robot (ASCII, pos, speed, déplacements)
│   └── robot_client.py     # Interface Python : envoi/réception de commandes
│
├── tests/
│   ├── test_functional.py       # Tests fonctionnels de base (T1→T5)
│   ├── test_speed_rules.py      # Tests sur la variable speed (T1→T4)
│   ├── test_protocol.py         # Tests protocole & robustesse (T1→T5)
│   ├── test_dynamics.py         # Tests dynamiques position/stabilité (T2→T3)
│   ├── test_speed_timing.py     # Test vitesse réelle (T1)
│   └── test_with_hardware.py    # Version matériel réel (désactivée par défaut)
│
└── README.md                    # Ce fichier
```

---

## Exécution (simulation, sans matériel)
```bash
cd robot_test_project_full
python3 -m venv .venv
source .venv/bin/activate        # Sous Windows : .venv\Scripts\activate
pip install pytest
pytest -q                        # Exécute tous les tests (simulateur)
```

**Résultat attendu :**
```
.........................                                          [100%]
17 passed in X.XXs
```

---

## Exécution sur matériel réel (optionnel)
Pour exécuter les tests sur un robot connecté physiquement via port série :

### 1. Configurer le port série :
- **macOS/Linux :**
  ```bash
  export ROBOT_PORT=/dev/tty.usbserial-XXXX
  export ROBOT_ADDR=01
  ```
- **Windows (PowerShell) :**
  ```powershell
  $env:ROBOT_PORT="COM"
  $env:ROBOT_ADDR="01"
  ```

### 2. Lancer uniquement les tests matériels :
```bash
pytest -q tests/test_with_hardware.py
```

💡 Si `ROBOT_PORT` n’est pas défini, les tests matériels sont **automatiquement ignorés** (`skip`).

---

## Catégories de tests automatisés
| Fichier | Catégorie | Objectif principal |
|----------|------------|--------------------|
| `test_functional.py` | Tests fonctionnels de base | Vérifie `get`, `move`, cohérence position |
| `test_speed_rules.py` | Variable `speed` | Bornes, rejets, persistance |
| `test_protocol.py` | Protocole ASCII & robustesse | Syntaxe, adresses, erreurs |
| `test_dynamics.py` | Dynamique du déplacement | Stabilité et évolution régulière |
| `test_speed_timing.py` | Influence de la vitesse | t(2) > t(5) > t(10) |
| `test_with_hardware.py` | Tests réels (optionnels) | Exécution sur robot physique réelle |

---

## Technologies utilisées
- **Python 3**
- **Pytest** — framework de test unitaire
- **SimSerial** — simulateur interne du robot
- **RobotClient** — abstraction unifiée pour matériel/simulateur

---

## Résultats globaux
| Environnement | Tests exécutés | Résultat |
|----------------|----------------|-----------|
| Simulation (par défaut) | 17 tests |  100% passed |
| Matériel réel (optionnel) | 5 tests fonctionnels |  En attente matériel |


---

## Points forts
- Plan de test **entièrement automatisé (17 cas)**
- Tests **simulables sans matériel**
- Réponses ASCII **parfaitement conformes à la spécification**

---

###  En résumé :
Ce projet illustre une démarche complète de **test et validation hardware**, alliant : 
- couverture exhaustive des cas de test,  
- et automatisation intégrale des scénarios fonctionnels, dynamiques et de robustesse.
