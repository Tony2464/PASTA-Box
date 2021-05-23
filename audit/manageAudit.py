import json

# Audit configuration file
pastaAuditConfig = "/PASTA-Box/audit/config.json"


# Get the audit config from /PASTA-Box/audit/config.json

def getAuditMode():
    with open(pastaAuditConfig, encoding="utf8", errors="ignore") as configFile:
        configData = configFile.read()
        configFile.close()
    return json.loads(configData)
