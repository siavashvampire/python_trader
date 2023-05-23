from app.models.altitude.play_altitude_model import PlayAltitude


def play_altitude(app_name: str):
    if app_name == "altitude_discrete":
        env_name = "scripts:learn_altitude_ctrl_discrete_env-v0"
        file_name = "best_model.zip"
        times = 2
        max_integrate_time = 15
        random_start = True
    elif app_name == "altitude_continuous":
        env_name = "scripts:learn_altitude_ctrl_continuous_env-v0"
        file_name = "best_model.zip"
        times = 2
        max_integrate_time = 15
        random_start = True
    elif app_name == "altitude_fragment":
        env_name = "scripts:learn_altitude_ctrl_fragment_env-v0"
        file_name = "best_model.zip"
        times = 2
        max_integrate_time = 15
        random_start = True
    elif app_name == "altitude_test":
        env_name = "scripts:learn_altitude_ctrl_test_env-v0"
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

    learning_altitude = PlayAltitude(name=app_name, file_name=file_name, env_name=env_name,
                                     max_integrate_time=max_integrate_time, times=times, random_start=random_start)
    learning_altitude.play()
