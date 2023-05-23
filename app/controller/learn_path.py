from app.models.path_planning.learn_path_planning_model import LearningPathPlanning


def learn_path(app_name: str, max_iter: int):
    if app_name == "path_planning":
        env_name = "scripts:learn_path_env-v0"
        policy = "CnnPolicy"
        random_start = True
    else:
        env_name = ""
        policy = "CnnPolicy"
        random_start = True

    learning_altitude = LearningPathPlanning(name=app_name, env_name=env_name, policy=policy, random_start=random_start)
    learning_altitude.learn(max_iter=max_iter)
