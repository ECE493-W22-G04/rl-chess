## Server

### Requirements
* Python 3.9
* Postgres 13 (you can use the following docker command to build the default postgres server)
    ```sh
    docker run --rm --name pg-rl-chess \ 
      -e POSTGRES_PASSWORD=postgres \ 
      -e POSTGRES_USER=postgres \ 
      -d -p 5432:5432 \
      -v $HOME/docker/volumes/postgres/rl-chess:/var/lib/postgresql/data \ 
      postgres:13
    ```
* (Optional) sqlite -- to run tests

### Getting started
1. Install deps
    ```sh
    cd server
    pip install -r requirements.txt
    ````
2. Initialize database
    ```sh
    FLASK_APP=server flask db upgrade
    ```
    > You need to run this command everytime there is a model update or there is a new migration
3. Setup the `.env` file following the template
    ```
    cp .env.template .env
    ```
    Then modify the newly created `.env`
4. Run server in development mode
    ```sh
    make start
    ```
    
    or
    
    ```sh
    python -m server
    ```
    If you want to run the server in production mode use
    ```
    gunicorn --worker-class eventlet -w 1 server:app -b 0.0.0.0:5555
    ```
5. (Optional) Run tests
    ```
    make test
    ```
    
    or

    ```sh
    pytest -x -v
    ```


## Reinforcement Learning

### Self training

1. Checkout latest `main` branch
2. Activate your virtual environment (optional)
3. Install dependencies
4. Run the following script under `/server/`
   ```
   <python3.9> -m rl_agent.train
   ```


### Belief revision

1. Checkout latest `main` branch
2. Activate your virtual environment (optional)
3. Install dependencies
4. Run the following script under `/server/`
    ```
    <python3.9> -m rl_agent.belief
    ```