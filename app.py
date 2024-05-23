import gradio as gr
from huggingface_hub import list_models


def hello(profile: gr.OAuthProfile | None) -> str:
    # ^ expect a gr.OAuthProfile object as input to get the user's profile
    # if the user is not logged in, profile will be None
    if profile is None:
        return "I don't know you."
    return f"Hello {profile.name}"


def list_private_models(profile: gr.OAuthProfile | None, oauth_token: gr.OAuthToken | None) -> str:
    # ^ expect a gr.OAuthToken object as input to get the user's token
    # if the user is not logged in, oauth_token will be None
    if oauth_token is None:
        return "Please log in to list private models."
    models = [
        f"{model.id} ({'private' if model.private else 'public'})"
        for model in list_models(author=profile.username, token=oauth_token.token)
    ]
    return "Models:\n\n" + "\n - ".join(models) + "."


with gr.Blocks() as demo:
    gr.Markdown(
        "# Gradio OAuth Space"
        "\n\nThis Space is a demo for the **Sign in with Hugging Face** feature. "
        "Duplicate this Space to get started."
        "\n\nFor more details, check out:"
        "\n- https://www.gradio.app/guides/sharing-your-app#o-auth-login-via-hugging-face"
        "\n- https://huggingface.co/docs/hub/spaces-oauth"
    )
    gr.LoginButton()
    # ^ add a login button to the Space
    m1 = gr.Markdown()
    m2 = gr.Markdown()
    demo.load(hello, inputs=None, outputs=m1)
    demo.load(list_private_models, inputs=None, outputs=m2)

demo.launch()
