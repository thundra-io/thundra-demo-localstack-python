# from pathlib import Path

# from dotenv import load_dotenv

# env_path = Path('/Users/gokhansimsek/Desktop/thundra-demo-localstack-python/localstack.env')
# load_dotenv(dotenv_path=env_path)

import thundra

thundra.configure(
    options={
        "config": {
            "thundra.apikey": "6327942a-36ff-40a5-a840-98e71cc2af7e",
            "thundra.agent.test.project.id": "91596bb4-f5cf-4c28-9008-7eead02bd70f",
            "thundra.agent.application.name": "foresight_deneme_genel",
            "thundra.agent.debug.enable": "True",
            "thundra.agent.report.rest.baseurl": "https://collector.thundra.me/v1",
        }
    }
)