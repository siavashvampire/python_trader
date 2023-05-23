from app.models.altitude.learn_altitude_model import LearningAltitude


def learn_altitude(app_name: str, max_iter: int):
    if "altitude_discrete" in app_name:
        env_name = "scripts:learn_altitude_ctrl_discrete_env-v0"
        policy = "MlpPolicy"
        max_integrate_time = 6
        random_start = False
    elif "altitude_continuous" in app_name:
        env_name = "scripts:learn_altitude_ctrl_continuous_env-v0"
        policy = "MlpPolicy"
        max_integrate_time = 6
        random_start = False
    elif "altitude_fragment" in app_name:
        env_name = "scripts:learn_altitude_ctrl_fragment_env-v0"
        policy = "MlpPolicy"
        max_integrate_time = 6
        random_start = False
    elif "altitude_test" in app_name:
        env_name = "scripts:learn_altitude_ctrl_test_env-v0"
        policy = "MlpPolicy"
        max_integrate_time = 6
        random_start = False
    else:
        env_name = ""
        policy = "MlpPolicy"
        max_integrate_time = 3
        random_start = False

    learning_altitude = LearningAltitude(name=app_name, env_name=env_name, policy=policy,
                                         max_integrate_time=max_integrate_time, random_start=random_start)
    learning_altitude.learn(max_iter=max_iter)
