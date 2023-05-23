from app.models.attitude.play_attitude_model import PlayAttitude


def play_attitude(app_name: str):
    if app_name == "attitude_discrete":
        env_name = "scripts:learn_attitude_ctrl_discrete_env-v0"
        file_name = "best_model.zip"
        times = 2
        max_integrate_time = 15
        random_start = True
    elif app_name == "attitude_continuous":
        env_name = "scripts:learn_attitude_ctrl_continuous_env-v0"
        file_name = "best_model.zip"
        times = 2
        max_integrate_time = 15
        random_start = True
    elif app_name == "attitude_fragment":
        env_name = "scripts:learn_attitude_ctrl_fragment_env-v0"
        file_name = "best_model.zip"
        times = 2
        max_integrate_time = 15
        random_start = True
    elif app_name == "attitude_test":
        env_name = "scripts:learn_attitude_ctrl_test_env-v0"
        file_name = "best_model.zip"
        times = 2
        max_integrate_time = 15
        random_start = True
    else:
        env_name = ""
        file_name = ""
        times = 5
        max_integrate_time = 15
        random_start = True

    learning_attitude = PlayAttitude(name=app_name, file_name=file_name, env_name=env_name,
                                     max_integrate_time=max_integrate_time, times=times, random_start=random_start)
    learning_attitude.play()
