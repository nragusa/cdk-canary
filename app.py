#!/usr/bin/env python3
import os

import aws_cdk as cdk

from canary.canary_stack import CanaryStack


app = cdk.App()
CanaryStack(
    app,
    'CanaryStack',
    description='Creates a simple AWS CloudWatch Synthetics heartbeat canary',
    tags={
        'Project': 'Canary Monitoring'
    }
)

app.synth()
