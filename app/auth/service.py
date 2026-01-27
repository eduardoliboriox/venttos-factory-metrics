from app.auth.repository import get_user_by_provider, create_user

def get_or_create_user(profile, provider):
    provider_id = profile["id"]
    email = profile["email"]
    username = email.split("@")[0]

    user = get_user_by_provider(provider, provider_id)
    if user:
        return user

    return create_user({
        "username": username,
        "email": email,
        "provider": provider,
        "provider_id": provider_id
    })
