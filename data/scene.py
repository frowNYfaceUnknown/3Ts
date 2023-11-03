class Scene:
    def __init__(self) -> None:
        pass ## hook method

    def handle_events(self, events):
        raise NotImplementedError ## hook method

    def update(self) -> None:
        raise NotImplementedError ## hook method

    def draw(self) -> None:
        raise NotImplementedError ## hook method

class SceneManager:
    def __init__(self, initScene) -> None:
        self.go_to(initScene)

    def go_to(self, scene) -> None:
        self.scene = scene
        self.scene.manager = self