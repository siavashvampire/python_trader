from app.models.attitude.learn_attitude_model import LearningAttitude


def learn_attitude(app_name: str, max_iter: int):
    if "attitude_discrete" in app_name:
        env_name = "scripts:learn_attitude_ctrl_discrete_env-v0"
        policy = "MlpPolicy"
        max_integrate_time = 3
        random_start = False
    elif "attitude_continuous" in app_name:
        env_name = "scripts:learn_attitude_ctrl_continuous_env-v0"
        policy = "MlpPolicy"
        max_integrate_time = 3
        random_start = False
    elif "attitude_fragment" in app_name:
        env_name = "scripts:learn_attitude_ctrl_fragment_env-v0"
        policy = "MlpPolicy"
        max_integrate_time = 3
        random_start = False
    elif "attitude_test" in app_name:
        env_name = "scripts:learn_attitude_ctrl_test_env-v0"
        policy = "MlpPolicy"
        max_integrate_time = 3
        random_start = False
    else:
        env_name = ""
        policy = "MlpPolicy"
        max_integrate_time = 3
        random_start = False

    learning_attitude = LearningAttitude(name=app_name, env_name=env_name, policy=policy,
                                         max_integrate_time=max_integrate_time, random_start=random_start)
    learning_attitude.learn(max_iter=max_iter)
