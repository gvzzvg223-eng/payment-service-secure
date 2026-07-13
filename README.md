{
    "build": {
        "builder": "NIXPACKS"
    },
    "deploy": {
        "healthcheckPath": "/health",
        "healthcheckTimeout": 300,
        "startupTimeout": 300,
        "restartPolicyType": "always",
        "restartPolicyMaxRetries": 10
    }
}
