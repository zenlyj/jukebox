class ResourceAlreadyExists(Exception):
    def __init__(self, resource: str):
        self.resource = resource
        super().__init__(f"{resource} already exists")
