from aws_cdk import (
    # Duration,
    CfnParameter,
    Stack,
    aws_synthetics_alpha as synth,
    # aws_sqs as sqs,
)
from constructs import Construct


class CanaryStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "CanaryQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )

        endpoint_url = CfnParameter(
            self,
            'EndpointUrl',
            description='The endpoint you wish to monitor, e.g. https://my.example-endpoint.com/',
            type='String',
            default='https://google.com/'
        )

        synth.Canary(
            self,
            'HeartbeatCanary',
            runtime=synth.Runtime.SYNTHETICS_NODEJS_PUPPETEER_3_9,
            test=synth.Test.custom(
                code=synth.Code.from_inline(
                    "var synthetics = require('Synthetics');\nconst log = require('SyntheticsLogger');\nconst index = async function () {\n// INSERT URL here\n" + f"const URL = \"{endpoint_url.value_as_string}\";" +
                    "\n\nlet page = await synthetics.getPage();\nconst response = await page.goto(URL, {waitUntil: 'domcontentloaded', timeout: 30000});\n//Wait for page to render.\n//Increase or decrease wait time based on endpoint being monitored.\nawait page.waitFor(15000);\nawait synthetics.takeScreenshot('loaded', 'loaded');\nlet pageTitle = await page.title();\nlog.info('Page title: ' + pageTitle);\nif (response.status() !== 200) {\n     throw \"Failed to load page!\";\n}\n};\n\nexports.handler = async () => {\nreturn await index();\n};\n"
                ),
                handler='index.handler'
            )
        )
