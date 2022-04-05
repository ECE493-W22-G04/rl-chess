# rl-chess
Play chess against other players or an RL agent


### Setup
Start server
```
cd server
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

Start client
```
cd client
npm install
npm start
```

### Run belief revision
Get migration from production db then run:
```
cd server
python -m rl_agent.belief_revision
```
