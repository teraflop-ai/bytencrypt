import os

from infisical_sdk import InfisicalSDKClient


class Vault:
    def __init__(
        self,
        project_id=None,
        env="prod",
        path="/",
        host=None,
        client_id=None,
        client_secret=None,
    ):
        self.project_id = project_id or os.environ["INFISICAL_PROJECT_ID"]
        self.env, self.path = env, path
        self.client = InfisicalSDKClient(
            host=host or os.environ.get("INFISICAL_HOST", "https://app.infisical.com")
        )
        self.client.auth.universal_auth.login(
            client_id or os.environ["INFISICAL_CLIENT_ID"],
            client_secret or os.environ["INFISICAL_CLIENT_SECRET"],
        )

    def get(self, name):
        return self.client.secrets.get_secret_by_name(
            secret_name=name,
            project_id=self.project_id,
            environment_slug=self.env,
            secret_path=self.path,
        ).secretValue
