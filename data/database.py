import sqlite3
import json

class ExperimentDB:
    def __init__(self, db_name="data/experiments.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            # Create ExperimentConfig table
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS ExperimentConfig (
                    config_id INTEGER PRIMARY KEY,
                    random_seed INTEGER,
                    pong_config TEXT,
                    agent_config TEXT,
                    gridlink_config TEXT
                );
            """)

            # Create Experiment table
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS Experiment (
                    experiment_id INTEGER PRIMARY KEY,
                    config_id INTEGER,
                    start_time TEXT,
                    end_time TEXT,
                    steps_taken INTEGER,
                    results TEXT,
                    notes TEXT,
                    FOREIGN KEY (config_id) REFERENCES ExperimentConfig (config_id)
                );
            """)

            # Create Steps table
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS Steps (
                    step_id INTEGER PRIMARY KEY,
                    experiment_id INTEGER,
                    step_num INTEGER,
                    agent_action INTEGER,
                    environment_state TEXT,
                    FOREIGN KEY (experiment_id) REFERENCES Experiment (experiment_id)
                );
            """)

    def get_config_id(self, random_seed, pong_config, agent_config, gridlink_config):
        """
        Check if a similar configuration already exists in the database.
        If it exists, return the config_id.
        If it doesn't exist, insert the new configuration and return its config_id.
        """
        pong_config_str = json.dumps(pong_config)
        agent_config_str = json.dumps(agent_config)
        gridlink_config_str = json.dumps(gridlink_config)

        cur = self.conn.cursor()
        cur.execute("SELECT config_id FROM ExperimentConfig WHERE random_seed = ? AND pong_config = ? AND agent_config = ? AND gridlink_config = ?",
                    (random_seed, pong_config_str, agent_config_str, gridlink_config_str))
        
        result = cur.fetchone()
        if result:
            return result[0]
        else:
            return self.insert_experiment_config(random_seed, pong_config, agent_config, gridlink_config)

    def insert_experiment_config(self, random_seed, pong_config, agent_config, gridlink_config):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO ExperimentConfig (random_seed, pong_config, agent_config, gridlink_config) VALUES (?, ?, ?, ?)", 
                        (random_seed, json.dumps(pong_config), json.dumps(agent_config), json.dumps(gridlink_config)))
            return cur.lastrowid

    def start_experiment(self, config_id, start_time, notes=""):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO Experiment (config_id, start_time, notes) VALUES (?, ?, ?)", (config_id, start_time, notes))
            return cur.lastrowid

    def finalize_experiment(self, experiment_id, end_time, steps_taken, results):
        results_str = json.dumps(results)
        with self.conn:
            self.conn.execute("UPDATE Experiment SET end_time = ?, steps_taken = ?, results = ? WHERE experiment_id = ?", (end_time, steps_taken, experiment_id, results_str))

    def insert_step(self, experiment_id, step_num, agent_action, environment_state):
        env_state_str = json.dumps(environment_state._asdict())  # Convert NamedTuple to dictionary and then to JSON string
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO Steps (experiment_id, step_num, agent_action, environment_state) VALUES (?, ?, ?, ?)", 
                        (experiment_id, step_num, agent_action, env_state_str))
            return cur.lastrowid

    def close(self):
        self.conn.close()
