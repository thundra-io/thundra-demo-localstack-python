dynamo_db_chaos = {
    "type": "FilteringSpanListener",
    "config": {
        "listener": {
            "type": "ErrorInjectorSpanListener",
            "config": {
                "errorType": "ChaosError",
                "errorMessage": "Dynamo DB Chaos Injected!",
                "InjectPerentage": 100
            }
        },
        "filters": [
            {
                "className": 'AWS-DynamoDB',
            }
        ]
    }
}