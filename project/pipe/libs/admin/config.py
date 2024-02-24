
class Config:
    def __init__(self):
        self.shape = (480, 640, 3)
        self.reshape = (1, self.shape[0], self.shape[1], self.shape[2])
        self.update_interval = 5
        self.fps = 1

    def get_frame_config(self):
        return self.fps, self.shape, self.reshape

    def get_update_interval(self):
        return self.update_interval

    def get_project_info(self):
        return [
            ["Project", "Mimir"],
            ["Version", "0.1.0"],
            ["Company", "-"],
            ["Setting", f"update each {self.update_interval}s"],
            ["License", "12345-6"],
        ], ["Info", "Value"]
