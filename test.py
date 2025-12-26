from sambanova import SambaNova

client = SambaNova(
    api_key="8807ef7a-77c5-4d01-93cd-cd7c25997674",
    base_url="https://api.sambanova.ai/v1"
)

models = client.models.list()
print("AVAILABLE MODELS:")
for m in models.data:
    print("-", m.id)
